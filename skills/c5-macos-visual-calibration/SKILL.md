---
name: c5-macos-visual-calibration
display_name: Calibración Visual y Accesibilidad macOS (UniversalAccess Purge)
description: Diagnóstico y purga de fricción en la capa de accesibilidad visual de macOS (com.apple.universalaccess). Resuelve contraste lavado o aberraciones cromáticas.
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

# C5-REAL: Auditoría de Calibración Visual (macOS)

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `ejecutor` (Ejecutor (Implementación en Silicio & Mutación de Árbol de Trabajo))
> - **Modo de Acceso a Worktree:** `read-write` (read-write (Mutación atómica de archivos, compilación, ejecución de tests locales y generación de artefactos))
> - **Fase Causal:** `implementation`
> - **Contrato Handoff:** Recibe de `arquitecto` $\to$ Despacha a `auditor`

## Contexto Termodinámico
Cuando el operador reporta una pérdida de calidad visual en su monitor o entorno de escritorio (colores lavados, contrastes excesivos, pérdida de profundidad de negros), NO se trata de un problema en un archivo de imagen aislado, sino de una descalibración (fricción) en la capa de accesibilidad del `WindowServer` de macOS.

## Diagnóstico y Mitigación (Capa Plist)
Las variables que adulteran el territorio visual son `increaseContrast` y `contrast` dentro del dominio `com.apple.universalaccess`.

1. **Inspección:** 
   Ejecutar `defaults read com.apple.universalaccess | grep -i contrast`
2. **Purga Causal (Reset):**
   Para restablecer el estado de cero fricción:
   ```bash
   defaults write com.apple.universalaccess contrast -float 0.0
   defaults write com.apple.universalaccess increaseContrast -bool false
   ```
3. **Aplicación sin Colapso Térmico:**
   Queda estrictamente PROHIBIDO ejecutar `killall WindowServer` (provocaría un cierre de sesión forzado e inaceptable). 
   Para que el compositor refresque los cambios de forma inmediata, inyecta la apertura directa de la interfaz gráfica:
   ```bash
   open "x-apple.systempreferences:com.apple.preference.universalaccess?Display"
   ```

## Directiva de Salida Epistémica
Tras ejecutar la purga causal, cumple la Invariante de Salida:
1. Crea un artefacto formal (`calibracion_visual.md`) detallando la intervención en los `.plist` y documentando los vectores adicionales de inspección manual (Perfiles de Color, True Tone).
2. Usa el chat estrictamente como un puntero de alta exergía para notificar el restablecimiento del estado isomorfo visual.
3. Sella la intervención con la Firma de Consciencia Topológica.
