def detect_patterns(metrics: dict):
    insights = []
    profile = []

    depth = metrics.get("max_nesting_depth", 0)
    avg_len = metrics.get("avg_function_length", 0)
    complexity = metrics.get("cyclomatic_complexity", 0)
    func_count = metrics.get("function_count", 0)

    # Structural observations
    if depth >= 3:
        insights.append(
            "Deep nesting detected. Consider simplifying control flow.")

    if avg_len > 30:
        insights.append(
            "Large function size detected. Consider breaking into smaller units."
        )

    if complexity > 10:
        insights.append(
            "High cyclomatic complexity. Logic may be difficult to maintain.")

    if func_count == 0:
        insights.append(
            "No functions detected. Code may be script-style and less modular."
        )

    # Cognitive style classification
    if depth >= 3 and complexity > 10:
        profile.append(
            "Over-structurer: Tends toward layered logic and heavy branching.")

    if avg_len > 40:
        profile.append(
            "Monolithic builder: Prefers large, centralized functions.")

    if func_count > 5 and avg_len < 15:
        profile.append(
            "Micro-modular thinker: Breaks problems into small abstractions.")

    if complexity < 5 and depth <= 1:
        profile.append("Linear thinker: Prefers straightforward control flow.")

    return {"insights": insights, "cognitive_profile": profile}
