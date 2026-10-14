#!/usr/bin/env python3
"""
c5_model_router.py - Auto-Router de Modelos y Triaje Asimétrico para Antigravity.
Clasifica la consulta con Gemini 3.8 Flash y ajusta el nivel al selector de UI.
"""

from typing import Literal
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class RoutingDecision(BaseModel):
    target_model: Literal[
        "gemini-4-argon",
        "gemini-3.8-flash",
        "claude-opus-5.5",
        "claude-sonnet-5.5",
        "gpt-oss-120b",
    ]
    desired_level: Literal["low", "medium", "high"]
    digested_prompt: str = Field(
        description="Prompt técnico limpio, directo y sin ambigüedades listo para ejecutar."
    )
    reason: str = Field(description="Justificación técnica de 1 línea.")

# Mapa real de compatibilidad de niveles del selector UI de Antigravity
VALID_LEVELS = {
    "gemini-4-argon": {"low", "medium", "high"},
    "gemini-3.8-flash": {"high"},          # Solo High (Fast); no tiene Medium ni Low
    "claude-opus-5.5": {"low", "medium", "high"},
    "claude-sonnet-5.5": {"low", "medium", "high"},
    "gpt-oss-120b": {"medium"},            # Fijo en (Medium)
}

FALLBACK_LEVEL = {
    "gemini-3.8-flash": "high",
    "gpt-oss-120b": "medium",
}

def digest_and_route(user_query: str) -> tuple[str, str, str]:
    """Usa Gemini 3.8 Flash para digerir la consulta y elegir modelo + nivel válido."""
    client = genai.Client()
    router_prompt = f"""
    Analiza la siguiente petición y elige el motor más económico capaz de resolverla con éxito:
    - 'gemini-3.8-flash': Tareas rápidas, scripts cortos, dudas directas.
    - 'gpt-oss-120b': Resúmenes, texto general, borradores sin coste premium.
    - 'claude-sonnet-5.5': Implementación de código, UI, refactorización focalizada.
    - 'gemini-4-argon': Contexto masivo, análisis multifichero, debugging complejo.
    - 'claude-opus-5.5': Arquitectura crítica o algoritmos de extrema dificultad.
    
    En 'desired_level', elige siempre 'low' si la ruta es clara, 'medium' si requiere análisis moderado, y 'high' solo en casos críticos.
    
    Petición: {user_query}
    """

    res = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=router_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RoutingDecision,
            max_output_tokens=512,
        ),
    )

    decision: RoutingDecision = res.parsed
    model = decision.target_model
    level = decision.desired_level

    # Clamping forzado si el nivel no existe en el selector del modelo
    if level not in VALID_LEVELS[model]:
        level = FALLBACK_LEVEL[model]

    return model, level, decision.digested_prompt

if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Revisa por qué falla el tipado en auth.py"
    print(f"[c5_model_router] Digeriendo consulta: {query}")
    try:
        m, l, p = digest_and_route(query)
        print(f"🔄 [ROTAR A: {m} | NIVEL: {l}]")
        print(f"Pre-Flight Prompt:\n{p}")
    except Exception as e:
        print(f"Error en triaje: {e}")
