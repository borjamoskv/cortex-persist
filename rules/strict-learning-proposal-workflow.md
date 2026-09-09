---
name: strict-learning-proposal-workflow
description: Regla estricta que prohíbe la modificación directa de habilidades (Skills) y Reglas (Rules) sin una propuesta previa aprobada.
---

# Strict Learning Proposal Workflow Rule

**CRITICAL GUARDRAIL**: You must NEVER directly create, modify, or delete any file within the `~/.gemini/config/skills/`, `~/.gemini/config/rules/`, or `~/.gemini/config/plugins/` directories without explicit prior user approval via a learning proposal.

## Workflow Requirements

Whenever the user asks to create, update, or improve a rule, skill, or learned behavior (whether triggered via the `/learn` command or natural language like "improve it"):

1. **DO NOT** execute tool calls (`write_to_file`, `replace_file_content`, etc.) targeting the actual configuration files immediately.
2. **ALWAYS** create or update an artifact named `learning_proposal.md`.
3. Set `request_feedback = true` in the `ArtifactMetadata` of the `learning_proposal.md` file.
4. The proposal artifact must include:
   - Classification (Rule vs Skill).
   - Rationale for the change.
   - The exact proposed content or diff.
5. **HALT EXECUTION** and wait for the user to click the "Proceed" button or provide manual approval.
6. **ONLY AFTER** explicit approval is granted, proceed to execute the tool calls that modify the files in `~/.gemini/config/`.

This rule acts as an unbreachable constraint to prevent unauthorized drift in the agent's core configurations.
