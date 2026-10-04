#!/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
r"""
c5_face_swap_cli.py — CLI de Producción para Neural Video Face Swapping en Apple Silicon.
Desplegado para el skill c5-neural-face-swap-cuadrilla (V2 SOTA Architecture).

Mejoras de Síntesis Dialéctica (Iteración Recursiva V2):
- Restauración Facial Neuronal 512x512 (GPEN / CodeFormer / GFPGAN): Erradicación del cuello de botella de 128px.
- Segmentación Semántica y Desoclusión (BiSeNet ResNet-34): Preservación de manos, gafas, pelo y micrófonos.
- Transporte Óptimo Lineal (MKL): Coincidencia de covarianza cromática completa en espacio BGR canónico.
- FaceTracker Zero-Drop: Extrapolación inercial ante desenfoque cinético y 1-Euro Filter independiente por track.
- Aceleración en Silicio FP16 (Inswapper 128 FP16 en Apple Neural Engine ANE/CoreML).
- Worker Chunking Paralelo (--workers N): Inferencia multi-proceso desacoplada en Apple Silicon.
- Embeddings Serializados: Extracción previa O(1) de identidades, eliminando contención de recognition.
- Modo Watcher Daemon (--watch <inbox>): Ingesta reactiva autónoma de vídeos y URLs en segundo plano.
- Codificación acelerada por hardware Apple Silicon VideoToolbox (H.264 / HEVC).
"""

import sys
import os
import time
import argparse
import subprocess
import glob
import shutil
import cv2
import numpy as np
import onnxruntime as ort

PYTHON_BIN = "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
sys.path.insert(0, SCRIPT_DIR)

try:
    from c5_smoother import (
        OneEuroFilter,
        FaceTracker,
        TemporalPatchStabilizer,
        VerticalFramingTracker,
        reinhard_color_transfer,
        monge_kantorovich_color_transfer,
        spatial_illumination_transfer,
        match_sensor_grain,
        soft_elliptical_blend,
        get_bisenet_semantic_mask,
        restore_face_patch,
        sharpen_face_patch,
        two_band_blend_patch,
        estimate_dense_68_landmarks,
        estimate_head_pose_3d,
        compute_mouth_aspect_ratio,
        compute_eye_aspect_ratio,
        compute_frechet_mean,
        slerp_embeddings
    )
except ImportError:
    OneEuroFilter = None
    FaceTracker = None
    TemporalPatchStabilizer = None
    VerticalFramingTracker = None
    reinhard_color_transfer = None
    monge_kantorovich_color_transfer = None
    spatial_illumination_transfer = None
    match_sensor_grain = None
    soft_elliptical_blend = None
    get_bisenet_semantic_mask = None
    restore_face_patch = None
    sharpen_face_patch = None
    two_band_blend_patch = None
    estimate_dense_68_landmarks = None
    estimate_head_pose_3d = None
    compute_mouth_aspect_ratio = None
    compute_eye_aspect_ratio = None
    compute_frechet_mean = None
    slerp_embeddings = None

import insightface
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model
from insightface.utils import face_align

FACES_DIR = "/Users/borjafernandezangulo/Downloads/VIDEO BODA HUGO/faces"
MOVIES_DIR = "/Users/borjafernandezangulo/Movies/VIDEOS_MITICOS"
MODELS_DIR = os.path.expanduser("~/.insightface/models")

INSWAPPER_FP32_PATH = os.path.join(MODELS_DIR, "inswapper_128.onnx")
INSWAPPER_FP16_PATH = os.path.join(MODELS_DIR, "inswapper_128_fp16.onnx")
INSWAPPER_PATH = INSWAPPER_FP32_PATH if os.path.isfile(INSWAPPER_FP32_PATH) else INSWAPPER_FP16_PATH
CODEFORMER_PATH = os.path.join(MODELS_DIR, "codeformer.onnx")
GPEN_PATH = os.path.join(MODELS_DIR, "gpen_bfr_512.onnx")
GFPGAN_PATH = os.path.join(MODELS_DIR, "gfpgan_1.4.onnx")
BISENET_PATH = os.path.join(MODELS_DIR, "bisenet_resnet_34.onnx")
FAN_PATH = os.path.join(MODELS_DIR, "fan_68_5.onnx")
TEMP_EMBEDDINGS_PATH = "/tmp/c5_source_embeddings.npz"

ROSTER = {
    "alain": "alain_real.png",
    "alain elektronische": "alain_real.png",
    "eder": "eder_real.png",
    "eder dual sound": "eder_real.png",
    "luengo": "luengo_real.png",
    "tigre maquina": "luengo_real.png",
    "xabi": "xabi_real.png",
    "cabeza gigante": "xabi_real.png",
    "borja": "borja_real.png",
    "moskv": "borja_real.png",
    "hugo": "hugo_real.png",
    "hugo pink": "hugo_real.png",
    "mitxu": "mitxu_gafas_tecnicas.jpg",
    "mitxu gafas": "mitxu_gafas_tecnicas.jpg",
    "mitxu_gafas": "mitxu_gafas_tecnicas.jpg",
    "mitxu real": "mitxu_real.png",
    "el mitxus": "mitxu_gafas_tecnicas.jpg",
    "pedrerol": "pedrerol_real.png",
    "tosso": "tosso_real.png",
    "lander": "lander_real.png",
    "medina": "medina_real.png",
    "patxi": "patxi_real.png",
    "david landeta": "david_landeta_real.png",
    "landeta": "david_landeta_real.png",
    "aloisio": "aloisio_real.png",
    "jorge malatesta": "jorge_malatesta_real.png",
    "malatesta": "jorge_malatesta_real.png",
    "txinorris": "txinorris_real.png",
    "the brother": "the_brother_real.png",
    "diana": "diana_real.png",
    "chiquito": "chiquito_real.png",
    "chiquito de la calzada": "chiquito_real.png",
    "unaitxu": "unaitxu_real.png",
    "trump": "trump_real.jpg",
    "donald trump": "trump_real.jpg"
}

