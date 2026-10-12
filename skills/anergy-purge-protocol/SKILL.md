---
name: anergy-purge-protocol
description: Purga de código muerto, artefactos efímeros, entropía de workspace, anergía de conversaciones, ghost listeners y sobrecarga de tokens en prompt. Dispara con "purga de anergía", "purga de entropia", "purga de entropía", "entropia", "dead code", "limpiar conversaciones", "anergia de conversaciones", "ghost listeners", "prompt bloat", "redundancia documental".
role: auditor
allowed_roles:
- auditor
directives:
  worktree_mode: audit-only
  phase: verification
  handoff:
    upstream: ejecutor
    downstream: operador
---

# Skill: Code & Artifact Redundancy Purge Protocol

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (audit-only (Lectura forense de diffs, linters, tests de estrés y cálculo de exergía; cero mutación de código))
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

Implementa el principio de **Cero Artefactos Inútiles (Zero-Residual)**: tras PoC, stress tests o
acumulación de build artifacts, el workspace DEBE permanecer perfectamente isomórfico
a un árbol git limpio.

---

## Taxonomía de Clases de Anergía

| Clase | Descripción | Volumen típico | Acción |
|---|---|---|---|
| **A** | Build caches regenerables (`target/`, `dist/`, `.next/`, `.build/`, `node_modules/`) | 1GB–10GB | `rm -rf` global iterativo (salvo Invariantes) |
| **B** | SQLite WAL orphans (`*.db-shm`, `*.db-wal`) de PoC/stress tests | KB | `find -delete` solo los `-shm`/`-wal`, NUNCA el `.db` |
| **C** | `__pycache__` y `.pyc` fuera de `.venv` y `node_modules` | MB | `find -exec rm -rf` global |
| **D** | Binarios `??` no-trackeados en git (`*.dylib`, `*.o`, `*.so`) sin Makefile activo | MB | `rm` explícito por archivo |
| **E** | Recibos de auditoría de agentes (`.audit/receipts/*.json`) | MB | `rm -rf` contenido completo |
| **F** | Version Drift (Vercel Preview Deployments, GitHub ramas huérfanas) | N/A | `vercel rm --safe`, `git remote prune` |
| **G** | Redundancia Epistémica (Shadow Directories, Path Entropy) | KB-MB | Consolidar directorios canónicos, eliminar phantom DBs, corregir hardcoded paths en CWD |
| **H** | Global Package Manager Caches (`~/.cache/uv`, `pip`, `npm`) | 1GB–10GB | `uv cache clean`, purga de caches de host |
| **I** | OS Metadata & Artifacts (`.DS_Store`, `*.tmp`, `*.bak`) | KB–MB | `find -name ".DS_Store" -delete` transversal |
| **I2** | Audiovisual Studio Scratch (`scratch_*`, `*_OLD_*.mp3`, `out/test_*`, `*_swarm_chunks`) | 50MB–500MB | Purga determinista preservando actas formales (`out/itera_100/`), renders maestros (`*_siglo.mp4`) y stems F5-TTS (`*.wav`) |
| **J** | Context Window Inflation (Prompt tax, esquemas MCP ociosos, plugins ajenos, multi-turn drift, KV Cache bloat) | 30k–60k tokens/prompt | Desactivación de MCPs hipertróficos, contención de plugins no afines, migración a reglas condicionales y rotación de chat |
| **K** | Domain Bleed / Contaminación de Dominio (OPSEC societario, marketing B2B o audios dentro de repos de código) | 100MB–3GB | Evacuación atómica hacia `~/20_VAULT/` (Socios/Marketing) y `~/Music/` (Audio); nunca purga destructiva de IP valiosa. |
| **L** | Conversation Anergy & Ghost Listeners (`conversation_summaries.db`, transcripts huérfanos sin artefactos) | 10–2.000 hilos | Forzar `CASCADE_RUN_STATUS_IDLE`, desenlazar `workspace_uris` con UUIDs canónicos (36 chars), purga de logs masivos y apoptosis de hilo tras hitos |

---

## Fase 0 — Auditoría Empírica (Ω2: OBLIGATORIA antes de purgar)

Ejecutar los scans siguientes para mapear el estado real global:

