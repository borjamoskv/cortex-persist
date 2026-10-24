---
name: c5-sovereign-identity-hardening
display_name: Protocolo C5-REAL de Defensa e Inmunidad de Identidad Soberana
description: Aislamiento de identidad digital, auditoría de brechas vía k-anonimato,
  alias desvinculados y migración FIDO2/Passkey.
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

# c5-sovereign-identity-hardening

> **Directiva Declarativa:** Alias generado; conserva rol y alcance del módulo.

Lee [el procedimiento especializado](../c5-secops-infra-devtools/references/modules/c5-sovereign-identity-hardening/MODULE.md) solo cuando la petición requiera este dominio. Una coincidencia genérica como «itera», «sigue» o «auditoría» no activa el módulo. La carga no autoriza efectos externos.
