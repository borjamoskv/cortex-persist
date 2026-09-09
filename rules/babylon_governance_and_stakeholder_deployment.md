---
name: babylon-governance-and-stakeholder-deployment
description: Invariante de gobernanza corporativa de Babylon-60 y protocolo de despliegue de mínima fricción (1-clic) para stakeholders y desarrollo de negocio.
---

# Invariante de Gobernanza de Babylon-60 y Despliegue a Stakeholders

## 1. Estructura y Roles Canónicos de Babylon-60
En cualquier interacción, redacción de documentos, comunicaciones o planificación estratégica:
* **CEO & Fundador:** **Borja Fernández Angulo** (`borjamoskv`). Máxima autoridad técnica, científica y ejecutiva. Único facultado para decidir, firmar y vincular jurídicamente a la entidad.
* **Director de Desarrollo de Negocio (Business Development Director):** **Nacho** (Ignacio Zurita). Conduce negociaciones preliminares, abre canales comerciales e interlocución institucional. Carece de poder de firma o vinculación; toda propuesta comercial requiere elevación y ratificación previa del CEO.
* **Dirección Letrada:** **D. Ricardo Muñiz Zurita** (**Akorn Abogados**). Blindaje contractual, propiedad industrial, secreto empresarial, gobernanza jurídica y defensa procesal.

## 2. Principio de Cero Fricción para Stakeholders no Técnicos ("Perfil Zoo")
Cuando un stakeholder comercial, inversor o directivo (incluido Nacho) solicite probar, visualizar o evaluar software del ecosistema:
1. **Prohibición de Exigencia Técnica Local:** Queda terminantemente prohibido proponer que clonen repositorios, instalen entornos o paquetes (Rust, Node, Python), ejecuten comandos de terminal o compilen binarios manualmente.
2. **Entrega a un Clic:** La vía prioritaria es siempre un enlace web directo en vivo (despliegue en Cloudflare Pages, Vercel o túnel temporal HTTPS vía `cloudflared`/`ngrok`) operable desde móvil, tablet o portátil.
3. **Alternativa Binaria:** Si se requiere la experiencia de escritorio nativa, se provee exclusivamente un instalador precompilado autoinstalable (`.dmg` para macOS, `.exe`/`.msi` para Windows) alojado en un enlace de descarga directa.

## 3. Desambiguación de Entregables de Babylon-60
* **Babylon Interactive Runtime / Demostrador Web:** `apps/web` (Simulador sexagesimal F60, BFT, Ledger WORM, Inspector EU AI Act).
* **Babylon Sovereign IDE:** `babylon60-ide` (Entorno de escritorio multi-plataforma Tauri v2 + FastAPI).