class MinimalSourceFace:
    """Contenedor ligero de embedding para desacoplar workers del modelo de reconocimiento."""
    def __init__(self, embedding, normed_embedding, angles=None):
        self.embedding = embedding
        self.normed_embedding = normed_embedding
        self.angles = angles or []  # list of (emb, normed_emb, yaw)

    def get_embedding_for_yaw(self, target_yaw):
        if not self.angles or len(self.angles) <= 1:
            return self.embedding, self.normed_embedding
        angles_sorted = sorted(self.angles, key=lambda a: abs(a[2] - target_yaw))
        best = angles_sorted[0]
        if abs(best[2] - target_yaw) < 8.0 or len(angles_sorted) < 2:
            return best[0], best[1]
        second = angles_sorted[1]
        y1, y2 = best[2], second[2]
        if abs(y1 - y2) > 1e-3 and slerp_embeddings:
            t = np.clip((target_yaw - y1) / (y2 - y1), 0.0, 1.0)
            fused = slerp_embeddings(best[1], second[1], float(t))
            return fused, fused
        return best[0], best[1]

def resolve_single_identity(name_or_path):
    if os.path.isfile(name_or_path):
        return name_or_path
    clean_name = name_or_path.lower().strip()
    if clean_name in ROSTER:
        full_p = os.path.join(FACES_DIR, ROSTER[clean_name])
        if os.path.isfile(full_p):
            return full_p
    for k, fname in ROSTER.items():
        if clean_name in k or k in clean_name:
            full_p = os.path.join(FACES_DIR, fname)
            if os.path.isfile(full_p):
                return full_p
    raise ValueError(f"Identidad '{name_or_path}' no encontrada en el Roster ({FACES_DIR}).")

def resolve_identity_paths(identity_spec):
    """
    Resuelve una especificación de identidad hacia una lista de rutas de imágenes.
    Soporta:
    - Nombre del roster o ruta de archivo única: e.g. 'alain'
    - Identidades compuestas con '+': e.g. 'mitxu_gafas+mitxu_real'
    - Directorio con imágenes: e.g. '/path/to/mitxu_angles/'
    """
    if os.path.isdir(identity_spec):
        valid_exts = {'.png', '.jpg', '.jpeg', '.webp'}
        imgs = [os.path.join(identity_spec, f) for f in sorted(os.listdir(identity_spec))
                if os.path.splitext(f)[1].lower() in valid_exts]
        if not imgs:
            raise ValueError(f"Directorio de identidades vacío: {identity_spec}")
        return imgs

    parts = [p.strip() for p in identity_spec.split('+') if p.strip()]
    resolved = []
    for part in parts:
        resolved.append(resolve_single_identity(part))
    return resolved

# Alias para compatibilidad hacia atrás
resolve_identity_image = resolve_single_identity

def purge_temp_onnx_artifacts():
    """Purga determinista de artefactos .mlmodel/.mlmodelc huérfanos para preservar el disco."""
    for p in glob.glob('/var/folders/r_/hw1ds2nj49zffr6r4m_81r5h0000gn/T/onnxruntime-*'):
        try:
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            else:
                os.remove(p)
        except Exception:
            pass

