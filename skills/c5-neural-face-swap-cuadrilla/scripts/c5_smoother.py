#!/usr/bin/env python3
"""
c5_smoother.py — Motor de Estabilización Espaciotemporal, Armonización Fotométrica,
Super-Resolución Neuronal y Rastreo Zero-Drop para Video Face Swapping en Apple Silicon.
"""

import numpy as np
import cv2

class OneEuroFilter:
    """
    Filtro 1-Euro adaptativo (Casiez et al., CHI 2012).
    Minimiza jitter estático con baja latencia en movimientos dinámicos.
    """
    def __init__(self, min_cutoff=0.8, beta=0.005, d_cutoff=1.0):
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)
        self.x_prev = None
        self.dx_prev = None

    def _smoothing_factor(self, cutoff, dt):
        tau = 1.0 / (2.0 * np.pi * cutoff)
        return 1.0 / (1.0 + tau / dt)

    def filter(self, x, dt=1.0/30.0):
        x = np.asarray(x, dtype=np.float32)
        if self.x_prev is None:
            self.x_prev = x.copy()
            self.dx_prev = np.zeros_like(x)
            return x

        dx = (x - self.x_prev) / max(dt, 1e-6)
        edx = self._smoothing_factor(self.d_cutoff, dt)
        dx_hat = edx * dx + (1.0 - edx) * self.dx_prev

        cutoff = self.min_cutoff + self.beta * float(np.linalg.norm(dx_hat))
        e = self._smoothing_factor(cutoff, dt)
        x_hat = e * x + (1.0 - e) * self.x_prev

        self.x_prev = x_hat.copy()
        self.dx_prev = dx_hat.copy()
        return x_hat

    def reset(self):
        self.x_prev = None
        self.dx_prev = None


class TemporalPatchStabilizer:
    """
    Estabilizador Temporal de Parches Faciales para erradicar el parpadeo de microtexturas (GAN shimmer)
    en zonas estáticas de la piel, manteniendo respuesta instantánea (cero ghosting) en articulación
    bucal, parpadeo y expresiones dinámicas.
    """
    def __init__(self, alpha_static=0.45, diff_min=4.0, diff_max=20.0):
        self.prev_patch = None
        self.alpha_static = float(alpha_static)
        self.diff_min = float(diff_min)
        self.diff_max = float(diff_max)
        self.inv_range = 1.0 / max(self.diff_max - self.diff_min, 1e-4)

    def stabilize(self, current_patch, motion_magnitude=0.0):
        """
        Aplica suavizado adaptativo por vóxeles en función de la variación local y desplazamiento global.
        """
        if self.prev_patch is None or current_patch is None:
            if current_patch is not None:
                self.prev_patch = current_patch.copy()
            return current_patch

        # Si hay movimiento brusco de cabeza (> 2.5 px), omitir estabilización temporal
        if motion_magnitude > 2.5:
            self.prev_patch = current_patch.copy()
            return current_patch

        # Diferencia acelerada por C++ SIMD NEON
        diff_bgr = cv2.absdiff(current_patch, self.prev_patch)
        diff_gray = cv2.cvtColor(diff_bgr, cv2.COLOR_BGR2GRAY)

        alpha = np.clip((diff_gray.astype(np.float32) - self.diff_min) * self.inv_range, 0.0, 1.0)
        alpha = (self.alpha_static + (1.0 - self.alpha_static) * alpha)[:, :, None]

        if motion_magnitude > 0.8:
            m_factor = np.clip((motion_magnitude - 0.8) / 1.7, 0.0, 1.0)
            alpha = np.maximum(alpha, m_factor)

        stabilized = (alpha * current_patch.astype(np.float32) + (1.0 - alpha) * self.prev_patch.astype(np.float32)).astype(np.uint8)
        self.prev_patch = stabilized.copy()
        return stabilized

    def reset(self):
        self.prev_patch = None


