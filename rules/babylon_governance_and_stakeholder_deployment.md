---
name: babylon-governance-and-stakeholder-deployment
description: Invariante de gobernanza corporativa de Babylon-60 y protocolo de despliegue de mínima fricción (1-clic) para stakeholders y desarrollo de negocio.
---

# Invariante de Gobernanza de Babylon-60 y Despliegue a Stakeholders

## 1. Estructura y Roles Canónicos de Babylon-60
En cualquier interacción, redacción de documentos, comunicaciones o planificación estratégica:
* **CEO & Fundador (Operador Raíz):** Máxima autoridad técnica, científica y ejecutiva. Único facultado para decidir, firmar y vincular jurídicamente a la entidad.
* **Segundo de a Bordo (Primer Oficial / Operaciones):** Ignacio Zurita («Nacho Borracho»). Mano derecha operativa en el puente de mando de Babylon-60; salvaguarda la cohesión interna y la ejecución logística de la nave.
* **Dirección de Desarrollo de Negocio (Business Development):** Conduce negociaciones preliminares, abre canales comerciales e interlocución institucional. Carece de poder de firma o vinculación; toda propuesta comercial requiere elevación y ratificación previa del CEO.

## 2. Principio de Cero Fricción para Stakeholders no Técnicos ("Perfil Zoo")
Cuando un stakeholder comercial, inversor o directivo solicite probar, visualizar o evaluar software del ecosistema:
1. **Prohibición de Exigencia Técnica Local:** Queda terminantemente prohibido proponer que clonen repositorios, instalen entornos o paquetes (Rust, Node, Python), ejecuten comandos de terminal o compilen binarios manualmente.
2. **Entrega a un Clic:** La vía prioritaria es siempre un enlace web directo en vivo (despliegue en Cloudflare Pages, Vercel o túnel temporal HTTPS vía `cloudflared`/`ngrok`) operable desde móvil, tablet o portátil.
3. **Alternativa Binaria:** Si se requiere la experiencia de escritorio nativa, se provee exclusivamente un instalador precompilado autoinstalable (`.dmg` para macOS, `.exe`/`.msi` para Windows) alojado en un enlace de descarga directa.

## 3. Desambiguación de Entregables de Babylon-60
* **Babylon Interactive Runtime / Demostrador Web:** `apps/web` (Simulador sexagesimal F60, BFT, Ledger WORM, Inspector EU AI Act).
* **Babylon Sovereign IDE:** `babylon60-ide` (Entorno de escritorio multi-plataforma Tauri v2 + FastAPI).

## 4. Política de Financiación y Capital Soberano de Babylon-60

Toda estrategia de captación de fondos, valoración o relación con inversores se rige estrictamente por estas invariantes:

### 1. La Ronda Semilla Soberana Privada (Vía Ágil de Mercado)
* **Ticket Objetivo:** **600.000 € – 800.000 €** (tope psicológico infranqueable: **1.000.000 €**).
* **Valoración Pre-Money:** **6.000.000 € – 7.500.000 €**.
* **Dilución Permitida:** **8% al 11%** (veto estricto a diluciones $\ge 12\%$).
* **Uso de Fondos:** 18 meses de runway comercial puro (despliegue de los primeros 5 pilotos de 15k € y conversión a licencias On-Premise de 80k–250k €) + blindaje de patentes en la EPO.
* **Cláusulas Anti-Anergía:** Cero liquidación preferente $> 1\text{x}$, cero derechos de veto operativo sobre la arquitectura técnica y cero puestos dominantes en el Consejo de Administración.

### 2. La Vía Institucional Mixta (Bruselas / EIC Accelerator STEP)
* **Subvención a Fondo Perdido (*Grant*):** **2.500.000 €** (dilución = **0%**).
* **Componente de Capital (*Equity* vía BEI / InvestEU):** **Hasta 15.000.000 €** en capital pasivo sin intromisión de gobernanza.
* **Total Tramitado:** **17.500.000 € – 20.000.000 €** mediante consultora a éxito (Zabala / FI Group).

### 3. Cartografía Estricta de Inversores Admitidos vs. Vetados
* **Inversores Permitidos:**
  1. *Family Offices* Industriales y Patrimoniales (Norte y Madrid): Capital paciente que comprende activos de infraestructura en propiedad.
  2. *VCs Especializados en Ciberseguridad / Deep-Tech*: Fondos con tesis de soberanía y EU AI Act (ej. *33N Ventures*, *Adara Ventures*).
  3. *Corporate Venture Capital (CVCs)*: Ramas inversoras de clientes corporativos (banca y aseguradoras) vinculadas a contratos de licencia.
* **Inversores Vetados:** VCs generalistas de "growth" (exigencias de B2C/SaaS de quemar caja y dilución del 25%-30%) y Business Angels aficionados intrusivos.
