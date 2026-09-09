---
name: vscode-git-packed-refs-diagnostics
display_name: "Reparación de Corruptelas Git & Packed-Refs en VS Code"
description: "Reparación de corruptelas de Git, bloqueos de packed-refs e índice de repositorios en VS Code / Antigravity IDE. Dispara con \"vscode git enoent\", \"packed-refs\", \"corrupción git\", \"reparar git vscode\"."
---

# Skill: VS Code Git Extension Colapse Diagnostics

## Contexto de Activación
Este protocolo se activa cuando la interfaz gráfica de VS Code (Source Control) se corrompe, lanza errores emergentes rojos (`Failed to execute git`), o emite advertencias en el *Output* con las siguientes firmas:
- `[Git][revParse] Unable to read file: ENOENT: no such file or directory` (Refs empaquetadas o Worktrees fantasma).
- `[GitFileSystemProvider][readFile] File not found - git:...?ref=~` (Crash por diff en submódulos).
- `[GitFileSystemProvider][stat] File not found - git:...` (Archivos renombrados o artefactos efímeros no rastreados).
- `BABYLON-60 pre-commit WARNINGS (non-blocking)` abortando el *commit* falsamente.


## Diagnóstico y Principio Físico
La extensión de Git en VS Code colapsa térmicamente cuando su capa de lectura en Node.js choca contra inconsistencias topológicas del repositorio:
1. **Packed-refs:** Si `git pack-refs` elimina los archivos sueltos en `.git/refs/remotes/`, `fs.readFile` explota.
2. **Ghost Worktrees:** Si un subagente o proceso externo crea un *git worktree* y lo borra físicamente sin hacer `git worktree prune`, VS Code leerá el metadato en `.git/worktrees/` apuntando a la nada.
3. **Submódulos Modificados:** Si un submódulo dentro de un *Monorepo* contiene archivos *untracked*, VS Code intenta renderizar un diff virtual del directorio que falla y estrella la UI.
4. **Pre-commits Ciegos:** Si un hook evalúa `git diff --cached` sin ignorar los archivos que están siendo borrados (`git rm`), abortará el proceso al confundir un borrado con una adición.

## Procedimientos Deterministas de Remediación

Aplicar de forma estricta los siguientes comandos nativos de máxima exergía en lugar de scripts manipuladores.

### 1. Remediación de Ghost Worktrees (El más letal)
Si el log indica `ENOENT` apuntando a un directorio de *worktree* (ej. `.gemini/antigravity/brain/...`):
```bash
git worktree prune -v
```
*Impacto:* Borra instantáneamente los metadatos de los *worktrees* muertos, restaurando la estabilidad de la UI.

### 2. Remediación de Crash por Submódulos (Monorepos / Vaults)
Si el IDE expone submódulos modificados pero no deja ver el *diff* (File not found):
```bash
git config --local diff.ignoreSubmodules dirty
```
*Impacto:* Frena la recursión innecesaria. El repositorio padre ignorará las modificaciones internas de los submódulos y solo reportará cambios si su *commit base* cambia, salvando a VS Code de la recursividad infinita.

### 3. Remediación de Packed-refs o Referencias Rotas
Si el log indica `ENOENT` sobre `refs/remotes/origin/...`:
```bash
git pack-refs --all && git gc --prune=now
```
*Impacto:* Fuerza una limpieza y compresión topológica para que los punteros sueltos se reconstruyan (opcional: realizar un `git fetch` en el repositorio afectado para restaurar el puntero).

### 4. Axioma para Hooks de Pre-Commit
Si un archivo borrado dispara reglas de *pre-commit* y aborta la confirmación:
*Nunca* usar `git diff --cached --name-only` en crudo.
*Axioma Invariante:* Inyectar `--diff-filter=ACMR` en el *hook* para ignorar archivos en proceso de borrado.
```bash
# CORRECTO
staged_files=$(git diff --cached --name-only --diff-filter=ACMR)
```

### 5. Remediación de Directorios Legados `.git/remotes/` (Cuelgues de filter-repo)
Si `git status` o `git filter-repo` emiten la advertencia `warning: unable to access '.git/remotes/origin': Is a directory`:
```bash
rm -rf .git/remotes
```
*Impacto:* Elimina el formato legado pre-Git 1.5 que provoca el cuelgue silencioso de `git filter-repo` al recorrer el árbol de referencias.

### 6. Diagnóstico de Repositorio Archivado en GitHub (Read-Only)
Si un `git push` responde con `ERROR: This repository was archived so it is read-only`:
- No reintentar el push inmediatamente.
- Notificar al usuario para desarchivar desde GitHub (**Settings -> Danger Zone -> Unarchive this repository**).

### 7. Remediación de Límite de Gödel-Turing (State Bloat / >10k Cambios Activos)
Si la UI colapsa con el warning `El repositorio Git contiene muchos cambios activos, solamente un subconjunto...`:
```bash
echo -e "\nnode_modules\n.DS_Store\ndist\nbuild\n.next\nout\n.env" >> .gitignore && git rm -rf --cached node_modules .DS_Store dist build .next out 2>/dev/null || true
```
### 8. Remediación del Límite de Packfile de GitHub (2.00 GiB Exceeded)
Si un `git push` falla con `remote: fatal: pack exceeds maximum allowed size (2.00 GiB)`:
1. Inspeccionar cuáles son los blobs o carpetas gigantes que inflan el repositorio:
   ```bash
   git ls-tree -r -l HEAD | sort -n -k 4 | tail -20
   ```
2. Si existen carpetas de backup accidentales (ej. `BABYLON-60.git-backup/`) o binarios comprimidos gigantes:
   ```bash
   git filter-repo --invert-paths --path <ruta_gigante> --force
   ```
3. Verificar la reducción de tamaño de `.git` (`du -sh .git`) y re-vincular el remoto SSH antes de reintentar el push.

### 9. Diagnóstico de URIs Virtuales de Git (GitFileSystemProvider Warnings)
Si la consola del IDE o los logs emiten avisos del tipo `[GitFileSystemProvider][stat]` o `[readFile] File not found` para rutas `git:/...`:
- **Archivos Renombrados**: Si el archivo fue renombrado en commits recientes (ej. refactorización C5-REAL), el proveedor virtual resolverá revisiones históricas pero fallará en el *working tree* actual. Verificar con `git log --oneline -n 5 -- <ruta_antigua>` y `git show <commit> --stat`.
- **Artefactos Efímeros Untracked (.sarif, .tmp, logs)**: Si se borraron o cerraron pestañas de informes efímeros no rastreados por Git, los avisos de `GitFileSystemProvider` son inofensivos. Se resuelven cerrando las pestañas huérfanas en el editor o refrescando el panel *Source Control*.

## Protocolo de Ejecución
Ante un crash de VS Code Git, ejecuta las remediaciones 1, 2 y 3. Inmediatamente después, indica al usuario que presione el botón de "Refrescar (🔄)" en la pestaña de *Source Control* de su IDE. El sistema recuperará su estado nominal.


