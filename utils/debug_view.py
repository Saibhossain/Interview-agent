def format_state_debug(state) -> str:
    if not state or not getattr(state, "values", None):
        return "No state available."

    values = state.values
    lines = ["========== GRAPH STATE DEBUG =========="]
    for key, value in values.items():
        lines.append(f"{key}: {value}")
    lines.append("======================================")
    return "\n".join(lines)