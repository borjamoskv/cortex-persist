---
name: c5-poster-and-sign-craft
display_name: Pipeline de Remasterización Gráfica, Rotulación en Perspectiva y Filtrado Analógico
description: Protocolo de alta precisión para remasterización de cartelería e ilustración 4K, rotulación tipográfica en perspectiva (sign painting) con eliminación limpia de caracteres previos, preservación de jerarquía óptica (líquidos/vidrios en primer plano) y filtrado de imprenta analógica / vintage cómic de bajo contraste. Dispara con "remasterizar cartel", "rotular letrero", "cambiar texto cartel", "sign craft", "filtro vintage comic", "bajar contraste imagen", "quitar contraste duro", "poster remaster".
role: ejecutor
allowed_roles:
- ejecutor
- arquitecto
directives:
  worktree_mode: read-write
  phase: implementation
  handoff:
    upstream: arquitecto
    downstream: auditor
---

# Pipeline de Remasterización Gráfica, Rotulación en Perspectiva y Filtrado Analógico

Este skill formaliza el procedimiento determinista en silicio local (OpenCV, PIL, AppKit) para la restauración y modificación de carteles, portadas e ilustraciones de alta resolución.

---

## 1. Rotulación Tipográfica en Perspectiva («Sign Craft»)

### A. Rectificación a Espacio Plano 2D
1. Localizar los 4 vértices del panel interior de la señalización, **excluyendo estrictamente las molduras exteriores o vigas del marco**:
   $$P_{\text{src}} = \begin{pmatrix} x_{TL} & y_{TL} \\ x_{TR} & y_{TR} \\ x_{BR} & y_{BR} \\ x_{BL} & y_{BL} \end{pmatrix}$$
2. Calcular la matriz de perspectiva $M$ hacia un canvas plano normalizado ($W \times H$) y su inversa $M^{-1}$ con `cv2.getPerspectiveTransform`.

### B. Erradicación Atómica de Textos Previos (Anti-Fantasmas)
* **Veto:** Prohibido usar umbrales simples de brillo (`gray > 85`). Dejan intactas las sombras talladas, biseles y rebordes oscuros, provocando que el texto previo reaparezca como un fantasma sucio.
* **Protocolo:**
  1. Inpainting preventivo profundo sobre la máscara dilatada del área de caracteres originales.
  2. O síntesis de soporte limpio: muestreo paramétrico de las vetas de madera/textura en zonas libres, generando un fondo limpio con gradiente lumínico ambiental adaptativo.

### C. Tipografía Artesanal de Época
* **Selección de Fuente:** Descartar fuentes digitales genéricas (Arial, Times). Emplear familias de tipo de madera / rótulo tradicional (`SuperClarendon`, `Rockwell`, `Cooper Black`).
* **Proporción y Condensación:** Aplicar escala horizontal ($0.75 - 0.78\times$) para emular los tipos móviles condensados de imprenta del siglo XIX/XX.
* **Estratificación 3D en Capas:**
  1. *Filete de tinta (Ink Outline):* Trazo perimetral oscuro de 1-2 px que integra la tipografía con el dibujo.
  2. *Sombra tallada (Carved Drop Shadow):* Desplazamiento oblicuo (+3 px, +4 px) en umber oscuro/negro madera (`#100A06`).
  3. *Cuerpo principal:* Marfil/ocre añejo (`#F0E1C3`) con degradado cálido hacia la base.
  4. *Realce superior (Chisel Highlight):* Filete sutil (-1 px, -1 px) en blanco hueso cálido (`#FFF8E8`).

### D. Fusión por Gradientes de Poisson
* Deformar el panel terminado con $M^{-1}$ hacia la perspectiva original (`cv2.INTER_LANCZOS4`).
* Integrar mediante `cv2.seamlessClone` en modo `NORMAL_CLONE` sobre el soporte limpio, absorbiendo automáticamente la temperatura de color y la iluminación ambiental sin costuras perimetrales.

### E. Jerarquía Óptica de Primer Plano (Oclusiones, Líquidos y Vidrio)
* Si un elemento en primer plano (copa, vaso, rama, personaje) cruza el rótulo:
  1. **Segmentación Curvilínea:** Prohibido truncar con líneas rectas de coordenadas fijas (`y < N`). Trazar la curvatura física del objeto mediante polígono suave o detección de contorno.
  2. **Física de Absorción (Ley de Beer-Lambert):** Los líquidos transparentes (vino tinto, cerveza) operan como filtro multiplicativo: el texto subyacente debe teñirse del color del líquido, mientras que los reflejos especulares blancos del cristal y los bordes oscuros del vidrio se componen en capa superior con opacidad total.

---

## 2. Filtrado Analógico Vintage Comic / Anti-Contraste Duro

### Diagnóstico de "Mucho Contraste"
El contraste digital excesivo se produce al clipear negros a 0, blancos a 255 y aplicar sharpening indiscriminado, provocando desconexión visual entre caras fotográficas integradas y el entintado original.

### Pipeline de Calibración Tonal de Imprenta Litográfica (Ligne Claire)

```python
# 1. Entrada normalizada en float32 [0.0, 1.0]
img_f = img.astype(np.float32) / 255.0

# 2. Descompresión de medios tonos con gamma suave
toned = np.power(img_f, 0.955)

# 3. Compresión de Rango Dinámico (Matte Black Lift & Rag Paper Softening)
# Sombras elevadas a negro de tinta mate (8.2% = RGB ~21)
# Altas luces suavizadas a papel de grabado/algodón (92.8% = RGB ~236)
toned = 0.082 + (0.928 - 0.082) * toned

# 4. Calibración de Color de Papel Cálido de Autor
toned[:, :, 0] = toned[:, :, 0] * 0.965 + 0.022  # Azul suavizado
toned[:, :, 1] = toned[:, :, 1] * 0.985 + 0.016  # Verde neutro
toned[:, :, 2] = toned[:, :, 2] * 1.015 + 0.012  # Rojo cálido aterciopelado

# 5. Micro-Textura de Papel y Grano Fino (Agente Unificador)
# Convolución gaussiana de ruido blanco para emular grano litográfico
grain = cv2.GaussianBlur(np.random.normal(0, 0.011, toned.shape).astype(np.float32), (3, 3), 0)
final_bgr = np.clip(toned + grain, 0.0, 1.0)
```

---

## 3. Protocolo de Entrega Master
1. **Doble Formato 300 DPI:**
   - JPEG Master (`Q=98`, `subsampling=0`, `dpi=(300, 300)`).
   - PNG Master (Lossless, optimizado, `dpi=(300, 300)`).
2. **Inyección en Portapapeles macOS (`NSPasteboard`):** Copiar automáticamente la imagen al portapapeles para pegado instantáneo con `Cmd + V`.
