---
name: c5-dataset-monotonicity-invariant
description: Invariante de Monotonicidad de Datasets (INV_DATASET_MONOTONIC). Prohíbe el truncamiento o sobrescritura destructiva de corpora maestros en pipelines de fine-tuning de IA.
---

# Invariante de Monotonicidad de Datasets (INV_DATASET_MONOTONIC)

## Principio de Expansión No Destructiva
Al crear, modificar o ejecutar scripts de preparación, sanitización o consolidación de datasets multi-dominio (ej. `prepare_master_dataset.py`, integradores ShareGPT/ChatML):

1. **Prohibición de Truncamiento:** El agente NUNCA debe permitir que la ejecución de un script reduzca el número total de muestras únicas ($N_{\text{nuevo}} < N_{\text{anterior}}$) de un dataset maestro consolidado, salvo instrucción explícita de purga.
2. **Baseline Inmutable como Fallback:** Si las rutas a los archivos de dominios individuales o volcados brutos están ausentes (ej. movidos a vault, archivados o en nodos remotos), el script DEBE utilizar el dataset maestro preexistente en disco como baseline de partida inmutable y añadir las nuevas muestras de forma aditiva y deduplicada.
3. **Verificación de Invariante ($\Delta N \ge 0$):** Antes de sobrescribir archivos `.jsonl` maestros y splits de entrenamiento (`train.jsonl`, `valid.jsonl`), el proceso debe asertar programáticamente que el conteo final de registros es igual o superior al estado precedente.