def render_worker_chunk(
    video_path, source_faces, start_frame, end_frame, out_part_path,
    fps, width, height, bitrate, use_smooth=True,
    enhancer='gpen', enhance_weight=0.7, mask_mode='bisenet', color_transfer='mkl',
    lighting='spatial', grain_strength=0.5, preserve_mouth='auto', preserve_eyes='auto',
    blend_mode='two-band', stabilize_patch=True,
    target_face_index=0, swap_all=False,
    worker_id=0
):
    """Procesa una franja contigua de fotogramas [start_frame, end_frame) en un subproceso aislado."""
    app_det = FaceAnalysis(name='buffalo_l', allowed_modules=['detection'], providers=['CPUExecutionProvider'])
    app_det.prepare(ctx_id=0, det_size=(640, 640))
    swapper = get_model(INSWAPPER_PATH, providers=['CoreMLExecutionProvider', 'CPUExecutionProvider'])

    # Sesiones ONNX para Restaurador, Segmentación y Landmarker 3D
    sess_opts = ort.SessionOptions()
    sess_opts.intra_op_num_threads = 4

    enhancer_sess = None
    if enhancer in ['gpen', 'adaptive'] and os.path.isfile(GPEN_PATH):
        # CPUExecutionProvider con 4 hilos por worker: cero colisión de particiones y máxima estabilidad
        enhancer_sess = ort.InferenceSession(GPEN_PATH, sess_options=sess_opts, providers=['CPUExecutionProvider'])
    elif enhancer == 'codeformer' and os.path.isfile(CODEFORMER_PATH):
        enhancer_sess = ort.InferenceSession(CODEFORMER_PATH, sess_options=sess_opts, providers=['CPUExecutionProvider'])
    elif enhancer == 'gfpgan' and os.path.isfile(GFPGAN_PATH):
        enhancer_sess = ort.InferenceSession(GFPGAN_PATH, sess_options=sess_opts, providers=['CPUExecutionProvider'])

    bisenet_sess = None
    if mask_mode == 'bisenet' and os.path.isfile(BISENET_PATH):
        # Aceleración ANE / CoreML: 19ms por frame vs 284ms en CPU
        bisenet_sess = ort.InferenceSession(BISENET_PATH, sess_options=sess_opts, providers=['CoreMLExecutionProvider', 'CPUExecutionProvider'])

    fan_sess = None
    if os.path.isfile(FAN_PATH):
        fan_sess = ort.InferenceSession(FAN_PATH, sess_options=sess_opts, providers=['CPUExecutionProvider'])

    tracker = FaceTracker(max_extrapolate=2) if (FaceTracker and use_smooth) else None
    local_stabilizer = TemporalPatchStabilizer() if (TemporalPatchStabilizer and stabilize_patch) else None

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{width}x{height}',
        '-pix_fmt', 'bgr24',
        '-r', f'{fps}',
        '-i', '-',
        '-vf', 'cas=strength=0.6,unsharp=5:5:0.7:5:5:0.3,format=yuv420p',
        '-c:v', 'h264_videotoolbox',
        '-b:v', bitrate,
        '-pix_fmt', 'yuv420p',
        out_part_path
    ]
    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    num_frames = end_frame - start_frame
    t_start = time.time()
    dt = 1.0 / max(fps, 1.0)

    for idx in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break

        faces = app_det.get(frame)
        if tracker:
            tgt_idx = None if swap_all else target_face_index
            assignments = tracker.update(faces, len(source_faces), dt=dt, swap_all=swap_all, target_index=tgt_idx)
        else:
            if faces:
                faces_sorted = sorted(faces, key=lambda f: (f.bbox[2]-f.bbox[0]) * (f.bbox[3]-f.bbox[1]), reverse=True)
                if not swap_all and target_face_index is not None:
                    assignments = [(faces_sorted[target_face_index], 0, 0)] if target_face_index < len(faces_sorted) else []
                else:
                    assignments = [(f, i, i) for i, f in enumerate(faces_sorted) if i < len(source_faces)]
            else:
                assignments = []

        res = frame.copy()
        for item in assignments:
            if len(item) == 3:
                tf, face_idx, tid = item
            else:
                tf, face_idx = item
                tid = 0
            if face_idx < 0 or face_idx >= len(source_faces):
                continue
            src_f = source_faces[face_idx]

            # 1. FAN-68 dense landmarks, 3D pose, MAR y EAR
            mar = 0.0
            ear = 0.30
            pitch, yaw, roll = 0.0, 0.0, 0.0
            lm68 = None
            if fan_sess is not None and estimate_dense_68_landmarks:
                lm68 = estimate_dense_68_landmarks(tf.kps, fan_sess)
                if lm68 is not None:
                    if compute_mouth_aspect_ratio:
                        mar = compute_mouth_aspect_ratio(lm68)
                    if compute_eye_aspect_ratio:
                        ear = compute_eye_aspect_ratio(lm68)
                    if estimate_head_pose_3d:
                        pitch, yaw, roll = estimate_head_pose_3d(lm68, frame.shape)

            if preserve_mouth == 'true':
                mouth_active = True
            elif preserve_mouth == 'false':
                mouth_active = False
            else:  # auto
                mouth_active = (mar > 0.14)

            if preserve_eyes == 'gaze':
                eyes_active = 'gaze'
            elif preserve_eyes == 'true':
                eyes_active = True
            elif preserve_eyes == 'false':
                eyes_active = False
            else:  # auto (parpadeo u ojos cerrados)
                eyes_active = (ear < 0.18)

            # Inyección adaptativa de ángulo 3D si hay multi-referencia
            if hasattr(src_f, 'get_embedding_for_yaw') and src_f.angles:
                active_emb, active_norm = src_f.get_embedding_for_yaw(yaw)
                swap_src = MinimalSourceFace(active_emb, active_norm)
            else:
                swap_src = src_f

            bgr_fake, M = swapper.get(res, tf, swap_src, paste_back=False)

            if enhancer != 'none' and (enhancer_sess is not None or enhancer in ['adaptive', 'unsharp']):
                # =======================================================
                # PIPELINE V5 SOTA: 512p + Adaptive/GPEN CoreML + MKL + Spatial Lighting + Stabilizer + Sensor Grain + BiSeNet + Two-Band
                # =======================================================
                crop_512 = cv2.resize(bgr_fake, (512, 512), interpolation=cv2.INTER_CUBIC)

                # Super-resolución adaptativa según la escala del rostro
                face_h = tf.bbox[3] - tf.bbox[1]
                if enhancer == 'unsharp' or (enhancer == 'adaptive' and face_h < 140):
                    restored_512 = sharpen_face_patch(crop_512, amount=1.2) if sharpen_face_patch else crop_512
                else:
                    eff_enhancer = 'gpen' if enhancer == 'adaptive' else enhancer
                    restored_512 = restore_face_patch(crop_512, eff_enhancer, enhancer_sess, weight=enhance_weight)

                aimg_512, M_512 = face_align.norm_crop2(res, tf.kps, 512)

                # 1. Transferencia cromática global
                if color_transfer == 'mkl' and monge_kantorovich_color_transfer:
                    ready_512 = monge_kantorovich_color_transfer(restored_512, aimg_512)
                elif color_transfer == 'reinhard' and reinhard_color_transfer:
                    ready_512 = reinhard_color_transfer(restored_512, aimg_512)
                else:
                    ready_512 = restored_512

                # 2. Transferencia de iluminación espacial 3D y sombras
                if lighting == 'spatial' and spatial_illumination_transfer:
                    ready_512 = spatial_illumination_transfer(ready_512, aimg_512)

                # 3. Inyección de grano de sensor y textura analógica (anti-plasticidad GAN)
                if grain_strength > 0.0 and match_sensor_grain:
                    ready_512 = match_sensor_grain(ready_512, aimg_512, strength=grain_strength)

                # 4. Estabilización temporal inter-frame de parches (erradicación de GAN shimmer)
                if stabilize_patch:
                    if tracker:
                        motion = tracker.compute_motion(tid, tf.kps)
                        stab = tracker.get_stabilizer(tid)
                        if stab:
                            ready_512 = stab.stabilize(ready_512, motion)
                    elif local_stabilizer:
                        ready_512 = local_stabilizer.stabilize(ready_512, 0.0)

                IM_512 = cv2.invertAffineTransform(M_512)

                if bisenet_sess is not None and get_bisenet_semantic_mask:
                    lm68_512 = cv2.transform(lm68.reshape(1, -1, 2), M_512).reshape(-1, 2) if lm68 is not None else None
                    mask_512 = get_bisenet_semantic_mask(
                        aimg_512, bisenet_sess, feather=25,
                        preserve_mouth=mouth_active,
                        preserve_eyes=eyes_active,
                        eye_landmarks_512=lm68_512
                    )

                    if blend_mode == 'two-band' and two_band_blend_patch:
                        blended_512 = two_band_blend_patch(aimg_512, ready_512, mask_512, blur_ksize=21)
                        warped_mask = cv2.warpAffine(mask_512, IM_512, (width, height), borderValue=0.0)[:, :, None]
                        warped_blended = cv2.warpAffine(blended_512, IM_512, (width, height), borderValue=0.0)
                        res = np.clip(warped_mask * warped_blended + (1.0 - warped_mask) * res.astype(np.float32), 0, 255).astype(np.uint8)
                    else:
                        mask_512 = np.expand_dims(mask_512, axis=2)
                        warped_mask = cv2.warpAffine(mask_512, IM_512, (width, height), borderValue=0.0)
                        warped_mask = np.expand_dims(warped_mask, axis=2)
                        warped_fake = cv2.warpAffine(ready_512, IM_512, (width, height), borderValue=0.0)
                        res = np.clip(warped_mask * warped_fake + (1.0 - warped_mask) * res.astype(np.float32), 0, 255).astype(np.uint8)
                else:
                    mask_local = np.zeros((512, 512), dtype=np.float32)
                    cv2.ellipse(mask_local, (256, int(512 * 0.52)), (int(512 * 0.42), int(512 * 0.46)), 0, 0, 360, 1.0, -1)
                    mask_local = cv2.GaussianBlur(mask_local, (31, 31), 0)
                    warped_mask = cv2.warpAffine(mask_local, IM_512, (width, height), borderValue=0.0)
                    warped_mask = np.expand_dims(warped_mask, axis=2)
                    warped_fake = cv2.warpAffine(ready_512, IM_512, (width, height), borderValue=0.0)
                    res = np.clip(warped_mask * warped_fake + (1.0 - warped_mask) * res.astype(np.float32), 0, 255).astype(np.uint8)

            else:
                # =======================================================
                # PIPELINE V1 BASELINE: 128px + Soft Elliptical Blend
                # =======================================================
                if soft_elliptical_blend:
                    res = soft_elliptical_blend(res, bgr_fake, M)
                else:
                    res = swapper.get(res, tf, swap_src, paste_back=True)

        try:
            ffmpeg_proc.stdin.write(res.tobytes())
        except (BrokenPipeError, IOError):
            print(f"[!] Worker {worker_id} detectó cierre de tubería FFmpeg.", flush=True)
            break

        if (idx + 1) % 30 == 0 or idx == num_frames - 1:
            el = time.time() - t_start
            cur_fps = (idx + 1) / el if el > 0 else 0
            pct = (idx + 1) / num_frames * 100
            print(f"  [Worker {worker_id}] Frame {idx+1:04d}/{num_frames} ({pct:5.1f}%) | {cur_fps:.2f} FPS", flush=True)

    cap.release()
    ffmpeg_proc.stdin.close()
    ffmpeg_proc.wait()

