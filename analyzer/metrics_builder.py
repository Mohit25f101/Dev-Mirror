from analyzer.ast_parser import parse_code
from analyzer.complexity import calculate_complexity
from analyzer.pattern_detector import detect_patterns


def analyze_code(code: str) -> dict:
    ast_metrics = parse_code(code)

    if "error" in ast_metrics:
        return ast_metrics

    complexity_metrics = calculate_complexity(code)

    combined_metrics = {**ast_metrics, **complexity_metrics}

    pattern_data = detect_patterns(combined_metrics)
    combined_metrics.update(pattern_data)

    return combined_metrics
 