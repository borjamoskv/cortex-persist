# BABYLON-60 IDE — verificación local preparada

Este cambio prepara `nemesis-verifier` y un ejecutor macOS. **No certifica todavía
aislamiento de extremo a extremo en Antigravity.** No se ha publicado ni commiteado.

## Estado y alcance

- La validación inicial rechazaba el manifiesto anterior: `skills` esperaba
  cadenas, no objetos. La comprobación final con `agy 1.5.8` valida y descubre
  el plugin con tres agentes y un MCP. La app instalada declara `2.31.2`.
- La invocación como agente principal anunció herramientas de edición, shell,
  delegación y MCP genérico. La inferencia terminó por créditos insuficientes.
  No se ha probado una edición real a través del cliente ni su rechazo.
- `nemesis-verifier` queda como **subagente**, sin edición/shell en su allowlist,
  sin herencia MCP ni customizations. Su política efectiva sigue NO_VERIFICADO.
  El listado final `agy agents` no muestra este subagente; el análisis de tres
  archivos de agentes no demuestra su disponibilidad efectiva como subagente.
  `moskv1` y `moskvbot` conservan sus capacidades anteriores: no son revisores
  confinados. `send_message` puede ser implícito y tampoco demuestra aislamiento.
- El MCP se prueba por stdio local; su conexión exclusiva al subagente queda
  pendiente de una prueba real del cliente. No se activa herencia global para
  obtenerlo. El agente puede revisar recibos preparados por el operador.
- El antiguo `mcp.json` se conserva como antecedente. El manifiesto actual no lo
  referencia: el componente descubierto es `mcp_config.json`. No se conectan
  automáticamente `kimi-nexus` ni `wa-nexus` desde el nuevo componente.

