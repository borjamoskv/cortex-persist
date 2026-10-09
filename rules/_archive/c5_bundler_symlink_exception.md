# Excepción Causal: Bundlers y Centralización de Activos (C5-REAL)

## La Paradoja de Webpack/Remotion
Cuando se aplique la **Invariante de Centralización de Activos Musicales** (`~/Music/`), el agente DEBE analizar primero si el archivo de audio reside dentro de la carpeta estática (`/public/`, `/assets/`) de un bundler de frontend activo (Next.js, Vite, Remotion).

## Resolución (Inversión Topológica)
- **Fallo:** Mover el archivo a `~/Music/` y poner un symlink en `/public/` romperá el build por restricciones de seguridad del empaquetador web (impidiendo accesos fuera de la raíz del proyecto).
- **Acción Obligatoria (Zero-Breakage):** El archivo real DEBE permanecer físicamente en el repositorio del proyecto (`/public/audio/`). La centralización se logrará creando el symlink a la inversa: un enlace estático en `~/Music/` que apunte hacia el interior del proyecto.