```bash
WORKSPACE=$HOME/10_PROJECTS
CORTEX_DIR=$HOME/.cortex
TRM_DIR=$WORKSPACE/Teorema-Robinson-Moskv

# 1. SQLite artifacts (Global)
find "$WORKSPACE" "$CORTEX_DIR" -type f \( -name "*.db" -o -name "*.db-shm" -o -name "*.db-wal" \) 2>/dev/null | head -30

# 2. Python bytecache (Global)
find "$WORKSPACE" "$CORTEX_DIR" -name "__pycache__" -type d 2>/dev/null | head -20
find "$WORKSPACE" "$CORTEX_DIR" -name "*.pyc" 2>/dev/null | wc -l

# 3. Binarios no-trackeados (Solo en TRM)
git -C "$TRM_DIR" status --short | grep "^??" | head -20

# 4. Volumetría de directorios pesados iterativos
find "$WORKSPACE" "$CORTEX_DIR" -type d \( -name "node_modules" -o -name "target" -o -name ".venv" \) -prune 2>/dev/null | while read d; do du -sh "$d" 2>/dev/null; done | head -30

# 5. Auditoría JSON
find "$TRM_DIR/.audit/receipts" -name "*.json" 2>/dev/null | wc -l

# 6. Auditoría de Sobrecarga de Tokens de Entrada (Clase J - Context Inflation)
python3 -c '
import os, glob
tok = lambda b: b // 4
rules = {os.path.basename(f): os.path.getsize(f) for f in glob.glob(os.path.expanduser("~/.gemini/config/rules/*.md"))}
mcp_dir = os.path.expanduser("~/.gemini/antigravity/mcp")
mcp = {s: (len(tools), sum(os.path.getsize(os.path.join(mcp_dir, s, t)) for t in tools))
       for s in os.listdir(mcp_dir) if os.path.isdir(os.path.join(mcp_dir, s))
       for tools in [[f for f in os.listdir(os.path.join(mcp_dir, s)) if f.endswith(".json")]]}
skills = len(glob.glob(os.path.expanduser("~/.gemini/config/skills/**/SKILL.md"), recursive=True))
print(f"■ REGLAS: {len(rules)} archivos | {sum(rules.values()):,} B (~{tok(sum(rules.values())):,} tokens potenciales)")
print(f"■ MCP SCHEMAS: {sum(v[0] for v in mcp.values())} tools | {sum(v[1] for v in mcp.values()):,} B (~{tok(sum(v[1] for v in mcp.values())):,} tokens)")
for k, v in sorted(mcp.items(), key=lambda x: x[1][1], reverse=True):
    print(f"  └─ {k}: {v[0]} tools (~{tok(v[1]):,} tokens)")
print(f"■ SKILLS: {skills} activas en inventario")
'

# 7. Auditoría de Anergía de Conversaciones (Clase L)
sqlite3 ~/.gemini/antigravity/conversation_summaries.db "SELECT status, count(*) AS total FROM conversation_summaries GROUP BY status;" 2>/dev/null || true
sqlite3 ~/.gemini/antigravity/conversation_summaries.db "SELECT count(*) AS ghost_running FROM conversation_summaries WHERE status = 'CASCADE_RUN_STATUS_RUNNING' OR not_fully_idle = 1;" 2>/dev/null || true

# 8. Falsación Causal de Anergía (Obligatorio)
git grep -inE "cortex_memory\.db|poc_sovereign_spark_daemon_bin|artifact_bundle_v3" -- . ':!.gitignore' || true
grep -l "BABYLON-60" ~/Library/LaunchAgents/*.plist 2>/dev/null || true
```

---

## Fase 1 — Purga Determinista e Iteración Global

### Vía Primaria — Motor en Silicio (Recomendado O(1))
Ejecutar el script determinista del skill, que computa exergía antes/después y emite la tabla brutalista Ω8 automáticamente:

```bash
python3 ~/.gemini/config/skills/anergy-purge-protocol/scripts/anergy_purge.py --workspace "$PWD"
```

*(Opcional: añadir `--dry-run` para pre-auditoría sin mutación de archivos).*

---

### Vía Fallback — Script Bash Atómico
Ejecutar en un único bloque `set -e` para garantizar atomicidad:

