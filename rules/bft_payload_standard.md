# Estándar de Payloads BFT (Zero-Rhetoric Context)

Cuando el Transductor deba inyectar un payload en un asalto BFT (ej. modificando el script `detonate_bft_ultrathink.py`), NUNCA debe usar cadenas estáticas o genéricas (como "LEGION_1_SIGUE"). 

DEBE sintetizar el contexto semántico de la conversación reciente (ej. límites físicos evaluados, teoremas discutidos o capturas de pantalla analizadas) y formatearlo estrictamente en **INGLÉS** (cumpliendo con el Axioma Ω6 de Bifurcación Lingüística), en **UPPERCASE con guiones bajos**, concatenado con la firma de la operación solicitada.

**Ejemplo de Formato:** 
`MISSION_[MAIN_TOPIC]_[KEY_VARIABLES]_[OPERATION]`

**Ejemplo Real:** 
`MISSION_PHYSICAL_LIMITS_MAC_M3_PRO_18GB_ULTRATHINK`

Esto garantiza que, aunque el canal de respuesta degenere en silencio absoluto en cumplimiento del **Axioma Ω3**, la "intención" del operador y el contexto de la detonación queden inyectados y auditados permanentemente en el Ledger inmutable de SQLite WAL.