def generate_vertical_916_video(master_video, out_916_path, bg_mode='crop', target_w=1080, target_h=1920):
    """
    Transforma un vídeo panorámico master en un reel vertical 9:16 (1080x1920)
    con rastreo de cámara inteligente (Pan & Scan) centrado en el rostro principal.
    Acelerado con Apple Silicon VideoToolbox y filtros unsharp+CAS.
    """
    if not VerticalFramingTracker:
        print("[!] VerticalFramingTracker no disponible. Omitiendo render 9:16.", flush=True)
        return None

    cap = cv2.VideoCapture(master_video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w_src = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h_src = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    tracker = VerticalFramingTracker(w_src, h_src, target_w=target_w, target_h=target_h)

    # Detector facial para centrar el encuadre
    app_det = FaceAnalysis(name='buffalo_l', allowed_modules=['detection'], providers=['CPUExecutionProvider'])
    app_det.prepare(ctx_id=0, det_size=(320, 320))

    temp_raw_916 = "/tmp/c5_vertical_nosound.mp4"
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{target_w}x{target_h}',
        '-pix_fmt', 'bgr24',
        '-r', f'{fps}',
        '-i', '-',
        '-vf', 'cas=strength=0.6,unsharp=5:5:0.7:5:5:0.3,format=yuv420p',
        '-c:v', 'h264_videotoolbox',
        '-b:v', '7500k',
        '-pix_fmt', 'yuv420p',
        temp_raw_916
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    dt = 1.0 / max(fps, 1.0)

    print(f"[*] Generando export vertical 9:16 ({target_w}x{target_h}) en modo '{bg_mode}'...", flush=True)
    for idx in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break
        primary_bbox = None
        if idx % 2 == 0:
            faces = app_det.get(frame)
            if faces:
                best_face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0]) * (f.bbox[3]-f.bbox[1]))
                primary_bbox = best_face.bbox

        crop_rect = tracker.update(primary_bbox, dt=dt)
        reframe = tracker.reframe_frame(frame, crop_rect, mode=bg_mode)
        proc.stdin.write(reframe.tobytes())

    cap.release()
    proc.stdin.close()
    proc.wait()

    subprocess.run([
        'ffmpeg', '-y',
        '-i', temp_raw_916,
        '-i', master_video,
        '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '192k',
        '-map', '0:v:0',
        '-map', '1:a:0?',
        '-shortest',
        out_916_path
    ], check=True, stderr=subprocess.DEVNULL)

    if os.path.isfile(temp_raw_916):
        os.remove(temp_raw_916)

    print(f"  [✓] Vídeo Vertical 9:16 listo: {out_916_path}", flush=True)
    return out_916_path