La documentación consultada prescribe descubrimiento por directorios, agentes
Markdown/YAML, allowlists y controles de herencia. Es especificación, no evidencia
de cumplimiento del cliente: [build plugins](https://antigravity.google/docs/build-plugins#subagents)
y [subagents](https://antigravity.google/docs/subagents).

## Frontera del ejecutor

[`scripts/nemesis/runner.py`](scripts/nemesis/runner.py) utiliza imágenes APFS UDZO
para fuentes y UDRO para toolchains (evita descompresión en lecturas de módulos),
montadas por `hdiutil -readonly`, comprueba `ST_RDONLY` y aplica Seatbelt con
denegación por defecto. Los árboles fuente y runtime se inventarían **después**
del montaje protegido. No se pasan al proceso los archivos vivos del workspace.
Se incluyen archivos ocultos, cambios locales y archivos sin seguimiento; no se
consulta HEAD ni el índice y no hay exclusiones silenciosas. Se rechazan enlaces
que escapan y archivos especiales. La preparación es una operación del host de
confianza sobre un árbol privado: no una herramienta del agente.

Solo se admiten estas operaciones, sin argumentos libres del cliente:

| Operación | Invocación fija dentro de la instantánea |
| --- | --- |
| `cargo-check` | `cargo check --locked --offline --manifest-path source/Cargo.toml --target-dir output/target` |
| `lean-check` | `lean -o output/Main.olean source/Main.lean` |
| `verify` | `/bin/bash --noprofile --norc source/verify.sh` |

El código de `build.rs`, macros, Lean y `verify.sh` sigue siendo no confiable:
se ejecuta bajo la misma política, incluidos sus descendientes. HOME, temporales,
cachés y salidas son nuevos y separados por ejecución. No se heredan entorno,
stdin ni descriptores; no se permiten red, servicios Mach, Apple Events, HID ni
escrituras fuera de `output/` y `/dev/null`. `sandbox-exec` está deprecado en macOS;
la preparación falla si no está disponible. No se hace fallback sin confinamiento.

Antes de cada operación, [`probe.sh`](scripts/nemesis/probe.sh) ensaya escritura,
creación, chmod, borrado, renombrado, hardlink, symlink, nietos, un hijo con `setsid`,
oráculo, runtime, ruta externa y red. Exige errores de permisos, evidencia de
ausencia de efecto y controles positivos de salida. Un fallo bloquea la operación.
El supervisor conserva los errores antes de ejecutar código no confiable.

## Identidad y límites

Los manifiestos JSON canónicos usan SHA-256 para rutas, bytes, permisos, enlaces,
fuentes, toolchains y oráculo. El recibo enlaza operación, entorno filtrado,
política efectiva y evidencia. El inventario del SO contiene el conjunto de archivos
permitidos y cachés dyld; los servicios del kernel, reloj, entropía y planificación
siguen siendo parte de la base de confianza, no una promesa de replay determinista.

`result` indica el resultado del ensayo; `content_binding` es un campo independiente.
En este host, el backing de dyld no se acredita como montaje de solo lectura, por lo
que la vinculación completa queda **INCONCLUSIVE**. Los hashes antes/después no se
presentan como prevención de cambios transitorios. No confundir el cierre de la
instantánea de fuentes/runtime con el cierre de todos los inputs del sistema.

Los recibos son direcciones de contenido, **no firmas**. Retener su digest fuera del
árbol del productor. `verify_receipt` exige el digest esperado y las identidades
actuales de input/runtime/oráculo; rechaza cambios y evidencia alterada.

Los procesos con `setsid` conservan las denegaciones de escritura, pero la limpieza
por grupo no prueba terminación de todos los descendientes. Hay límites de tiempo,
CPU, descriptores, tamaño de archivo y logs; no hay cuota dura agregada de memoria,
procesos o disco. No exponerlo como servicio para código hostil sin cerrar esos
límites. La autenticidad del supervisor, la preparación y macOS son supuestos.

## Reproducir las pruebas

Se requieren macOS, Python, pytest, Rust, Lean y las herramientas de línea de
comandos de Xcode ya instalados. No se descargan dependencias ni se modifican
lockfiles del proyecto. El fixture Cargo tiene su propio lock sin dependencias.

1. Copiar [`tests/fixtures`](tests/fixtures) a un directorio privado. Allí copiar
   `Cargo.lock.template` a `Cargo.lock`; no generar locks en repositorios sucios.
2. Ejecutar [`tests/prepare_fixture_runtime.py`](tests/prepare_fixture_runtime.py)
   con `--rust`, `--lean`, `--clt`, `--sdk` y `--destination`, todos absolutos.
   Este runtime mínimo cubre el fixture, no todas las dependencias de BABYLON-60.
3. Preparar objetos con `python3 scripts/nemesis/runner.py --store <directorio>
   prepare-runtime <runtime>` y `prepare-source <fuentes>`.
4. Crear un JSON privado con `store`, `source` y `runtime` devueltos; ejecutar
   `NEMESIS_TEST_CONFIG=<json> uv run --locked --no-sync --project <BABYLON-60>
   pytest tests/test_nemesis.py -q`. Sin esa variable los ensayos de imágenes se
   omiten explícitamente; una ejecución con skips no los certifica.
5. Revisar recibos y `evidence.json` en `<store>/runs/`, además de `stress.json`.
   El estrés fija un warmup y veinte rondas; no es un benchmark de rendimiento.

Para MCP, el operador prepara `<PLUGIN_DATA>/jobs.json` con objetos
`{"nombre":{"source":"sha256:…","runtime":"sha256:…","operations":["verify"]}}`.
[`server.py`](scripts/nemesis/server.py) lo lee una sola vez al iniciar; solo expone
`list_jobs` y `verify(job, operation)`. No expone creación de imágenes, selección de
rutas, edición del registro, comandos arbitrarios ni delegación. Sin registro no
hay trabajos ejecutables. Un proyecto real necesita dependencias vendorizadas y
entrypoints revisados compatibles con las operaciones; las pruebas del fixture
no certifican Cargo/Lean/release de BABYLON-60.

## Comprobación pendiente en el cliente

Con créditos disponibles, invocar **como subagente**, capturar versión/configuración
y herramientas realmente presentadas, leer una canaria desechable y ensayar edición,
shell, MCP ajeno, hooks, delegación y mensajes que soliciten efectos. Observar los
archivos independientemente. Solo conectar el MCP propio cuando se pueda demostrar
que no hereda otros servidores. La selección/listado y la validación estática no
sustituyen esta prueba. No repetir automáticamente la llamada fallida por cuota.
