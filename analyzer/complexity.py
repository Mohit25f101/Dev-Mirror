from radon.complexity import cc_visit


def calculate_complexity(code: str) -> dict:
    try:
        results = cc_visit(code)
    except Exception:
        return {"cyclomatic_complexity": 0}

    if not results:
        return {"cyclomatic_complexity": 0}

    avg_complexity = sum(block.complexity for block in results) / len(results)

    return {
        "cyclomatic_complexity": round(avg_complexity, 2)
    }