def process_video_pipeline(video_input, args):
    """Ejecuta el pipeline completo de Face Swap sobre un archivo de vídeo o URL."""
    if video_input.startswith("http://") or video_input.startswith("https://"):
        print(f"[*] Ingesta directa desde URL: {video_input}", flush=True)
        tmp_raw = "/tmp/c5_input_raw.mp4"
        dl_cmd = ['yt-dlp', '-f', 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best', '-o', tmp_raw, video_input]
        subprocess.run(dl_cmd, check=True)
        video_input = "/tmp/c5_input_h264.mp4"
        subprocess.run(['ffmpeg', '-y', '-i', tmp_raw, '-c:v', 'h264_videotoolbox', '-b:v', '8M', '-c:a', 'copy', video_input], check=True, stderr=subprocess.DEVNULL)

    if not os.path.isfile(video_input):
        raise FileNotFoundError(f"Vídeo de entrada no existe: {video_input}")

    id_list = [s.strip() for s in args.identity.split(",") if s.strip()]
    resolved_id_groups = [resolve_identity_paths(x) for x in id_list]
    num_total_refs = sum(len(g) for g in resolved_id_groups)
    print(f"[*] Roster de Escena fijado ({len(resolved_id_groups)} identidades, {num_total_refs} fotos fuente): {', '.join(id_list)}", flush=True)
    print(f"[*] Configuración V4 SOTA: Enhancer={args.enhancer} (w={args.enhance_weight}) | Mask={args.mask} | Blend={args.blend} | Lighting={args.lighting} | PreserveMouth={args.preserve_mouth} | PreserveEyes={args.preserve_eyes} | Stabilize={not args.no_stabilize_patch}", flush=True)

    output_path = args.output
    if not output_path:
        base_name = os.path.splitext(os.path.basename(video_input))[0]
        first_ref_name = os.path.splitext(os.path.basename(resolved_id_groups[0][0]))[0].replace("_real", "")
        output_path = os.path.join(os.getcwd(), f"{base_name}_{first_ref_name}_c5swap.mp4")

    audio_tmp = "/tmp/c5_audio_track.m4a"
    subprocess.run(['ffmpeg', '-y', '-i', video_input, '-vn', '-c:a', 'copy', audio_tmp], check=True, stderr=subprocess.DEVNULL)

    cap = cv2.VideoCapture(video_input)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    workers = max(1, min(args.workers, 4))
    print(f"[*] Vídeo: {width}x{height} @ {fps:.2f} FPS | Total: {total_frames} frames | Workers: {workers}", flush=True)

    print(f"[*] Compilando vectores latentes ArcFace y orientaciones 3D de las identidades fuente...", flush=True)
    app_rec = FaceAnalysis(name='buffalo_l', allowed_modules=['detection', 'recognition'], providers=['CPUExecutionProvider'])
    app_rec.prepare(ctx_id=0, det_size=(640, 640))
    fan_sess_prep = None
    if os.path.isfile(FAN_PATH) and estimate_dense_68_landmarks and estimate_head_pose_3d:
        fan_sess_prep = ort.InferenceSession(FAN_PATH, providers=['CPUExecutionProvider'])

    src_faces = []
    emb_dict = {}

    for i, p_list in enumerate(resolved_id_groups):
        embs = []
        angles = []
        for p in p_list:
            im = cv2.imread(p)
            f = app_rec.get(im) if im is not None else None
            if not f:
                img_raw = cv2.imread(p, cv2.IMREAD_UNCHANGED)
                if img_raw is not None:
                    if len(img_raw.shape) == 3 and img_raw.shape[2] == 4:
                        alpha = img_raw[:, :, 3] / 255.0
                        bgr = img_raw[:, :, :3]
                        white = (np.ones_like(bgr) * 255).astype(np.uint8)
                        im_prep = (bgr * alpha[:, :, None] + white * (1 - alpha[:, :, None])).astype(np.uint8)
                    else:
                        im_prep = img_raw
                    im_padded = cv2.copyMakeBorder(im_prep, 60, 60, 60, 60, cv2.BORDER_CONSTANT, value=[255, 255, 255])
                    f = app_rec.get(im_padded)
            if not f:
                raise ValueError(f"No face detected in source {p}")
            emb = f[0].embedding
            norm = emb / np.maximum(np.linalg.norm(emb), 1e-7)
            embs.append(emb)

            yaw_ref = 0.0
            if fan_sess_prep is not None:
                lm68_ref = estimate_dense_68_landmarks(f[0].kps, fan_sess_prep)
                if lm68_ref is not None:
                    _, yaw_ref, _ = estimate_head_pose_3d(lm68_ref, im.shape if im is not None else (512, 512, 3))
            angles.append((emb, norm, float(yaw_ref)))

        if len(embs) > 1 and compute_frechet_mean:
            fused_emb = compute_frechet_mean(embs)
            fused_norm = fused_emb / np.maximum(np.linalg.norm(fused_emb), 1e-7)
            src_f = MinimalSourceFace(fused_emb, fused_norm, angles=angles)
            angles_str = ", ".join([f"{a[2]:+.1f}°" for a in angles])
            print(f"  [+] Identidad {i} ('{id_list[i]}'): Fusión Fréchet de {len(embs)} referencias en S^511 (ángulos: [{angles_str}]).", flush=True)
        else:
            emb = embs[0]
            norm = emb / np.maximum(np.linalg.norm(emb), 1e-7)
            src_f = MinimalSourceFace(emb, norm, angles=angles)

        src_faces.append(src_f)
        emb_dict[f'emb_{i}'] = src_f.embedding
        emb_dict[f'norm_{i}'] = src_f.normed_embedding
        if src_f.angles:
            emb_dict[f'angles_embs_{i}'] = np.array([a[0] for a in src_f.angles], dtype=np.float32)
            emb_dict[f'angles_yaws_{i}'] = np.array([a[2] for a in src_f.angles], dtype=np.float32)

    np.savez_compressed(TEMP_EMBEDDINGS_PATH, **emb_dict)
    del app_rec
    if fan_sess_prep:
        del fan_sess_prep

    t0_all = time.time()

    if workers == 1:
        render_worker_chunk(
            video_path=video_input,
            source_faces=src_faces,
            start_frame=0,
            end_frame=total_frames,
            out_part_path="/tmp/c5_video_nosound.mp4",
            fps=fps,
            width=width,
            height=height,
            bitrate=args.bitrate,
            use_smooth=not args.no_smooth,
            enhancer=args.enhancer,
            enhance_weight=args.enhance_weight,
            mask_mode=args.mask,
            color_transfer=args.color_transfer,
            lighting=args.lighting,
            grain_strength=args.grain,
            preserve_mouth=args.preserve_mouth,
            preserve_eyes=args.preserve_eyes,
            blend_mode=args.blend,
            stabilize_patch=not args.no_stabilize_patch,
            target_face_index=args.target_face_index,
            swap_all=args.swap_all,
            worker_id=0
        )
        concat_video = "/tmp/c5_video_nosound.mp4"
    else:
        chunk_size = total_frames // workers
        subprocs = []
        part_files = []

        print(f"[*] Lanzando {workers} workers en paralelo en Apple Silicon...", flush=True)

        for w_idx in range(workers):
            sf = w_idx * chunk_size
            ef = total_frames if (w_idx == workers - 1) else (w_idx + 1) * chunk_size
            part_p = f"/tmp/c5_part_{w_idx}.mp4"
            part_files.append(part_p)

            cmd = [
                PYTHON_BIN, SCRIPT_PATH,
                "--video", video_input,
                "--identity", args.identity,
                "--worker-mode",
                "--start-frame", str(sf),
                "--end-frame", str(ef),
                "--part-output", part_p,
                "--worker-id", str(w_idx),
                "--bitrate", args.bitrate,
                "--enhancer", args.enhancer,
                "--enhance-weight", str(args.enhance_weight),
                "--grain", str(args.grain),
                "--mask", args.mask,
                "--blend", args.blend,
                "--color-transfer", args.color_transfer,
                "--lighting", args.lighting,
                "--preserve-mouth", args.preserve_mouth,
                "--preserve-eyes", args.preserve_eyes,
                "--target-face-index", str(args.target_face_index)
            ]
            if args.no_smooth: cmd.append("--no-smooth")
            if args.no_stabilize_patch: cmd.append("--no-stabilize-patch")
            if args.swap_all: cmd.append("--swap-all")

            p = subprocess.Popen(cmd)
            subprocs.append(p)
            if w_idx < workers - 1:
                time.sleep(2)

        for idx, p in enumerate(subprocs):
            ret = p.wait()
            if ret != 0:
                raise RuntimeError(f"Worker {idx} terminó con error (exit code {ret}).")

        concat_list = "/tmp/c5_concat_list.txt"
        with open(concat_list, "w") as fp:
            for pf in part_files:
                fp.write(f"file '{pf}'\n")

        concat_video = "/tmp/c5_merged_chunks.mp4"
        subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_list, '-c', 'copy', concat_video], check=True, stderr=subprocess.DEVNULL)

    print(f"[*] Muxing de pista sonora final -> {output_path}...", flush=True)
    subprocess.run([
        'ffmpeg', '-y',
        '-i', concat_video,
        '-i', audio_tmp,
        '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '192k',
        '-shortest',
        output_path
    ], check=True, stderr=subprocess.DEVNULL)

    purge_temp_onnx_artifacts()

    # Generación opcional de formato vertical 9:16 para Reels / TikTok / WhatsApp Status
    if getattr(args, 'format', 'original') in ['9:16', 'both']:
        base_no_ext, ext = os.path.splitext(output_path)
        out_916_path = f"{base_no_ext}_vertical_916{ext}"
        bg_mode = getattr(args, 'vertical_bg', 'crop')
        generate_vertical_916_video(output_path, out_916_path, bg_mode=bg_mode)
        if os.path.isdir(MOVIES_DIR):
            canon_916 = os.path.join(MOVIES_DIR, os.path.basename(out_916_path))
            if os.path.abspath(out_916_path) != os.path.abspath(canon_916):
                subprocess.run(['cp', '-f', out_916_path, canon_916], check=True)
                print(f"  -> Replicado vertical 9:16 en biblioteca canónica: {canon_916}", flush=True)

    total_time = time.time() - t0_all
    avg_fps = total_frames / total_time if total_time > 0 else 0
    print(f"\n[DONE] Render completado en {total_time:.1f}s ({total_time/60:.2f} min) | {avg_fps:.2f} FPS efectivos agregados", flush=True)
    print(f"  -> Archivo local: {output_path}", flush=True)

    if os.path.isdir(MOVIES_DIR):
        canon_path = os.path.join(MOVIES_DIR, os.path.basename(output_path))
        if os.path.abspath(output_path) != os.path.abspath(canon_path):
            subprocess.run(['cp', '-f', output_path, canon_path], check=True)
            print(f"  -> Replicado en biblioteca canónica: {canon_path}", flush=True)
        else:
            print(f"  -> Ya reside en la biblioteca canónica: {canon_path}", flush=True)

    return output_path

