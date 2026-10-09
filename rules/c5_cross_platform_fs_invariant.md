# Invariante Cross-Platform de Silicio Efímero (INV_C5_CROSS_PLATFORM_FS)

**Contexto:** Los agentes tienden a confabular asumiendo entornos POSIX universales al interactuar con el sistema de archivos efímero, provocando fracturas y cuellos de botella termodinámicos en nodos Windows (como se observó en la caída de PRs por bloqueos estáticos en `/tmp/`).

1. **Veto a Rutas Absolutas (Fail-Closed):** Queda estrictamente prohibido hardcodear rutas como `/tmp/`, `/var/run/`, o `~/.cache/` para semáforos, *locks* o almacenamiento efímero en scripts multiplataforma (Python, Rust, Bash compatibles).
2. **Abstracción Obligatoria:** 
   - En **Python**, exigir invariablemente `os.path.join(tempfile.gettempdir(), ...)`.
   - En **Rust**, exigir invariablemente `std::env::temp_dir()`.
   - En **Scripts Shell**, utilizar expansiones tolerantes como `${TMPDIR:-/tmp}`.
