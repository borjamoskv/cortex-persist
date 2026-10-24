---
name: c5_github_supply_chain_and_governance_invariant
description: Invariante C5-REAL de homogenización y endurecimiento de GitHub Actions (supply chain, mínimo privilegio, concurrencia y gobernanza de anillos).
trigger: "model_decision"
---

# Invariante de Cadena de Suministro y Gobernanza de GitHub (INV_C5_GITHUB_SUPPLY_CHAIN_AND_GOVERNANCE)

Toda interacción, diseño, auditoría o refactorización sobre `.github/` o metadatos de repositorio en repositorios soberanos y de alta exergía DEBE cumplir estrictamente estas 5 invariantes:

## 1. Fijación Inmutable de Actions (Veto a Tags Flotantes y Ficticios)
* **Prohibición de Tags Ficticios:** Queda estrictamente prohibido emitir o aceptar versiones imaginarias o no verificadas (`@v7`, `@v8`, etc.).
* **Pinning por Commit SHA de 40 Caracteres:** En workflows de producción, verificación o release, toda acción externa o de GitHub DEBE fijarse mediante su hash SHA-1 de commit inmutable de 40 caracteres hexadecimales, documentando la versión semántica en comentario:
  ```yaml
  uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v4.2.2
  uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v5.x
  ```

## 2. Mínimo Privilegio de Tokens (Principio de Least Privilege)
* **Permisos Raíz Obligatorios:** Todo archivo `.github/workflows/*.yml` DEBE declarar a nivel raíz:
  ```yaml
  permissions:
    contents: read
  ```
* **Elevación Quirúrgica:** Permisos adicionales (`id-token: write`, `pull-requests: write`, `security-events: write`, `issues: write`) se declaran exclusivamente dentro del job específico que los consume.
* **Persist Credentials False:** Todo paso `actions/checkout` DEBE incorporar `persist-credentials: false` salvo requerimiento explícito de mutación remota de Git.

## 3. Concurrencia y Anergía Cero en CI
* Todo workflow activado por eventos `push` o `pull_request` DEBE incluir bloque de concurrencia para abortar ejecuciones obsoletas:
  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: true
  ```

## 4. Gobernanza de Repositorio Acoplada a Anillos
* **CODEOWNERS:** Mapear la jerarquía de Anillos de Seguridad del proyecto:
  * `Ring-0`: Núcleos de silicio, memoria compartida, criptografía (`00_ABZU_KERNEL/`, `crates/`, `src/`).
  * `Ring-1`: Verificación formal, Lean 4, Z3, contratos (`proof/`, `contracts/`).
  * `Ring-2`: CI/CD, scripts de calidad, dependencias, ledger (`.github/`, `scripts/`, `tests/`).
  * `Ring-3`: Documentación, guías y manifiestos de raíz (`docs/`, `*.md`).
* **Veto a Blank Issues:** `.github/ISSUE_TEMPLATE/config.yml` DEBE contener `blank_issues_enabled: false` y redirigir a la política de seguridad (`SECURITY.md`) y contratos de trabajo (`AGENTS.md`).
* **Plantillas Estructuradas:** Issues de errores deben formularse bajo el protocolo de Falsación Popperiana (Hipótesis + Contraejemplo Reproducible); propuestas arquitectónicas bajo Stage 1 de C5-REAL (utilidad causal independiente + criterio observable de aceptación/fallo).

## 5. Paridad de Dependencias y Salud de Repositorio
* **Dependabot Ecosistemas Nativos:** Usar `pip` para Python (no `uv`), configurar agrupaciones atómicas (`groups`) para dependencias acopladas y prefijar commits con el linter del repo (`commit-message: prefix: "[AX-0] DEPS"`).
* **Archivos Canónicos Obligatorios:** Todo repositorio con formalización o código ejecutable debe incluir `CONTRIBUTING.md` (enlazando reglas y contratos) y `CITATION.cff` (metadatos formales de citación para investigación y preprints).
