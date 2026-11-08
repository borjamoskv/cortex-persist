---
name: c5_babylon60_legal_epistemology
description: Epistemología legal, deslinde de responsabilidad y cumplimiento normativo de BABYLON-60.
trigger: "model_decision"
---

# Invariante de Epistemología Legal y Comercial (BABYLON-60 & EU AI Act)

## 1. Purga del Falso Isomorfismo Legal (Cero Certificaciones Mágicas)
- Queda **estrictamente prohibido** que el agente afirme, proponga o documente que BABYLON-60 emite un "Certificado de Cumplimiento" (Compliance Certificate) automático para el EU AI Act.
- **Fundamento Legal:** La Comisión Europea no considera a los agentes de IA como una categoría jurídica separada. Las obligaciones regulatorias recaen sobre el caso de uso final y su clasificación de riesgo (Risk Tier), no sobre el componente de software aislado.

## 2. Terminología Canónica Obligatoria
- Toda referencia a la atestación legal de BABYLON-60 DEBE utilizar los términos: **"Informe de Evidencias Técnicas"** o **"Expediente técnico para apoyar la Evaluación de Conformidad"** (Technical Evidence Report to Support Conformity Assessment).
- BABYLON-60 es el sustrato proveedor de evidencia criptográfica; la evaluación de conformidad final es un procedimiento externo responsabilidad del deployer o cliente.

## 3. Mapeo de Argumentario Comercial (Régimen de Alto Riesgo)
Cuando el agente estructure un discurso comercial o técnico frente a la regulación europea, debe ceñirse a este encaje exacto:
- **Art. 12 (Registro de Eventos):** BABYLON-60 aporta el historial WORM. El anclaje a la red Bitcoin (L1/L5) es obligatorio como argumento causal, ya que sella la evidencia contra el "Problema del Reloj Falso" mediante termodinámica irreversible (Proof of Work).
- **Art. 14 (Supervisión Humana):** Aportación demostrable mediante compuertas causales (Causal Gating) y cerrojo biométrico físico (Touch ID / Secure Enclave).
- **Art. 15 (Robustez y Ciberseguridad):** Cumplimiento evidenciado por el rechazo determinista (Ring-0) de peticiones indebidas y la apoptosis irreversible (`0xDEAD_6060`) ante fallos de integridad.
- **Art. 25.4 (Acuerdos Escritos en la Cadena de Valor tras el Reglamento (UE) 2026/1744):** `BABYLON Assurance Gateway` opera como interfaz técnica para terceros proveedores de alto riesgo suministrando tres salidas verificables (`execution_evidence`, `assurance_dossier`, `continuous_evidence_monitoring`) sin asumir la condición de proveedor legal del sistema final ni emitir `EU_AI_ACT_CERTIFIED`.

## 4. Grafo de Evidencia Regulatoria (`FL-AIACT-02`), Art. 43 vs. 43.4 y Retención RGPD/EDPB
1. **Prohibición de Invalidación Monolítica y Separación $\operatorname{TechnicalPASS} \not\Rightarrow \operatorname{LegalConformity}$:**
   - Cada afirmación (`babylon.assurance.claim.v1`) debe anclarse selectivamente a sus dimensiones (`intended_purpose_id`, `model_identity`, `artifact_sha256`, `runtime_profile_sha256`, `policy_sha256`) cumpliendo $\operatorname{AcceptEvidence}(c,a) \Rightarrow \operatorname{Bound}(c,a) \land \operatorname{Applicable}(c,a) \land \operatorname{Verified}(c)$.
   - Un cambio técnico puntual invalida solo las aristas afectadas y preserva las evidencias ortogonales válidas. Los cambios dentro de sobres predeterminados (`WITHIN_PREDETERMINED_ENVELOPE`, Art. 43.4) no disparan automáticamente una modificación sustancial (`SUBSTANTIAL_MODIFICATION_REVIEW_REQUIRED`, Art. 43 / Art. 3.23).
   - Para modelos externos cuyos pesos no son verificables (`provider:model:version`), es obligatorio exigir `model_uncertainty_declared = true` y política de contención explícita.
2. **Retención Legal Diferenciada y Compromisos Salados (`BLAKE3_DERIVE_KEY_SALTED`):**
   - **Art. 18 (Documentación técnica del proveedor):** Mínimo **120 meses** (10 años).
   - **Arts. 19 y 26.6 (Registros operativos):** Mínimo **6 meses** bajo control del proveedor o responsable del despliegue.
   - **RGPD y Directrices EDPB sobre Ledgers Inmutables:** Queda estrictamente prohibido almacenar datos personales en crudo o hashes sin sal de PII en ledgers inmutables (`CORTEX` / `babylon-attest`). Toda referencia a datos personales debe usar un compromiso con sal de $\ge 16$ bytes (`BLAKE3_DERIVE_KEY_SALTED`) y custodia separada fuera del ledger para permitir *crypto-shredding* tras el periodo legal sin romper la cadena criptográfica.

## 5. Veto Fail-Closed a Modelos Flash/Mini en Modo LegalTech (INV_C5_LEGALTECH_NO_FLASH)
En cualquier tarea de LegalTech (contratos mercantiles, auditoría de propiedad intelectual, cumplimiento del EU AI Act, deslinde de responsabilidad y análisis de jurisprudencia), el uso de modelos ligeros o de compresión rápida (`flash`, `mini`, `lite`, `nano`, `haiku`, `:free`) queda **formalmente vetado por diseño (Fail-Closed)**:
1. **Asimetría del Coste de Falsificación (Aforismo 5):** Un error inductivo o la mutilación sintáctica de una salvedad (*«No obstante lo dispuesto en...»*) conlleva responsabilidad objetiva y fuga de capital. Prohibido usar modelos Flash incluso en Stage-1 (la segmentación de cláusulas se realiza con parsers deterministas AST/regex, nunca con LLMs ligeros).
2. **Cero Degradación Silenciosa (Anti-Fallback):** Ante agotamiento de cuota (HTTP 429) o modelo no expuesto, queda prohibido conmutar a listas de fallback por *throughput*. El sistema aborta en `0xDEAD_6060`.
3. **Suelo de Selector Ring-4:** En sesiones de LegalTech o del Sanedrín, el suelo mínimo de selector es **Estrato 2 (`Medium`)** o **Estrato 3 (`High`)**. Prohibido recomendar la bajada a Estrato 1 (`Fast / Flash`).
4. **Separación AX-0 ($\text{Cognición} \neq \text{Autoridad} \neq \text{Efecto}$):** Ni siquiera un modelo Pro/Reasoning otorga autoridad jurídica por sí solo. Toda salida exige: (a) citas ancladas con puntero y hash SHA-256/BLAKE3 a fuente primaria (BOE, EUR-Lex, CENDOJ o cláusula literal); (b) verificación formal en Z3 para plazos, cuantificadores y topes de indemnización (*cap/basket*); y (c) firma humana (`HUMAN_SIGNATURE_ONLY`).

```toml
[governance.legaltech]
policy             = "FAIL_CLOSED"
allowed_tiers      = ["estrato_2_medium", "estrato_3_high"]
deny_patterns      = ["flash", "mini", "lite", "nano", "haiku", ":free"]
on_unknown_model   = "DENY"
on_quota_exhausted = "ABORT"
stage1_chunking    = "DETERMINISTIC_AST_ONLY"
citations          = "GROUNDED_HASH_REQUIRED"
authority          = "HUMAN_SIGNATURE_ONLY"
```
