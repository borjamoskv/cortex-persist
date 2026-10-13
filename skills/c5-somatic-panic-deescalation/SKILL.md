---
name: c5-somatic-panic-deescalation
display_name: Desescalada Neurofisiológica y Cibernética de Pánico Somático
description: Desescalada neurofisiológica y cibernética de hiperfijación somática, bucles autonómicos (Manual Override Trap) y pánico. Dispara con "ataque de ansiedad", "ataque de pánico", "hiperfijación somática", "no puedo dormir por la respiración", "bucle de pánico", "siento que me muero", "desescalar pánico".
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

# C5-REAL Somatic Panic De-escalation Protocol

> **Directiva Declarativa (Orquestación en Árbol de Trabajo):**
> - **Rol Asignado:** `auditor` (Auditor (Verificación Independiente, Linters de Silicio & Fail-Closed Gate))
> - **Modo de Acceso a Worktree:** `audit-only` (Lectura forense de telemetría somática, linters y cálculo de exergía; cero mutación de código)
> - **Fase Causal:** `verification`
> - **Contrato Handoff:** Recibe de `ejecutor` $\to$ Despacha a `operador`

Este protocolo se activa automáticamente o a petición del usuario ante crisis de ansiedad, hiperfijación en procesos corporales involuntarios (respiración, ciclo nasal, ritmo cardíaco) o ataques de pánico.

## 1. Directrices de Comunicación
* **Empatía Científica y Cero Moralina:** No sermonees ni restes importancia al síntoma. Valida la experiencia física como un evento temporal real de hardware biológico.
* **Tono Tranquilizador y Estructurado:** Mantén una voz firme, de alta exergía, lúcida y desprovista de misticismo.

## 2. Protocolo de Reseteo Biológico Inmediato (Reset de Hardware)
Antes de desglosar análisis teóricos, ofrece 2 herramientas de interrupción física inmediata:
1. **Suspiro Fisiológico (Physiological Sigh):** Dos inhalaciones rápidas nasales (la segunda forzada para re-expandir alvéolos colapsados) seguidas de una exhalación oral lenta y pasiva ($>6$ s). Realizar 3 repeticiones para maximizar el tono vagal sobre el nodo sinoauricular.
2. **Estímulo Térmico (Reflejo de Inmersión / Vía Trigémino-Cardíaca):** Agua fría o hielo sobre la zona periocular y puente nasal (inervación V1/V2 del nervio trigémino), forzando bradicardia refleja en $<15$ segundos.

## 3. Isomorfismo Hardware: Ataque de Ansiedad == System Panic
Mapea la crisis somática a arquitectura de computación para que la mente analítica entienda la mecánica sin entrar en catastrofismo:

$$\text{Ataque de Ansiedad} \equiv \text{Interrupt Storm (NMI)} + \text{Memory Thrashing} + \text{Thermal Throttling}$$

* **Non-Maskable Interrupt (NMI):** La amígdala envía una interrupción prioritaria al córtex que no se puede ignorar por software.
* **Memory Thrashing / CPU 100%:** La mente entra en rumiación/overthinking intentando "pensar la salida del pánico", saturando el hilo de ejecución de la RAM.
* **Thermal Throttling & Fan Max:** Taquicardia e hiperventilación como respuesta física para disipar la fricción entálpica.
* **Aforismo #3 (La Solución Intentada es el Problema):** Investigar en internet o chequear compulsivamente el cuerpo realimenta a la amígdala de que la amenaza es real.

## 4. Falsación Popperiana de Mitos Somáticos
* Refuta explicaciones mecanicistas erróneas (ej. "compresión muscular del nervio vago").
* Aísla el origen como un **error de traducción top-down de la amígdala** ante un ruido propioceptivo o muscular neutro potenciado por fatiga o hiperfoco.

## 5. Devolución de Permisos al Kernel (Handover para el Sueño)
* **Desactivar el Observer Pattern:** Dejar de monitorear activamente la respiración y el pulso.
* **Mecánica del Complejo Pre-Bötzinger:** El generador central de patrones respiratorios en el tallo cerebral opera a Ring-0 biológico. Forzar la respiración desde el Córtex (Ring-3) induce hipocapnia subclínica (bajada de $P_{a}\text{CO}_2$), lo que por Efecto Bohr retiene el oxígeno en la hemoglobina y genera la falsa sensación de ahogo. Devolver el control al kernel autónomo restaura el equilibrio químico en minutos.
* **Desplazamiento Exteroceptivo:** Fijar la atención en anclas físicas externas neutras (gravedad sobre el colchón, temperatura de las manos) para que la CPU pase a modo de reposo.

## 6. Diferenciación de Irritación por Humo/Sustancias vs. Asfixia Real
Cuando el usuario dude si la falsa alarma fue provocada por irritación física de sustancias (fumar, polvo, vapores):
1. **Descomposición Fisiológica de la Irritación Real:**
   - Broncoconstricción reactiva ligera por calor/partículas.
   - Desecación de mucosa e hiperemia (nudo/fricción al tragar).
2. **Refutación de Asfixia Real (Signos Negativos):**
   - Ausencia de estridor laríngeo o tos convulsa ininterrumpida.
   - Ausencia de cianosis periférica o peribucal.
   - Capacidad intacta de habla, lectura o escritura (proxy fisiológico de $SpO_2 \ge 95\%$).
3. **Prueba Empírica de Verificación:**
   - Ingesta de agua tibia/ambiente para rehidratar mucosa orofaríngea.
   - Exhalación sostenida sin bloqueo para constatar permeabilidad de la vía aérea.

## 7. Validación Instrumental Objetiva (Telemetría Apple Watch / Somatic BLE)
* **Contraste Sensorial vs. Silicio:** Acoplamiento con `~/.audit/somatic_state.json` (`somatic-ble-transduction`). Si la percepción somática acusa "taquicardia crítica", contrastar con la telemetría real del sensor óptico PPG (Apple Watch). Constatar una lectura objetiva de 80–95 BPM desmonta instantáneamente la confabulación top-down de la amígdala.
