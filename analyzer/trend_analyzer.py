import math
from statistics import mean, stdev


# ----------------------------
# CONFIGURATION
# ----------------------------

DEFAULT_CONFIG = {
    "nesting_threshold": 3,
    "cc_safe_range": 3,
    "length_safe_range": 6,
    "weights": {
        "nesting": 0.4,
        "cyclomatic": 0.4,
        "length": 0.2
    }
}

# This function computes a structural discipline score (0–100)
# Higher score = cleaner, more controlled structure
def calculate_structural_score(metrics: dict):
    # Extract metrics safely
    depth = metrics.get("max_nesting_depth", 0)
    complexity = metrics.get("cyclomatic_complexity", 0)
    avg_len = metrics.get("avg_function_length", 0)
    func_count = metrics.get("function_count", 0)

    # Penalize excessive nesting (too many nested branches)
    depth_penalty = min(depth * 5, 30)

    # Penalize high branching complexity
    complexity_penalty = min(complexity * 2, 40)

    # Penalize overly long functions
    length_penalty = min(avg_len / 2, 30)

    # Reward modular design (multiple small functions)
    modularity_bonus = 0
    if func_count >= 3 and avg_len < 25:
        modularity_bonus = 5
    if func_count >= 6 and avg_len < 20:
        modularity_bonus = 10

    # Base score calculation
    raw_score = 100 - (depth_penalty + complexity_penalty + length_penalty)

    # Add reward bonus
    final_score = raw_score + modularity_bonus

    # Clamp score between 0 and 100
    return max(min(round(final_score, 2), 100), 0)

# This function evaluates short-term structural change
# but now also compares against the initial baseline
def analyze_trend(history: list):
    # Need at least 2 submissions
    if len(history) < 2:
        return "Insufficient data for trend analysis."

    # Most recent and previous entries
    prev = history[-2]
    curr = history[-1]

    # Structural scores (already computed and stored)
    prev_score = prev.get("structural_score", 0)
    curr_score = curr.get("structural_score", 0)

    # Baseline is the very first submission
    baseline_score = history[0].get("structural_score", 0)

    # Short-term comparison
    delta = curr_score - prev_score

    # Long-term comparison to baseline
    baseline_delta = curr_score - baseline_score

    if delta > 2:
        short_term = "Improving recently."
    elif delta < -2:
        short_term = "Declining recently."
    else:
        short_term = "Stable recently."

    if baseline_delta > 5:
        long_term = "Overall structural growth since baseline."
    elif baseline_delta < -5:
        long_term = "Overall structural decline since baseline."
    else:
        long_term = "Near baseline structure."

    return f"{short_term} {long_term}"


# This function analyzes long-term improvement trend
# It calculates average score change across the session
def calculate_growth_velocity(history: list):
    # Require at least 3 submissions for meaningful velocity
    if len(history) < 3:
        return "Not enough data to estimate growth velocity."

    # Extract structural scores from history
    scores = [entry.get("structural_score", 0) for entry in history]

    # Compute score differences between consecutive submissions
    deltas = []
    for i in range(1, len(scores)):
        deltas.append(scores[i] - scores[i - 1])

    # Average improvement/regression amount
    avg_delta = sum(deltas) / len(deltas)

    # Classify growth pattern
    if avg_delta > 2:
        return "Rapid structural improvement."
    elif avg_delta > 0:
        return "Gradual structural improvement."
    elif avg_delta == 0:
        return "No structural change trend."
    elif avg_delta > -2:
        return "Mild structural regression."
    else:
        return "Significant structural regression."

# This function estimates how reliable our structural analysis is
# More submissions = higher confidence
def calculate_signal_confidence(history: list):
    submission_count = len(history)

    # Very low sample size
    if submission_count < 3:
        return "Low confidence (insufficient data)."

    # Medium sample size
    elif submission_count < 7:
        return "Moderate confidence (limited history)."

    # Good sample size
    elif submission_count < 15:
        return "High confidence (solid behavioral sample)."

    # Strong statistical pattern
    else:
        return "Very high confidence (strong behavioral pattern established)."

# ----------------------------
# COGNITIVE PROFILE INFERENCE
# ----------------------------

def infer_cognitive_profile(history):

    if len(history) < 3:
        return []

    avg_lengths = [h["avg_function_length"] for h in history]
    nestings = [h["max_nesting_depth"] for h in history]
    function_counts = [h["function_count"] for h in history]

    profile = []

    if mean(avg_lengths) < 5 and function_counts[-1] > function_counts[0]:
        profile.append("Micro-function architect tendency")

    if mean(nestings) > 3:
        profile.append("Deep nesting bias")

    if mean(avg_lengths) > 10:
        profile.append("Monolithic construction tendency")

    return profile