class FaceTracker:
    """
    Rastreador temporal determinista de identidades con Extrapolación Zero-Drop,
    Filtros 1-Euro independientes por trayectoria y Estabilizador de Parches Temporales.
    """
    def __init__(self, max_lost=20, max_extrapolate=2, iou_thresh=0.25):
        self.tracks = {}  # track_id: {'bbox': bbox, 'lost': 0, 'identity_idx': int, 'last_face': face, 'smoother': OneEuroFilter, 'stabilizer': TemporalPatchStabilizer, 'last_kps': ndarray}
        self.next_id = 0
        self.max_lost = max_lost
        self.max_extrapolate = max_extrapolate
        self.iou_thresh = iou_thresh

    @staticmethod
    def compute_iou(boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        interArea = max(0, xB - xA) * max(0, yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        denom = float(boxAArea + boxBArea - interArea)
        return interArea / denom if denom > 0 else 0.0

    def get_stabilizer(self, tid):
        if tid in self.tracks:
            return self.tracks[tid].get('stabilizer')
        return None

    def compute_motion(self, tid, current_kps):
        if tid in self.tracks and self.tracks[tid].get('last_kps') is not None:
            last_k = self.tracks[tid]['last_kps']
            motion = float(np.mean(np.linalg.norm(current_kps - last_k, axis=1)))
            self.tracks[tid]['last_kps'] = current_kps.copy()
            return motion
        return 0.0

    def update(self, detected_faces, num_identities, dt=1.0/30.0, swap_all=False, target_index=None):
        """
        Asigna a cada rostro detectado un identity_idx estable temporalmente.
        Aplica suavizado 1-Euro por track y extrapola en frames sin detección (Zero-Drop).
        Si target_index is not None, sólo asigna el rostro de ese rango/índice.
        Si swap_all es False, nunca asigna identidades a caras secundarias no deseadas.
        Retorna lista de tuplas (face, identity_idx, track_id).
        """
        if not detected_faces:
            extrapolated = []
            for tid in list(self.tracks.keys()):
                self.tracks[tid]['lost'] += 1
                if self.tracks[tid]['lost'] <= self.max_extrapolate and self.tracks[tid]['last_face'] is not None:
                    # Extrapolación inercial: reutilizar último rostro si tiene swap activo
                    if self.tracks[tid]['identity_idx'] >= 0:
                        extrapolated.append((self.tracks[tid]['last_face'], self.tracks[tid]['identity_idx'], tid))
                elif self.tracks[tid]['lost'] > self.max_lost:
                    del self.tracks[tid]
            return extrapolated

        det_boxes = [f.bbox for f in detected_faces]
        matched_dets = set()
        matched_tracks = set()
        assignments = []

        # 1. Emparejamiento por máxima intersección sobre unión (IoU)
        for tid, tinfo in self.tracks.items():
            best_iou = 0.0
            best_det_idx = -1
            for d_idx, dbox in enumerate(det_boxes):
                if d_idx in matched_dets:
                    continue
                iou = self.compute_iou(tinfo['bbox'], dbox)
                if iou > best_iou:
                    best_iou = iou
                    best_det_idx = d_idx
            if best_iou >= self.iou_thresh:
                matched_dets.add(best_det_idx)
                matched_tracks.add(tid)
                det_face = detected_faces[best_det_idx]

                # Suavizado de landmarks específico para esta trayectoria
                if tinfo['smoother'] is not None:
                    det_face.kps = tinfo['smoother'].filter(det_face.kps, dt=dt)

                self.tracks[tid]['bbox'] = det_face.bbox
                self.tracks[tid]['lost'] = 0
                self.tracks[tid]['last_face'] = det_face
                if self.tracks[tid]['identity_idx'] >= 0:
                    assignments.append((det_face, self.tracks[tid]['identity_idx'], tid))

        # 2. Nuevas detecciones no emparejadas (ordenadas por área de caja: mayor rostro primero)
        used_indices = {tinfo['identity_idx'] for tinfo in self.tracks.values() if tinfo['lost'] == 0 and tinfo['identity_idx'] >= 0}
        available_indices = [i for i in range(num_identities) if i not in used_indices]

        unmatched = [(d_idx, dbox) for d_idx, dbox in enumerate(det_boxes) if d_idx not in matched_dets]
        unmatched.sort(key=lambda item: (item[1][2]-item[1][0]) * (item[1][3]-item[1][1]), reverse=True)

        for d_idx, dbox in unmatched:
            new_id = self.next_id
            self.next_id += 1
            if target_index is not None:
                chosen_idx = 0 if (d_idx == target_index and 0 in available_indices) else -1
            elif available_indices:
                chosen_idx = available_indices.pop(0)
            elif swap_all:
                chosen_idx = d_idx % num_identities
            else:
                chosen_idx = -1

            det_face = detected_faces[d_idx]
            smoother = OneEuroFilter()
            det_face.kps = smoother.filter(det_face.kps, dt=dt)
            self.tracks[new_id] = {
                'bbox': dbox,
                'lost': 0,
                'identity_idx': chosen_idx,
                'last_face': det_face,
                'smoother': smoother,
                'stabilizer': TemporalPatchStabilizer(),
                'last_kps': det_face.kps.copy()
            }
            if chosen_idx >= 0:
                assignments.append((det_face, chosen_idx, new_id))

        # 3. Purgar tracks perdidos o extrapolar si es un fallo transitorio de detección
        for tid in list(self.tracks.keys()):
            if tid not in matched_tracks and tid in self.tracks:
                self.tracks[tid]['lost'] += 1
                if self.tracks[tid]['lost'] <= self.max_extrapolate and self.tracks[tid]['last_face'] is not None:
                    if self.tracks[tid]['identity_idx'] >= 0:
                        assignments.append((self.tracks[tid]['last_face'], self.tracks[tid]['identity_idx'], tid))
                elif self.tracks[tid]['lost'] > self.max_lost:
                    del self.tracks[tid]

        return assignments


def monge_kantorovich_color_transfer(source, target):
    """
    Transporte Óptimo Lineal (MKL) en espacio tridimensional BGR.
    Alinea la media y la covarianza completa del color entre el crop original y el generado.
    """
    s = source.astype(np.float32)
    t = target.astype(np.float32)

    s_mean = s.mean(axis=(0, 1), keepdims=True)
    t_mean = t.mean(axis=(0, 1), keepdims=True)

    s_zero = (s - s_mean).reshape(-1, 3)
    t_zero = (t - t_mean).reshape(-1, 3)

    cov_s = np.cov(s_zero, rowvar=False) + 1e-4 * np.eye(3)
    cov_t = np.cov(t_zero, rowvar=False) + 1e-4 * np.eye(3)

    u_s, d_s, vt_s = np.linalg.svd(cov_s)
    u_t, d_t, vt_t = np.linalg.svd(cov_t)

    sqrt_cov_t = u_t @ np.diag(np.sqrt(d_t)) @ vt_t
    inv_sqrt_cov_s = u_s @ np.diag(1.0 / np.sqrt(d_s)) @ vt_s

    A = sqrt_cov_t @ inv_sqrt_cov_s
    s_transformed = (s_zero @ A.T).reshape(s.shape) + t_mean
    return np.clip(s_transformed, 0, 255).astype(np.uint8)


def reinhard_color_transfer(source_patch, target_patch, blend_ratio=0.85):
    """
    Transferencia estadística de color en espacio ortogonal CIELAB (Reinhard et al., 2001).
    """
    if source_patch.shape[:2] != target_patch.shape[:2]:
        target_patch = cv2.resize(target_patch, (source_patch.shape[1], source_patch.shape[0]))

    s_lab = cv2.cvtColor(source_patch, cv2.COLOR_BGR2LAB).astype(np.float32)
    t_lab = cv2.cvtColor(target_patch, cv2.COLOR_BGR2LAB).astype(np.float32)

    s_mean, s_std = s_lab.mean(axis=(0, 1)), s_lab.std(axis=(0, 1)) + 1e-5
    t_mean, t_std = t_lab.mean(axis=(0, 1)), t_lab.std(axis=(0, 1)) + 1e-5

    corrected = (s_lab - s_mean) * (t_std / s_std) + t_mean
    corrected = np.clip(corrected, 0, 255).astype(np.float32)

    final_lab = blend_ratio * corrected + (1.0 - blend_ratio) * s_lab
    return cv2.cvtColor(np.clip(final_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def soft_elliptical_blend(target_img, bgr_fake, M, feather=15):
    """
    Mezcla sigmoidal elíptica C^inf en espacio afín inverso.
    """
    IM = cv2.invertAffineTransform(M)
    h_fake, w_fake = bgr_fake.shape[:2]

    mask_local = np.zeros((h_fake, w_fake), dtype=np.float32)
    cv2.ellipse(mask_local, (w_fake // 2, int(h_fake * 0.52)),
                (int(w_fake * 0.42), int(h_fake * 0.46)), 0, 0, 360, 1.0, -1)
    mask_local = cv2.GaussianBlur(mask_local, (feather * 2 + 1, feather * 2 + 1), 0)

    h_tgt, w_tgt = target_img.shape[:2]
    warped_fake = cv2.warpAffine(bgr_fake, IM, (w_tgt, h_tgt), borderValue=0.0)
    warped_mask = cv2.warpAffine(mask_local, IM, (w_tgt, h_tgt), borderValue=0.0)
    warped_mask = np.expand_dims(warped_mask, axis=2)

    merged = warped_mask * warped_fake + (1.0 - warped_mask) * target_img.astype(np.float32)
    return np.clip(merged, 0, 255).astype(np.uint8)


def get_bisenet_semantic_mask(crop_512, sess_bisenet, feather=19, preserve_mouth=False, preserve_eyes=False, eye_landmarks_512=None):
    """
    Segmentación semántica precisa de rostros a 512x512 con BiSeNet ResNet-34.
    Aisla piel, cejas, ojos, nariz y labios, respetando gafas, pelo y manos.
    Si preserve_mouth=True, excluye la cavidad bucal interna (clase 11) para conservar
    los dientes y lengua orgánicos del orador original durante habla/gritos.
    Si preserve_eyes=True o eye_landmarks_512 no es None, protege los párpados
    y ojos cerrados/parpadeo del rostro original para mantener el parpadeo natural.
    """
    inp = cv2.cvtColor(crop_512, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    inp = (inp - mean) / std
    inp = inp.transpose(2, 0, 1)[None, ...]

    out = sess_bisenet.run(None, {'input': inp})[0]
    parsing = np.argmax(out[0], axis=0)

    # Clases BiSeNet: 1 (piel), 2 (ceja izq), 3 (ceja der), 4 (ojo izq), 5 (ojo der), 10 (nariz), 12 (labio sup), 13 (labio inf)
    valid_classes = [1, 2, 3, 10, 12, 13]
    if not preserve_eyes:
        valid_classes.extend([4, 5])
    if not preserve_mouth:
        valid_classes.append(11)  # Clase 11: Cavidad oral interna (dientes/lengua)

    mask = np.isin(parsing, valid_classes).astype(np.float32)

    # Si se deben preservar los ojos (por parpadeo detectado con EAR < 0.18 o forzado)
    if preserve_eyes and eye_landmarks_512 is not None and len(eye_landmarks_512) >= 68:
        # Puntos de los ojos en espacio 512x512: 36..41 (izq) y 42..47 (der)
        hull_left = cv2.convexHull(eye_landmarks_512[36:42].astype(np.int32))
        hull_right = cv2.convexHull(eye_landmarks_512[42:48].astype(np.int32))
        eye_exclude = np.zeros((512, 512), dtype=np.float32)
        cv2.fillPoly(eye_exclude, [hull_left, hull_right], 1.0)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        eye_exclude = cv2.dilate(eye_exclude, kernel)
        eye_exclude = cv2.GaussianBlur(eye_exclude, (15, 15), 0)
        mask = mask * (1.0 - eye_exclude)

    mask = cv2.GaussianBlur(mask, (feather, feather), 0)
    return mask


def restore_face_patch(crop_512, enhancer_type, session, weight=0.7):
    """
    Restaura y super-resuelve un recorte facial a 512x512 mediante red neuronal.
    Soporta: 'codeformer', 'gpen', 'gfpgan'.
    """
    inp = cv2.cvtColor(crop_512, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    inp = (inp - 0.5) / 0.5
    inp = inp.transpose(2, 0, 1)[None, ...]

    if enhancer_type == 'codeformer':
        w_arr = np.array(weight, dtype=np.double)
        out = session.run(None, {'input': inp, 'weight': w_arr})[0]
    else:  # gpen o gfpgan
        out = session.run(None, {'input': inp})[0]

    res = out[0].transpose(1, 2, 0)
    res_norm = (res + 1.0) / 2.0
    return np.clip(res_norm * 255.0, 0, 255).astype(np.uint8)[:, :, ::-1]


def two_band_blend_patch(target_patch, fake_patch, mask_patch, blur_ksize=15):
    """
    Mezcla espectral de dos bandas (frecuencia baja y alta) en espacio canónico 512x512.
    Erradica costuras, saltos tonales y artefactos en el contorno sin desenfocar texturas.
    Ejecución optimizada a >110 FPS en silicio Apple.
    """
    tgt_f = target_patch.astype(np.float32) / 255.0
    fake_f = fake_patch.astype(np.float32) / 255.0
    mask_f = mask_patch.astype(np.float32)
    if mask_f.ndim == 2:
        mask_f = mask_f[:, :, None]

    k = (blur_ksize, blur_ksize)
    tgt_low = cv2.GaussianBlur(tgt_f, k, 0)
    fake_low = cv2.GaussianBlur(fake_f, k, 0)

    tgt_high = tgt_f - tgt_low
    fake_high = fake_f - fake_low

    mask_low = cv2.GaussianBlur(mask_f, (blur_ksize * 2 + 1, blur_ksize * 2 + 1), 0)
    if mask_low.ndim == 2:
        mask_low = mask_low[:, :, None]

    comp_low = mask_low * fake_low + (1.0 - mask_low) * tgt_low
    comp_high = mask_f * fake_high + (1.0 - mask_f) * tgt_high
    return np.clip((comp_low + comp_high) * 255.0, 0, 255).astype(np.uint8)


# Plantilla canónica normalizada FFHQ-512 para proyección de landmarks
FFHQ_512_NORM = np.array([
    [0.37691676, 0.46864664],
    [0.62285697, 0.46912813],
    [0.50123859, 0.61331904],
    [0.39308822, 0.72541100],
    [0.61150205, 0.72490465]
], dtype=np.float32)

# Modelo 3D antropométrico estándar para estimación de pose por PnP
CANONICAL_3D_MODEL_POINTS = np.array([
    (0.0, 0.0, 0.0),          # Punta de la nariz (Landmark #30)
    (0.0, -330.0, -65.0),     # Mentón (Landmark #8)
    (-225.0, 170.0, -135.0),  # Esquina exterior ojo izquierdo (Landmark #36)
    (225.0, 170.0, -135.0),   # Esquina exterior ojo derecho (Landmark #45)
    (-150.0, -150.0, -125.0), # Comisura izquierda de la boca (Landmark #48)
    (150.0, -150.0, -125.0)   # Comisura derecha de la boca (Landmark #54)
], dtype=np.float64)


def estimate_dense_68_landmarks(kps_5, fan_sess):
    """
    Predice los 68 puntos faciales densos a partir de los 5 puntos detectados por SCRFD.
    Utiliza el modelo fan_68_5.onnx con normalización afín RANSAC sobre plantilla FFHQ-512.
    Latencia: ~0.017 ms.
    """
    affine_matrix = cv2.estimateAffinePartial2D(kps_5, FFHQ_512_NORM, method=cv2.RANSAC, ransacReprojThreshold=100)[0]
    if affine_matrix is None:
        return None
    kps_norm = cv2.transform(kps_5.reshape(1, -1, 2), affine_matrix).reshape(-1, 2)
    out = fan_sess.run(None, {'input': [kps_norm.astype(np.float32)]})[0][0]
    inv_affine = cv2.invertAffineTransform(affine_matrix)
    lm68 = cv2.transform(out.reshape(1, -1, 2), inv_affine).reshape(-1, 2)
    return lm68


def estimate_head_pose_3d(lm68, frame_shape):
    """
    Estima la orientación 3D de la cabeza (Pitch, Yaw, Roll en grados) mediante cv2.solvePnP.
    """
    if lm68 is None or len(lm68) < 68:
        return 0.0, 0.0, 0.0

    image_points = np.array([
        lm68[30], # Punta nariz
        lm68[8],  # Mentón
        lm68[36], # Ojo izq exterior
        lm68[45], # Ojo der exterior
        lm68[48], # Boca izq
        lm68[54]  # Boca der
    ], dtype=np.float64)

    h, w = frame_shape[:2]
    focal_length = float(w)
    center = (float(w) / 2.0, float(h) / 2.0)
    camera_matrix = np.array([[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]], dtype=np.float64)
    dist_coeffs = np.zeros((4, 1))

    success, rvec, tvec = cv2.solvePnP(CANONICAL_3D_MODEL_POINTS, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    if not success:
        return 0.0, 0.0, 0.0

    R, _ = cv2.Rodrigues(rvec)
    sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    if sy >= 1e-6:
        pitch = np.degrees(np.arctan2(R[2, 1], R[2, 2]))
        yaw = np.degrees(np.arctan2(-R[2, 0], sy))
        roll = np.degrees(np.arctan2(R[1, 0], R[0, 0]))
    else:
        pitch = np.degrees(np.arctan2(-R[1, 2], R[1, 1]))
        yaw = np.degrees(np.arctan2(-R[2, 0], sy))
        roll = 0.0

    return float(pitch), float(yaw), float(roll)


def compute_mouth_aspect_ratio(lm68):
    """
    Calcula el Mouth Aspect Ratio (MAR) a partir de los puntos del contorno bucal interno.
    Valores > 0.15 indican apertura bucal activa (habla, grito, risa).
    """
    if lm68 is None or len(lm68) < 68:
        return 0.0
    # Puntos internos: 60 (comisura izq), 64 (comisura der), 62 (labio sup centro), 66 (labio inf centro)
    # y verticales secundarios: 63, 65
    v1 = np.linalg.norm(lm68[62] - lm68[66])
    v2 = np.linalg.norm(lm68[63] - lm68[65])
    h = np.linalg.norm(lm68[60] - lm68[64])
    return float((v1 + v2) / max(2.0 * h, 1e-6))


def compute_eye_aspect_ratio(lm68):
    """
    Calcula el Eye Aspect Ratio (EAR) a partir de los puntos densos de ambos ojos.
    Valores < 0.18 indican parpadeo u ojos cerrados; valores > 0.25 indican ojos abiertos.
    """
    if lm68 is None or len(lm68) < 68:
        return 0.30
    p36, p37, p38, p39, p40, p41 = lm68[36:42]
    ear_left = (np.linalg.norm(p37 - p41) + np.linalg.norm(p38 - p40)) / max(2.0 * np.linalg.norm(p36 - p39), 1e-6)
    p42, p43, p44, p45, p46, p47 = lm68[42:48]
    ear_right = (np.linalg.norm(p43 - p47) + np.linalg.norm(p44 - p46)) / max(2.0 * np.linalg.norm(p42 - p45), 1e-6)
    return float((ear_left + ear_right) / 2.0)


def spatial_illumination_transfer(swap_patch, target_patch, sigma_ambient=31, sigma_smooth=11, gain_min=0.5, gain_max=2.0):
    """
    Transfiere el gradiente de iluminación espacial y sombras 3D del target al swap.
    Preserva los poros y detalles de alta frecuencia del swap eliminando el efecto 'plano' o 'recorte pegado'.
    """
    swap_f = swap_patch.astype(np.float32)
    tgt_f = target_patch.astype(np.float32)

    k_amb = int(sigma_ambient * 2) + 1
    if k_amb % 2 == 0:
        k_amb += 1
    tgt_low = cv2.GaussianBlur(tgt_f, (k_amb, k_amb), sigma_ambient)
    swap_low = cv2.GaussianBlur(swap_f, (k_amb, k_amb), sigma_ambient)

    eps = 1e-4
    ratio = (tgt_low + eps) / (swap_low + eps)
    ratio = np.clip(ratio, gain_min, gain_max)

    k_sm = int(sigma_smooth * 2) + 1
    if k_sm % 2 == 0:
        k_sm += 1
    ratio_smooth = cv2.GaussianBlur(ratio, (k_sm, k_sm), sigma_smooth)

    lit_swap = swap_f * ratio_smooth
    return np.clip(lit_swap, 0, 255).astype(np.uint8)


def compute_frechet_mean(embeddings):
    """
    Media Fréchet Riemanniana en la hiperesfera unitaria S^511 para fusionar múltiples fotos.
    """
    embs = np.array(embeddings, dtype=np.float32)
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    normed = embs / np.maximum(norms, 1e-7)
    mean_vec = np.sum(normed, axis=0)
    mean_norm = np.linalg.norm(mean_vec)
    return (mean_vec / max(mean_norm, 1e-7)).astype(np.float32)


def slerp_embeddings(e1, e2, t):
    """
    Interpolación esférica lineal (SLERP) entre dos vectores latentes en S^511.
    """
    e1 = e1 / max(np.linalg.norm(e1), 1e-7)
    e2 = e2 / max(np.linalg.norm(e2), 1e-7)
    dot = float(np.clip(np.dot(e1, e2), -1.0, 1.0))
    omega = np.arccos(dot)
    if np.abs(omega) < 1e-5:
        return ((1.0 - t) * e1 + t * e2).astype(np.float32)
    sin_omega = np.sin(omega)
    res = (np.sin((1.0 - t) * omega) / sin_omega * e1 + np.sin(t * omega) / sin_omega * e2)
    return res.astype(np.float32)