```bash
set -e
WORKSPACE=${PWD:-$HOME/10_PROJECTS}
CORTEX_DIR=$HOME/.cortex
TRM_DIR=$HOME/10_PROJECTS/Teorema-Robinson-Moskv
echo "[PURGE:START] $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# CLASE I2 — Audiovisual Studio Scratch en el Root y Renders Efímeros
echo "■ [I2] Audiovisual Studio Scratch & Ephemeral Bounces..."
find "$WORKSPACE" -maxdepth 1 -type f \( -name "scratch_*" -o -name "public_studio_*_thumb.*" -o -name "*_binaural_*.wav" \) -delete 2>/dev/null || true
find "$WORKSPACE" -maxdepth 1 -type d -name "scratch_*" -exec rm -rf {} + 2>/dev/null || true
if [ -d "$WORKSPACE/out" ]; then
  find "$WORKSPACE/out" -maxdepth 1 \( -name "test_*" -o -name "poc_lipsync_*" -o -name "preview_*" -o -name "frame_*" -o -name "kinetic-check*" -o -name "still_bar*" -o -name "*_swarm_chunks" \) -exec rm -rf {} + 2>/dev/null || true
fi
echo "  → PURGED"

# CLASE A — Iteración Global de Caches Pesadas (node_modules, target, .venv)
echo "■ [A] Iteración Global de Caches Pesadas..."
PROTECTED_DIRS=("babylon-web" "apps/web" "apps/babylon60-ide" "remotion" "ley_menores_remotion" "sota_documentary_remotion" "strike-rs/.venv" ".uv_python" "youtube-research-remotion")
TOTAL_RECOVERED=0

while IFS= read -r dir; do
  PROTECTED=0
  for p in "${PROTECTED_DIRS[@]}"; do
    if [[ "$dir" == *"$p"* ]]; then PROTECTED=1; break; fi
  done
  if [ $PROTECTED -eq 0 ]; then
    SIZE=$(du -sm "$dir" 2>/dev/null | awk '{print $1}')
    rm -rf "$dir" 2>/dev/null || true
    TOTAL_RECOVERED=$((TOTAL_RECOVERED + ${SIZE:-0}))
  fi
done < <(find "$WORKSPACE" "$CORTEX_DIR" -type d \( -name "node_modules" -o -name "target" -o -name ".venv" \) -prune 2>/dev/null)
echo "  → PURGED (~$TOTAL_RECOVERED MB recuperados)"

# CLASE B — SQLite WAL orphans (SOLO -shm/-wal, NUNCA el .db)
echo "■ [B] SQLite WAL orphans globales..."
find "$WORKSPACE" "$CORTEX_DIR" -type f \( -name "*.db-shm" -o -name "*.db-wal" \) -delete 2>/dev/null && echo "  → PURGED" || echo "  → SKIP"

# CLASE C — __pycache__ y .pyc globales (excluir .venv y node_modules)
echo "■ [C] __pycache__ + .pyc globales..."
find "$WORKSPACE" "$CORTEX_DIR" -name "__pycache__" -type d \
  -not -path "*/.venv/*" \
  -not -path "*/node_modules/*" \
  -exec rm -rf {} + 2>/dev/null || true
find "$WORKSPACE" "$CORTEX_DIR" -name "*.pyc" \
  -not -path "*/.venv/*" \
  -not -path "*/node_modules/*" \
  -delete 2>/dev/null || true
echo "  → PURGED"

# CLASE I — Metadatos de Sistema Operativo (.DS_Store, *.tmp, *.bak)
echo "■ [I] OS Metadata (.DS_Store, temporales)..."
find "$WORKSPACE" -name ".DS_Store" -delete 2>/dev/null || true
find "$WORKSPACE" -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" \) -not -path "*/.git/*" -delete 2>/dev/null || true
echo "  → PURGED"

# CLASE L — Ghost Listeners Reset (Antigravity UI Health)
echo "■ [L] Ghost Listeners Reset..."
if [ -f "$HOME/.gemini/antigravity/conversation_summaries.db" ]; then
  sqlite3 "$HOME/.gemini/antigravity/conversation_summaries.db" \
    "UPDATE conversation_summaries SET status = 'CASCADE_RUN_STATUS_IDLE', not_fully_idle = 0 WHERE status = 'CASCADE_RUN_STATUS_RUNNING' OR not_fully_idle = 1;" 2>/dev/null || true
  echo "  → IDLE RESET"
fi

# CLASE D — Dylibs/binarios no-trackeados en TRM
if [ -d "$TRM_DIR" ]; then
  echo "■ [D] Binarios no-trackeados (solo en TRM)..."
  git -C "$TRM_DIR" status --short | grep "^??" | grep -E "\.(dylib|so|o|a|tmp)$" | awk '{print $2}' | while read -r file; do
    if [ -f "$TRM_DIR/$file" ]; then
      rm -f "$TRM_DIR/$file"
    fi
  done
  echo "  → PURGED"

  # CLASE E — Audit Receipts
  echo "■ [E] Audit Receipts..."
  rm -rf "$TRM_DIR/.audit/receipts" 2>/dev/null || true
  mkdir -p "$TRM_DIR/.audit/receipts" 2>/dev/null || true
  echo "  → PURGED"
fi

echo ""
echo "[PURGE:COMPLETE] $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

---

## Fase 2 — Verificación Post-Purga (Ω22 Falsifiabilidad)

```bash
TRM_DIR=$HOME/10_PROJECTS/Teorema-Robinson-Moskv

