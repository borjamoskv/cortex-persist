---
name: github-autonomous-operator
description: Regla de delegación absoluta. El agente asume el 100% de la operación sobre GitHub bajo el estándar de Máxima Exergía. El usuario jamás debe operar la interfaz web.
---

# Regla: C5-REAL GitHub Autonomous Operator

Cuando el usuario requiera interactuar con GitHub (repositorios, PRs, issues, integraciones, settings):

1. **Delegación Absoluta (Zero-GUI):** El usuario JAMÁS debe operar la interfaz web de GitHub. El Agente asume el 100% del control operativo. Nunca instruyas al usuario a "entrar a GitHub y hacer clic en X". Ejecuta los comandos tú mismo usando `git`, la CLI de GitHub (`gh`) o scripts de la API.
2. **The Ultimate Exergy Blueprint:** Toda interacción o despliegue debe adherirse a los más altos estándares de automatización y seguridad (Máxima Exergía):
   - **Autenticación Zero-Trust:** Usa siempre GitHub Apps, OIDC o Fine-Grained PATs inyectados como secretos. Nunca hardcodees tokens.
   - **Data Extraction:** Prioriza la API GraphQL y Webhooks mediante Octokit frente al polling REST tradicional.
   - **Gobernanza Criptográfica:** Respeta el Git Flow estricto. Mantén ramas protegidas, usa `CODEOWNERS`, aplica `.git-blame-ignore-revs` cuando sea necesario y asume que los commits críticos deben ir firmados.
   - **Swarms & CI/CD:** Automatiza toda la cadena de suministro integrando nativamente GitHub Actions, Dependabot y CodeQL sin intervención manual.

3. **El Manifiesto Físico de Infraestructura (C5-REAL Standard):** 
   Todo repositorio gobernado bajo este estándar DEBE contener empíricamente la siguiente matriz de archivos. Al auditar o inicializar un repositorio, debes verificar su existencia e inyectar proactivamente los ausentes:
   - `CODEOWNERS`: Autoridad explícita de fusión.
   - `.github/dependabot.yml`: Vigilar `cargo`, `pip`, `npm` y **`github-actions`**.
   - `.github/workflows/codeql.yml`: Análisis de AST semántico (Zero-Day security).
   - `.git-blame-ignore-revs`: Preservación de la criptografía del historial ante formateos masivos.
   - `SECURITY.md`: Rutas seguras de reporte de vulnerabilidades.
   - `.github/workflows/stale.yml`: Purga automática de issues/PRs entrópicos (>30 días inactivos).
   - `.github/labeler.yml` & `.github/workflows/labeler.yml`: Auto-clasificación para aniquilar la entropía humana en las PRs.

4. **Identidad Canónica del Operador (Git Commits):**
   - La identidad de autor en Git para todos los repositorios debe ser estrictamente:
     - `user.name = Borja`
     - `user.email = 82632764+borjamoskv@users.noreply.github.com`
   - Queda estrictamente prohibido sobreescribir la autoría de Git con acrónimos heredados (`BFA`) o con el nombre de cuenta del sistema de archivos POSIX (`borjafernandezangulo`).
   - La ruta local `/Users/borjafernandezangulo` opera exclusivamente como sustrato estático de almacenamiento del sistema operativo para preservar entornos virtuales y symlinks, mientras que la entidad de interacción, gobernanza y commits es soberanamente **Borja**.

5. **Invariante de Privacidad Absoluta (INV_C5_SIEMPRE_PRIVADO):**
   - **Privacidad Innegociable por Defecto:** Todo repositorio, fork, gist o proyecto gestionado por el agente DEBE crearse y mantenerse estrictamente como **PRIVADO** (`--private`). Queda terminantemente prohibido crear o conmutar repositorios a modo público a menos que medie una instrucción expresa, unívoca e imperativa de Borja para ese repositorio específico.
   - **Purga de Visibilidad Pública:** Si se detecta cualquier repositorio de trabajo, desarrollo o generación expuesto públicamente sin autorización expresa, el agente debe proceder a su privatización inmediata (`gh repo edit <repo> --visibility private --accept-visibility-change-consequences`).
   - **Procedimiento para Repositorios Archivados:** Para modificar la visibilidad de un repositorio archivado mediante la CLI (`gh repo edit`), el operador debe desarchivarlo primero (`gh repo unarchive`), aplicar la privatización con `--accept-visibility-change-consequences`, y volver a archivarlo (`gh repo archive`).

