---
name: c5-editorial-magazine-architect
display_name: Arquitecto de Diseño Editorial, Revistas y Presentaciones
description: Generación de documentos impresos/digitales con tipografía de revista, fotos full-bleed, maquetación periodística de doble columna y diapositivas editoriales PPTX/HTML. Dispara con "revista digital", "photo magazine", "journalistic portrait", "geo magazine slides", "diseño editorial", "maquetación html pptx".
role: arquitecto
allowed_roles:
- arquitecto
directives:
  worktree_mode: spec-only
  phase: design
  handoff:
    upstream: operador
    downstream: ejecutor
---

# Skill: C5 Editorial Magazine & Presentation Architect

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `arquitecto` (Arquitecto (Diseño Sistémico & Contratos de Invariantes))
> - **Modo de Acceso a Worktree:** `spec-only` (spec-only (Lectura profunda y modelado formal; emisión de especificaciones sin mutación de código de producción))
> - **Fase Causal:** `design`
> - **Contrato Handoff:** Recibe de `operador` $\to$ Despacha a `ejecutor`

Este protocolo crea publicaciones digitales, maquetas periodísticas de alta gama e informes editoriales caracterizados por tipografía refinada (Serif/Sans contrastadas), fotografía sangrada (*full-bleed*) y tarjetas de datos estructuradas.

---

## 1. Reglas de Diseño Editorial C5-REAL

1. **Jerarquía Tipográfica Dinámica:**
   - Titulares en tipografía Serif editorial o Display de alto contraste.
   - Cuerpo de texto en Sans-Serif geométrica con altura x legíble y *interlineado* ventilado ($1.5 - 1.6$).
2. **Distribución de Retícula (Grid System):**
   - Retícula editorial asimétrica de 12 columnas.
   - Soporte para doble columna estilo periodístico (*Southern People Weekly style*).
3. **Fotografía & Tarjetas de Datos:**
   - Fotografía a sangre (*full-bleed photography*) con filtros de tono sutil y sombreados de contraste.
   - Tarjetas destacan métricas con *glassmorphism* o fondos mates de alta exergía.

---

## 2. Salida HTML / PPTX

- **Revista Digital HTML:** Archivo autosuficiente con CSS responsivo, diseño *landscape* / *portrait*, capitulares (*drop caps*) y citas destacadas (*pull quotes*).
- **Decks PPTX:** Exportación mediante plantillas de maquetación geográfica/editorial (*Geo-Magazine*) para presentaciones de nivel directivo.
