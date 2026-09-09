# CORTEX PERSIST

> **Sovereign Cognitive Core, Procedural Skills & Epistemic Invariants**  
> *Sustrato de persistencia cognitiva para el entorno agéntico Antigravity / Ecosistema C5-REAL.*

---

## 🏛️ Topología del Sistema

Este repositorio alberga la memoria procedural, heurísticas de razonamiento y herramientas operativas del operador:

```
~/.gemini/config/
├── AGENTS.md          # Directivas globales, perfiles de agente y protocolos de inferencia
├── rules/             # Invariantes sistémicas, marcos de gobernanza y axiomas C5-REAL
├── skills/            # Habilidades agénticas de alta exergía (DFIR, matemáticas, audio, devsecops)
├── plugins/           # Integraciones modulares y toolsets de desarrollo
├── mcp_config.json    # Configuración de pasarelas Model Context Protocol (MCP)
└── .gitignore         # Blindaje estricto de secretos y estados volátiles
```

---

## 🛡️ Invariantes de Seguridad y Soberanía

* **Zero-Leak Invariant:** Las credenciales de máquina (`config.json`), sesiones efímeras (`projects/`) y cachés en memoria (`.cortex/`) quedan terminantemente excluidas del control de versiones.
* **Separación de Capas (MASS):** Cortex Persist gestiona el **conocimiento procedimental y operativo** mutable, mientras que [`BABYLON-60`](https://github.com/borjamoskv/BABYLON-60) opera como el **ledger criptográfico inmutable** (*tamper-evident WAL*) para auditoría de acciones.

---

## ⚙️ Sincronización y Mantenimiento

Para sincronizar actualizaciones tras invocar `/learn` o refactorizar habilidades:

```bash
git add skills/ rules/ plugins/ AGENTS.md
git commit -m "feat(cortex): update procedural skills & rules"
git push origin main
```
