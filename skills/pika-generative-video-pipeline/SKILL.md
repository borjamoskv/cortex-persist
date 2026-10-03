---
name: pika-generative-video-pipeline
display_name: Pipeline de Generación y Control Parámetrico en Pika Art (A/V)
description: Generación de vídeo e integración de audio en Pika Art con control de física (-motion, -fps), Pikaffects y Pika Audio Models. Dispara con "pika art", "pika tutorial", "pika camera", "pikaffects", "pika prompt", "generación vídeo pika", "pikaffects sota".
role: ejecutor
allowed_roles:
- ejecutor
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# Pika Art Generative Video & Audio Pipeline

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

Esta habilidad proporciona las directrices y el cheatsheet determinista para la generación cinematográfica en Pika Art (1.0, 1.5, 2.0+) y su suite de audio.

## 🎯 Criterios de Activación
- Palabras clave / Intenciones: "pika art", "pika labs", "pika tutorial", "pikaffects", "pika camera", "pika audio", "pika prompt".

---

## 🛠️ Cheatsheet de Parámetros

### 📹 Control de Cámara (`-camera`)
- **Zoom:** `-camera zoom in` / `-camera zoom out`
- **Panorámica:** `-camera pan left` / `right` / `up` / `down`
- **Rotación:** `-camera rotate cw` / `ccw`
- *Nota:* Se pueden combinar vectores de cámara (ej. `-camera pan up right zoom in`).

### ⚙️ Parámetros de Calidad y Dinámica
- `-motion 1-4`: Intensidad de movimiento (1 = sutil/cinemático, 4 = caótico/FX).
- `-fps 8-24`: Tasa de refresco (24 = fluido, 12/8 = stop-motion/anime).
- `-gs 8-24`: Adherencia al prompt (Guidance Scale, default: 12).
- `-neg "..."`: Prompt negativo.
- `-ar [ratio]`: Relación de aspecto (16:9, 9:16, 1:1, 4:5).

---

## 🎨 Fórmula de Prompting en 4 Capas

$$\text{Prompt} = \text{[Sujeto + Acción Dinámica]} + \text{[Entorno + Iluminación]} + \text{[Lente + Estilo Fílmico]} + \text{[Flags]}$$

*Ejemplo:*
`Cyberpunk female android turning her head, eyes glowing cyan, standing in neon-drenched rain street, anamorphic lens 35mm, volumetric fog, cinematic lighting -camera zoom in -motion 2 -fps 24 -gs 14 -neg "ugly, cartoon, low quality"`

---

## 💥 Deformaciones Físicas (*Pikaffects*)
1. `Melt`: Derretimiento en fluido viscoso.
2. `Inflate`: Inflado de globo previo a colapso.
3. `Squish`: Aplastamiento vertical.
4. `Crush`: Compresión multidireccional.
5. `Explode`: Desintegración en partículas.
6. `Cakeify`: Revelado interior de textura de pastel.

---

## 🎵 Pika Audio Models Suite
1. **Pika Soundtrack:** Banda sonora cinemática coordinada con el movimiento.
2. **Pika Music:** Producción de canciones completas (voz + instrumental).
3. **Pika SFX:** Efectos de sonido Foley diegéticos.
4. **Pika Speech:** Clonación de voz y doblaje.

---

## 💻 Integración con CLI Soberano Local
Calcular directamente la fricción de créditos y validar la sintaxis de corchetes `[...]` mediante estimación analítica determinista:
```bash
# Cálculo inline de fricción de créditos Pika:
python3 -c 'import sys; d=float(sys.argv[1]); n=int(sys.argv[2]); print(f"Créditos estimados: {d * 2.5 * n:.1f}")' <duración_segundos> <iterations>
```
