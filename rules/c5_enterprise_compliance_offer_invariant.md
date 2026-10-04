# Invariante de Deslinde Ontológico en Oferta Comercial Enterprise (INV_C5_ENTERPRISE_OFFER)

## 1. Prohibición de Falsa Equivalencia Regulatoria (Silicio ≠ Conformidad Legal)
Queda estrictamente prohibido afirmar en landings comerciales, teasers, presentaciones de producto o documentación enterprise que BABYLON-60 otorga "conformidad total", "cumplimiento automático" o "certificación llave en mano" con el Reglamento (UE) 2024/1689 (EU Artificial Intelligence Act):
* **Vector Silicio (TCB):** BABYLON-60 implementa exclusivamente los *Controles Técnicos Habilitadores* de bajo nivel (trazabilidad WORM RFC 9942 COSE_Sign1, cerrojo biométrico Touch ID P-256 en hardware con reúso cero, y apoptosis determinista fail-stop 0xDEAD_6060).
* **Vector Organizativo (Operador):** La conformidad formal de un sistema de IA de alto riesgo exige que el operador defina políticas de retención, capacitación cognitiva del supervisor, explicabilidad en UI, procedimientos de mitigación y evaluación de sesgos/exactitud estadística del LLM.

## 2. Requisitos Mandatorios de la Oferta Enterprise
Toda superficie comercial enterprise de BABYLON-60 debe articularse mediante la **Matriz de Delimitación Ontológica (Doble Vector)** e incluir sin excepción:
1. **Ficha Técnica del Piloto (PoC):** Duración acotada (30 a 45 días), alcance de infraestructura (hasta 5 nodos) y 3 criterios medibles de aceptación Pass/Fail:
   - *Intercepción Fail-Closed:* 100% de veto determinista ante mutaciones o comandos hostiles/no autorizados (`AUTH_002`, `AUTH_007`).
   - *Trazabilidad Criptográfica:* 100% de efectos válidos sellados con recibos COSE_Sign1 SHA3-256 en SQLite WAL.
   - *Idempotencia ante Caídas:* Recuperación de estado consistente sin corrupción tras parada abrupta `SIGKILL` (`AUTH_003`, `AUTH_006`).
2. **Matriz Formal de SLA:** Tiempos de respuesta y mitigación garantizados por severidad (P1 < 2h 24/7/365, P2 < 4h 8x5 CET, P3 < 24h, P4 < 48h), exclusiones explícitas del TCB (ej. NFS/SMB sin rename atómico) y dimensionamiento del clúster (hasta 25 nodos activos).
3. **Evidencia Pre-Contacto:** Acceso directo a reportes de muestra JSON (`eu_ai_act_compliance_pack.json`) y enlace clicable entre claims técnicas y tests del monorepo (`CLAIMS.toml`).
4. **Desacoplamiento de Embudo:** Cero CTAs de retail/desarrollador individual ("Probar CORTEX") en cabeceras enterprise; foco exclusivo en perfiles decisores: CISO, Platform Engineering y DPO.

## 3. La Doctrina de Responsabilidad del Desplegador (EU AI Act Arts. 26 y 71)
Toda interacción o memorando técnico dirigido a perfiles C-Level (CISO, DPO, CIO, General Counsel) debe anclarse en la asimetría legal del Reglamento (UE) 2024/1689:
* **Escisión Ontológica Proveedor vs. Desplegador:** El proveedor fundacional no responde por las acciones del agente en producción. El *Deployer* (Art. 3.4) asume la responsabilidad jurídica exclusiva y directa (Art. 26) bajo sanciones de hasta 35.000.000 € o el 7% del volumen de negocio mundial (Art. 71).
* **Teorema de Imposibilidad del Guardrail Estocástico:** Queda prohibido aceptar guardrails probabilísticos (Lakera, NeMo, Credo, Holistic) como salvaguarda suficiente. Si el modelo alucina con probabilidad $\epsilon > 0$ y el guardrail falla con probabilidad $\delta > 0$, la probabilidad de catástrofe en base de datos o API es $P = \epsilon \cdot \delta > 0$, garantizando decenas de brechas anuales a escala enterprise ($N \ge 10^7$) y liquidando la excepción de diligencia debida en sede judicial.
* **Garantía en Silicio (Ring-0 / Invariante AX-0):** BABYLON-60 traslada la salvaguarda de la capa estocástica a la capa física de intercepción:
  $$P(\text{mutación causal no autorizada} \mid \text{Ring-0 Touch ID}) \equiv 0$$

## 4. Desarme Dialéctico de Contratos SaaS de la Competencia
En auditorías competitivas y respuestas a objeciones, evidenciar las 4 fracturas contractuales de los vendors de observabilidad y gobernanza (Credo AI, Holistic AI, Lakera, LangSmith):
1. **Cláusula "AS IS":** Excluyen toda garantía de idoneidad técnica o conformidad con el EU AI Act.
2. **Cap de Responsabilidad Irrisorio:** Limitan su responsabilidad a las cuotas pagadas en los últimos 12 meses (o 100 USD), dejando al cliente desprotegido ante multas millonarias de la AEPD/Comisión Europea.
3. **Indemnización Inversa:** Exigen que el cliente indemnice al proveedor ante reclamaciones derivadas del uso de la herramienta.
4. **Exfiltración de Telemetría:** Obligan a enviar trazas, prompts y variables a nubes SaaS en EE.UU., violando el principio de localización soberana y generando no-conformidad con GDPR / NIS2.
