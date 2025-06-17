from collections import defaultdict

# Simple in-memory context per client_id
session_contexts = defaultdict(list)

def get_context(client_id: str):
    return session_contexts[client_id]

def add_to_context(client_id: str, role: str, message: str):
    session_contexts[client_id].append({"role": role, "message": message})

def reset_context(client_id: str):
    session_contexts[client_id] = []
