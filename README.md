
Aegis: Protocol-Guided Emergency Stabilization

Aegis is an offline-first, zero-hallucination medical triage system designed for rural environments where cellular connectivity and professional medical intervention are unavailable.

Features

Deterministic Triage: Uses a custom GBNF grammar-locked LLM to extract triage variables (severe_bleeding, unconscious, breathing_difficulty) without conversation.

Protocol Guidance: Maps symptoms directly to WHO rural first-aid guidelines.

Offline Escalation: Uses Haversine spatial geometry to route patients to the nearest trauma facility without internet or GPS services.

Prerequisites

A CPU-only compute environment (Windows/Linux).

llama.cpp (or llama-cli) installed and in your PATH.

Qwen2.5-3B-Instruct (GGUF format).

How to run

Download the model file from Hugging Face.

Place the model file in the project root.

Run the system:

python aegis.py


Input emergency scenarios and follow the printed protocols.

License

MIT