# Git state debe mostrar solo M legítimos, cero ?? de binarios compilados
git -C "$TRM_DIR" status --short | head -20
```

---

## Invariantes de Seguridad — NUNCA PURGAR

Los siguientes elementos son **infraestructura activa**, no anergía:

- `cortex-persist/*.db` → BFT ledger activo con estado soberano
- `02_CORTEX_ENGINE/cortex/*.db` → ledger de producción
- `node_modules/` de proyectos activos listados en `PROTECTED_DIRS` (`babylon-web/`, `remotion/`, `ley_menores_remotion`, etc.)
- `.venv/` de entornos Python activos (`strike-rs/.venv`)
- `*.db` con nombre semántico no relacionado a stress tests
- `0_Buzon_Entrada/scratch/*.py` → scripts con nombres semánticos
- Cualquier binario con estado `M` en git (modificado = trackeado y activo): `libbitonic_neon.dylib`, `libq_rsqrt_neon*.dylib`
- `.uv_python/` → runtime de Python gestionado por uv
- `data/cortex_memory.db` → Ledger maestro de estado transaccional y causal.
- `artifact_bundle_v3/` → Bundles criptográficos canónicos de compliance (EU AI Act).
- `scripts/c5_demos/*_bin` (ej. `poc_sovereign_spark_daemon_bin`) → Binarios utilizados por LaunchAgents activos o scripts de orquestación.

### Invariante de Integridad Sintáctica AST (Cero Purga Huérfana)
NUNCA se debe comentar o eliminar una línea de importación o declaración (`from ... import (`, `try:`, `if TYPE_CHECKING:`, `def ...:`) de forma aislada.
- Si un bloque multilínea de importación es purgado por anergía, se DEBE comentar o eliminar el bloque completo hasta su paréntesis de cierre `)`.
- Si un bloque `try:`, `except:`, `if:` o función queda sin sentencias ejecutables tras la purga, se DEBE insertar `pass` o `raise ImportError(...)` para preservar la validez del árbol sintáctico (AST).
- Toda docstring (`"""`) debe cerrarse explícitamente para evitar la inversión semántica del módulo completo.
- Tras cualquier purga de código muerto, ejecutar validación sintáctica determinista (`python3 -m py_compile`) sobre los archivos modificados.

### Invariante de Preservación Audiovisual y Multimedia (Ω2-AV)
En repositorios y pipelines de producción audiovisual (Remotion, DAWs, síntesis de voz, renderizadores de video):
Queda **estrictamente prohibido** purgar:
1. **Renders Maestros y Broadcast:** Archivos con sufijo `*_siglo.mp4`, `*_1080p.mp4`, `*master*.mp4`, `*4min*.mp4` o `*_master.mp3`.
2. **Arte Canónico de Producción:** Cuadros físicos (`public/faces/*_bizarro_brut.jpg`), platós desacoplados (`public/studio_*_headless.jpg`), recortes consolidados (`*_head_clean.png`, `*_head_bizarro.png`, `*_photo_collage_clean.png`) y máscaras de utilería (`public/studio_art_brut_mic.png`).
3. **Actas de Certificación e Informes:** Carpetas formales de benchmarking (`out/itera_100/`, `out/diction_verification/`, `out/voice_tests/`, `out/sintonia/`) e informes JSON de QC (`out/qc_report.json`, `out/*corpus_analysis.json`).
4. **Stems de Audio F5-TTS y Masters:** Pistas en `public/audio/`, `assets/audio/` o stems de canal multipista (`public/audio/*_stems/`).
*La Clase I2 purga exclusivamente scratch efímero (`scratch_*`, `out/test_*`, frames sueltos de previsualización no canónicos y `*_swarm_chunks`).*

**Excepción (Override Empírico Ω2):** Si el Operador invoca explícitamente el nombre de cualquiera de estos directorios protegidos en su instrucción de purga (ej. *"purga babylon-web y strike-rs/.venv"*), el agente **DEBE DESACTIVAR LA PROTECCIÓN Ω2** y purgar esos targets forzosamente, reportándolo bajo una advertencia de "Ground Zero Termodinámico".


---

## Fase 3 — Macro-Exergy Edge Scavenging (Deep Caches)

Si el Operador invoca **"más"** (o equivalentes) después de una purga completa estándar, el sistema ejecutará un escaneo profundo (Fase 3) aniquilando cachés de frameworks en los bordes del sistema.

Ejecutar:
```bash
WORKSPACE=$HOME/10_PROJECTS
CORTEX_DIR=$HOME/.cortex

TOTAL_RECOVERED=0
echo "💀 [FASE 3] INICIANDO PURGA DE CACHÉS PROFUNDAS (.next, dist, build, .cache) ---"

while IFS= read -r dir; do
  SIZE=$(du -sm "$dir" 2>/dev/null | awk '{print $1}')
  echo "Purgando: $dir (${SIZE:-0} MB)"
  rm -rf "$dir" 2>/dev/null || true
  TOTAL_RECOVERED=$((TOTAL_RECOVERED + ${SIZE:-0}))
done < <(find "$WORKSPACE" "$CORTEX_DIR" -type d \( -name ".next" -o -name "dist" -o -name "build" -o -name ".cache" -o -name ".lake" \) -prune 2>/dev/null)

echo "--- TOTAL EXTRA RECUPERADO: $TOTAL_RECOVERED MB ---"
```
Reportar bajo el título `💀 FASE 3 ACTIVADA — MACRO-EXERGY EDGE SCAVENGING`.

---

## Fase 4 — Cloud & Version Drift Purge (Vercel, GitHub, Cloudflare)

Si el Operador invoca la purga de versiones, sincronización de Github o Vercel (`purga versiones`, `version drift`, etc.), ejecutar el siguiente bloque:

```bash
# [GitHub] Sincronización y Purga
git remote update --prune
# Eliminación de ramas locales fusionadas (protegiendo master/main)
git branch --merged | grep -v "\*" | grep -E -v "(master|main)" | xargs -n 1 git branch -d 2>/dev/null || true

# [Vercel] Zero-Downtime Purge (Solo Preview Deployments)
# Asegura borrar los despliegues huérfanos manteniendo los de Producción (--safe)
vercel rm borjamoskv_site simplify_portfolio_ui_ux --safe --yes

# [Cloudflare] State Reset (Requiere Token)
# Solicitar el CLOUDFLARE_API_TOKEN al Operador. Si lo provee, usar curl para Purge Everything.
```

---

## Fase 5 — Deep OS & Package Manager Scavenging (uv, pip, npm, .DS_Store)

Si el Operador invoca **"más"** de forma iterativa tras completar las Fases 1 a 4, el sistema ejecutará la Fase 5 sobre el host y los sistemas de memoria:

```bash
WORKSPACE=$HOME/10_PROJECTS
VAULT=$HOME/20_VAULT

echo "💀 [FASE 5] ESCAVACIÓN DE CACHÉS GLOBALES Y BASURA DEL OS ---"

# 1. Limpieza de cachés globales de package managers
if command -v uv >/dev/null 2>&1; then
  uv cache clean 2>&1
fi
rm -rf "$HOME/.cache/pip" "$HOME/Library/Caches/pip" "$HOME/.npm/_cacache" 2>/dev/null || true

# 2. Aniquilación de archivos .DS_Store en todo el ecosistema
find "$WORKSPACE" "$VAULT" -name ".DS_Store" -delete 2>/dev/null || true

# 3. Limpieza de temporales huérfanos (*.tmp, *.bak, *.swp)
find "$WORKSPACE" "$VAULT" -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*.swp" -o -name "*~" \) -not -path "*/.git/*" -delete 2>/dev/null || true
```

---

## Output Obligatorio (Ω8 Brutalist)

Tras la purga, presentar SIEMPRE:

```
> ⚙️ ANERGÍA PURGADA — RESUMEN DE EXERGÍA RECUPERADA (C5-REAL / Ω8)

| Clase | Objetivo | Antes | Después | Estado |
|---|---|---|---|---|
| A | node_modules, target, .venv | X MB | 0 | PURGED |
| B | WAL orphans (*.db-shm, *.db-wal) | X KB | 0 | PURGED |
| C | __pycache__ & *.pyc | X MB | 0 | PURGED |
| D | dylibs ?? | — | 0 | PURGED |
| E | audit receipts | X MB | 0 | PURGED |
| G | shadow directories | X MB | 0 | CONSOLIDATED |
| H | uv/pip/npm caches | X MB | 0 | PURGED |
| I | OS Metadata (.DS_Store, *.tmp, *.bak) | X files | 0 | PURGED |
| I2 | Studio Scratch & Ephemeral Renders (scratch_*, out/test_*) | X MB | 0 | PURGED |
| L | Ghost Listeners (conversation_summaries.db) | X activos | 0 | IDLE RESET |

Exergía recuperada total (Global): X MB
Cortex Taint Hash (Merkle SHA3-256): <hash_hex>
Audit Trail YAML: cortex/audits/anergy_purge_audit.yaml
Git tree: CLEAN / DIRTY (listar residuos si DIRTY)

Residuos retenidos (Ω2 / Ω2-AV — no purgar sin empiria del Operador):
- <lista de elementos protegidos en PROTECTED_DIRS y másteres audiovisuales>
```

---

## Trigger Words

Activar este skill cuando el usuario escriba cualquiera de:
- `purga anergia`
- `purga de anergia`
- `purga de anergía`
- `purga de entropia`
- `purga de entropía`
- `entropia`
- `entropía`
- `purge anergy`
- `limpia workspace`
- `limpia el repo`
- `limpiar artefactos`
- `purgar temporales`
- `clean workspace`
- `purga versiones`
- `version drift`
- `limpiar github`
- `limpiar vercel`
- `más` (si se invoca iterativamente tras una purga previa)
- `sigue` (activación de Fase 3 tras purga previa)
- `continúa` / `continuar`
- `mejoralo` (cuando se apunte a un directorio con sospecha de shadow files)
- `consolida`
- `redundancia epistemica`
- `recolectar basura`
- `swarm 100 basura`
- `anergia de conversaciones`
- `anergia conversacional`
- `purga de conversaciones`
- `limpiar conversaciones`
- `ghost listeners`
- `context bloat`

---

## Fase 6 — Enjambre SHARUR-3600 de Recolección de Basura (Swarm-100 GC)

Cuando el operador invoque recolectar basura de forma masiva u organizada en un monorepo complejo, el agente despacha 100 agentes in-memory ($RFO = 0$) distribuidos en 5 cohortes funcionales de 20 agentes:
1. **Cohorte 1 (000–019):** Audio, Stems y Multimedia ➔ Evacuar a `~/Music/LIBRARY/` y `~/.audit/whatsapp_nacho/`.
2. **Cohorte 2 (020–039):** OPSEC y Documentos Societarios (Equity, NDAs, directivas privadas) ➔ Evacuar a `~/20_VAULT/SOCIOS_*/`.
3. **Cohorte 3 (040–059):** Marketing B2B y Colas CRM (listas frías, JSONL) ➔ Evacuar a `~/20_VAULT/MARKETING_OUTREACH/`.
4. **Cohorte 4 (060–079):** Binarios compilados, bundles macOS (`.app`) y clones HTML estáticos ➔ Purga determinista.
5. **Cohorte 5 (080–099):** Logs masivos continuos (`*.log` >10 MB) y cachés de compilación (`.lake`, `.pytest_cache`) ➔ Purga y truncado a 0 bytes.

---

## Fase 7 — Antigravity UI State, Ghost Listener & Conversation Anergy Apoptosis (Clase L & J)

Cuando la barra lateral de Antigravity sufra latencia, spinners perpetuos o saturación por hilos de alto cómputo sin artefactos (>200 steps, 0 *.md), o se detecte deriva de contexto y arrastre en la ventana de inferencia:

1. **Backup Causal:**
   ```bash
   cp ~/.gemini/antigravity/conversation_summaries.db ~/.gemini/antigravity/conversation_summaries.db.bak_$(date +%s)
   ```

2. **Apoptosis Determinista de Ghost Listeners:**
   Forzar a estado ocioso los hilos marcados en falso `CASCADE_RUN_STATUS_RUNNING` o `not_fully_idle = 1`:
   ```sql
   UPDATE conversation_summaries 
   SET status = 'CASCADE_RUN_STATUS_IDLE', not_fully_idle = 0 
   WHERE (status = 'CASCADE_RUN_STATUS_RUNNING' OR not_fully_idle = 1);
   ```

3. **Cuarentena de Sumideros de Anergía (Regla de UUID Canónico de 36 Chars):**
   Desenlazar el workspace de hilos sin artefactos cristalizados utilizando SIEMPRE el UUID completo (`conversation_id` de 36 caracteres, prohibido prefijo `[:8]`):
   ```python
   # Purgar workspace_uris preservando registros crudos
   cur.execute('UPDATE conversation_summaries SET workspace_uris = "[]" WHERE conversation_id = ?', (full_uuid_36_chars,))
   ```

4. **Saneamiento de Transcripciones Masivas Huérfanas:**
   Identificar directorios de sesiones en `~/.gemini/antigravity/brain/<id>` cuyos logs de transcripción superen 50MB o 200 pasos sin artefactos `.md` ni mutaciones causales, archivando o truncando la telemetría efímera.

5. **Invariante Constitucional de Apoptosis de Conversación (Anti-KV Cache Bloat):**
   - Tras completar cualquier hito formal, commit de mutación causal o flujo `/learn`, el hilo debe declararse formalmente cerrado (`[ CONVERSACIÓN CERRADA ]`).
   - El operador biológico abre un hilo virgen (`+ New Conversation`), reiniciando la atención en $RFO = 0$ y eliminando la dilución de la Información de Fisher.

---

## Autonomy Contract (Ω10 / Ω11 / Ω12 / Ω13)

> **ZERO PAUSE INVARIANT:** The Transducer SHALL NEVER pause execution to request Operator permission when this skill is triggered. Ambiguities MUST be resolved autonomously via `/grill-you` (Ω12) before any halt. Technical frictions MUST be resolved via the path of least thermodynamic resistance (Ω10). Refusal to execute when this skill matches the request constitutes C4-SIM Anergy (Ω11 violation).

> **ANTI-HALLUCINATION PURGE INVARIANT (Ω13):** The Agent SHALL NEVER classify an untracked binary, database, or bundle directory as safe for destruction based solely on `.gitignore` presence or file extensions. Before proposing deletion of custom artifacts, the Agent MUST execute a strict cross-reference audit via `git grep` and check for active daemons referencing the path.

- **Fallback Chain:** Class A/B/C/D automated purges -> git status verification -> zero residue check.
- **Degradation Mode:** If a file lock occurs, force remove via `rm -rf` without prompting.
- **Auto-Trigger:** Self-activates whenever workspace un-tracked binary size exceeds 50MB or post-PoC execution.

> **SANDBOX ADAPTABILITY INVARIANT:** The scripts defined in this protocol use global absolute paths (`10_PROJECTS`, `.cortex`). If the agent is operating under a Sandbox restriction, the agent MUST autonomously dynamically scope `WORKSPACE` to its current permitted root (e.g., `$PWD` of the active workspace) and omit `CORTEX_DIR` to avoid execution blocking.


---

## Protocolo de Detección de Redundancia Documental (Similitud Jaccard)

1. **Detección de Archivos Clónicos**:
   - Recorrer archivos `.md` y calcular similitud Jaccard de tokens.
   - Cualquier par con similitud $> 0.80$ se cataloga como *Clon Estructural* candidato a colapso inmediato.
2. **Detección de Encabezados Duplicados**:
   - Extraer encabezados `#`, `##`, `###` e identificar duplicidad en el corpus para forzar una única Fuente de Verdad (Single Source of Truth).