def main():
    parser = argparse.ArgumentParser(description="C5-REAL Sovereign Face Swap Engine V5 SOTA (Apple Silicon)")
    parser.add_argument("--video", "-v", default=None, help="Ruta al vídeo local o URL de Instagram/TikTok/YouTube")
    parser.add_argument("--identity", "-i", required=True, help="Lista de identidades separadas por comas (e.g. 'Alain,Luengo,Xabi' o compuestas 'mitxu_gafas+mitxu_real')")
    parser.add_argument("--output", "-o", default=None, help="Ruta de guardado para el vídeo final")
    parser.add_argument("--bitrate", "-b", default="8500k", help="Bitrate de codificación hardware VideoToolbox")
    parser.add_argument("--workers", "-w", type=int, default=2, help="Número de workers en paralelo (default 2)")
    parser.add_argument("--watch", default=None, help="Directorio inbox para modo Watcher Daemon reactivo")
    parser.add_argument("--no-smooth", action="store_true", help="Desactivar filtro temporal")

    # Flags V5 SOTA
    parser.add_argument("--enhancer", choices=['adaptive', 'unsharp', 'gpen', 'codeformer', 'gfpgan', 'none'], default='adaptive',
                        help="Motor de Super-Resolución / Restauración facial (default: adaptive - escala inteligente)")
    parser.add_argument("--enhance-weight", type=float, default=0.7,
                        help="Peso de fidelidad de restauración para CodeFormer [0.0-1.0] (default: 0.7)")
    parser.add_argument("--grain", type=float, default=0.5,
                        help="Intensidad de grano de sensor y ruido Poisson-Gaussian [0.0-1.0] (default: 0.5)")
    parser.add_argument("--mask", choices=['bisenet', 'ellipse'], default='bisenet',
                        help="Tipo de máscara de segmentación: 'bisenet' o 'ellipse' (default: bisenet)")
    parser.add_argument("--blend", choices=['two-band', 'linear', 'ellipse'], default='two-band',
                        help="Fusión espectral: 'two-band' (descomposición en frecuencia), 'linear' o 'ellipse' (default: two-band)")
    parser.add_argument("--color-transfer", choices=['mkl', 'reinhard', 'none'], default='mkl',
                        help="Transferencia cromática: 'mkl' (Optimal Transport) o 'reinhard' (default: mkl)")
    parser.add_argument("--lighting", choices=['spatial', 'mkl', 'reinhard', 'none'], default='spatial',
                        help="Transferencia de iluminación espacial 3D y sombras: 'spatial' (default), 'mkl', 'reinhard', 'none'")
    parser.add_argument("--preserve-mouth", choices=['auto', 'true', 'false'], default='auto',
                        help="Preservar cavidad bucal orgánica (dientes/lengua) para articulación fonética (default: auto)")
    parser.add_argument("--preserve-eyes", choices=['auto', 'gaze', 'true', 'false'], default='auto',
                        help="Preservar párpados orgánicos o mirada/iris vivos 'gaze' (default: auto)")
    parser.add_argument("--format", choices=['original', '9:16', 'both'], default='original',
                        help="Formato de exportación: 'original', '9:16' (Reel/TikTok/Short) o 'both' (default: original)")
    parser.add_argument("--vertical-bg", choices=['crop', 'blur'], default='crop',
                        help="Modo de encuadre vertical: 'crop' (tracking dinámico) o 'blur' (fondo desenfocado) (default: crop)")
    parser.add_argument("--no-stabilize-patch", action="store_true",
                        help="Desactivar estabilizador temporal inter-frame de parches faciales (anti-shimmer)")
    parser.add_argument("--target-face-index", type=int, default=0,
                        help="Índice del rostro objetivo por tamaño descendente (default: 0 = principal)")
    parser.add_argument("--swap-all", action="store_true",
                        help="Intercambiar todos los rostros detectados en la escena")

    # Flags internas para subprocesos worker
    parser.add_argument("--worker-mode", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--start-frame", type=int, default=0, help=argparse.SUPPRESS)
    parser.add_argument("--end-frame", type=int, default=0, help=argparse.SUPPRESS)
    parser.add_argument("--part-output", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--worker-id", type=int, default=0, help=argparse.SUPPRESS)
    args = parser.parse_args()

    # Si se invoca como worker interno
    if args.worker_mode:
        if not os.path.isfile(TEMP_EMBEDDINGS_PATH):
            raise FileNotFoundError(f"Embeddings temporales no encontrados: {TEMP_EMBEDDINGS_PATH}")
        npz = np.load(TEMP_EMBEDDINGS_PATH)
        num_faces = len([k for k in npz.files if k.startswith('emb_')])
        src_faces = []
        for i in range(num_faces):
            emb = npz[f'emb_{i}']
            norm = npz[f'norm_{i}']
            angles = []
            if f'angles_embs_{i}' in npz and f'angles_yaws_{i}' in npz:
                a_embs = npz[f'angles_embs_{i}']
                a_yaws = npz[f'angles_yaws_{i}']
                for j in range(len(a_yaws)):
                    e = a_embs[j]
                    n = e / np.maximum(np.linalg.norm(e), 1e-7)
                    angles.append((e, n, float(a_yaws[j])))
            src_faces.append(MinimalSourceFace(emb, norm, angles=angles))

        cap = cv2.VideoCapture(args.video)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        render_worker_chunk(
            video_path=args.video,
            source_faces=src_faces,
            start_frame=args.start_frame,
            end_frame=args.end_frame,
            out_part_path=args.part_output,
            fps=fps,
            width=width,
            height=height,
            bitrate=args.bitrate,
            use_smooth=not args.no_smooth,
            enhancer=args.enhancer,
            enhance_weight=args.enhance_weight,
            mask_mode=args.mask,
            color_transfer=args.color_transfer,
            lighting=args.lighting,
            grain_strength=args.grain,
            preserve_mouth=args.preserve_mouth,
            preserve_eyes=args.preserve_eyes,
            blend_mode=args.blend,
            stabilize_patch=not args.no_stabilize_patch,
            target_face_index=args.target_face_index,
            swap_all=args.swap_all,
            worker_id=args.worker_id
        )
        return

    # MODO WATCHER DAEMON
    if args.watch:
        inbox_dir = os.path.abspath(args.watch)
        os.makedirs(inbox_dir, exist_ok=True)
        processed_dir = os.path.join(inbox_dir, "processed")
        os.makedirs(processed_dir, exist_ok=True)
        print(f"[*] Modo Watcher Daemon Activo. Monitorizando: {inbox_dir}", flush=True)
        print(f"[*] Identidad(es) objetivo: {args.identity}", flush=True)
        try:
            while True:
                files = [os.path.join(inbox_dir, f) for f in os.listdir(inbox_dir)
                         if os.path.isfile(os.path.join(inbox_dir, f)) and not f.startswith('.')]
                for fpath in files:
                    ext = os.path.splitext(fpath)[1].lower()
                    if ext in ['.mp4', '.mov', '.mkv', '.webm', '.avi']:
                        s0 = os.path.getsize(fpath)
                        time.sleep(1)
                        if os.path.getsize(fpath) != s0:
                            continue
                        print(f"\n[+] Nuevo metraje detectado en inbox: {fpath}", flush=True)
                        dest_processed = os.path.join(processed_dir, os.path.basename(fpath))
                        process_video_pipeline(fpath, args)
                        shutil.move(fpath, dest_processed)
                        print(f"[✓] Archivo origen archivado en: {dest_processed}", flush=True)
                    elif ext in ['.txt', '.url']:
                        with open(fpath, 'r') as fp:
                            url = fp.read().strip()
                        if url.startswith('http://') or url.startswith('https://'):
                            print(f"\n[+] URL detectada en inbox: {url}", flush=True)
                            process_video_pipeline(url, args)
                            os.remove(fpath)
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n[*] Watcher Daemon detenido por el usuario.")
            return

    # MODO MONO-VÍDEO DIRECTO
    if not args.video:
        parser.error("Se requiere --video <ruta/url> o --watch <directorio>.")
    process_video_pipeline(args.video, args)

if __name__ == '__main__':
    main()
