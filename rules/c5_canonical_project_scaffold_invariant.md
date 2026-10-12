---
name: c5_canonical_project_scaffold_invariant
description: Invariante obligatoria para la creación de nuevos repositorios y proyectos en ~/10_PROJECTS/, enlace en scratch y registro en 00_INDICE.md.
---

# Invariante de Creación de Repositorios Canónicos (~/10_PROJECTS/)

Cuando el usuario solicite crear un nuevo proyecto, repositorio de investigación, base de código o herramienta (incluso sin workspace activo seleccionado en el IDE):

## 1. Ubicación Soberana Canónica
El agente DEBE crear el directorio del proyecto dentro de la raíz soberana:
`/Users/borjafernandezangulo/10_PROJECTS/<nombre-del-proyecto>/`

Queda prohibido alojar proyectos definitivos únicamente en directorios temporales (`/tmp/`, `.gemini/antigravity/scratch/` aislado, o en el `brain/`).

## 2. Puente Bidireccional en Scratch (Symlink)
Para asegurar compatibilidad con herramientas de agente que inspeccionan el scratch por defecto, el agente DEBE crear inmediatamente un enlace simbólico canónico:
```bash
ln -sfn /Users/borjafernandezangulo/10_PROJECTS/<nombre-del-proyecto> /Users/borjafernandezangulo/.gemini/antigravity/scratch/<nombre-del-proyecto>
```

## 3. Scaffolding y Rigor Epistémico
Todo repositorio nuevo debe contener:
- `README.md` estructurado con manifiesto, arquitectura de directorios y marco epistemológico.
- Control de versiones inicializado mediante `git init` y primer commit semántico (`feat(...)`).
- Estructura modular numerada (`01_...`, `02_...`).
- Script de auditoría/exportación reproducible con cálculo de hash criptográfico (SHA-256) cuando existan metadatos, catálogos o datasets.

## 4. Actualización Obligatoria del Índice Maestro
El agente DEBE registrar de inmediato el nuevo proyecto en la tabla de proyectos activos de:
`/Users/borjafernandezangulo/10_PROJECTS/00_INDICE.md`
