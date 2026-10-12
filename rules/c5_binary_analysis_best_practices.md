# Invariante de Buenas Prácticas en Análisis de Binarios (C5-REAL)

## 9. Buenas prácticas y limitaciones

- **No romper la firma de código:** Modificar los binarios invalidará la firma y la app no arrancará sin desactivar Gatekeeper (`spctl --disable`).
- **No distribuir ningún fragmento extraído:** La licencia de la app protege el código. Queda estrictamente prohibido compartir, filtrar o distribuir la base de código.
- **Respeta la privacidad:** Si extraes tokens de API, elimínalos inmediatamente. Nunca los persistirás ni en los logs ni en el repositorio.
- **Entorno controlado:** Realiza el análisis en una VM o en una partición separada para evitar interferir con tu entorno de trabajo principal.
