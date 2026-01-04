from collections import defaultdict

DOMAIN_WEIGHTS = {
    "Relationship": {
        "Load": 1.4,
        "Feedback Safety": 1.4,
        "Signal Clarity": 1.1,
        "Incentives": 1.2,
        "Baseline Stability": 0.8,
        "Constraints": 0.8,
        "Trajectory": 1.0,
    },
    "Financial": {
        "Baseline Stability": 1.5,
        "Constraints": 1.5,
        "Load": 1.3,
        "Signal Clarity": 1.2,
        "Feedback Safety": 0.9,
        "Incentives": 1.1,
        "Trajectory": 0.9,
    },
    "Life Path": {
        "Trajectory": 1.6,
        "Signal Clarity": 1.3,
        "Incentives": 1.3,
        "Load": 1.2,
        "Feedback Safety": 1.0,
        "Baseline Stability": 0.9,
        "Constraints": 0.9,
    },
}

DOMAIN_OUTPUTS = {
    "Relationship": {
        "missing": "Unmodeled emotional and cognitive load consuming relational capacity",
        "distortion": "Capacity shortfall is misread as intent, triggering defensiveness and erosion",
        "lever": "Name load before assigning meaning; no interpretation without capacity context",
    },
    "Financial": {
        "missing": "Baseline instability and constraint pressure consuming planning bandwidth",
        "distortion": "Short-horizon survival behavior is misread as irresponsibility",
        "lever": "Stabilize one constraint before optimizing income or behavior",
    },
    "Life Path": {
        "missing": "Signal ambiguity combined with incentive pressure",
        "distortion": "Motion is mistaken for progress; endurance replaces direction",
        "lever": "Audit incentives and constraints before optimizing effort",
    },
}

def evaluate(responses, domain):
    buckets = defaultdict(list)

    for q, score in responses.items():
        buckets[q["variable"]].append(score * q["weight"])

    averaged = {k: sum(v) / len(v) for k, v in buckets.items()}
    weights = DOMAIN_WEIGHTS[domain]

    weighted = {
        k: averaged.get(k, 0) * weights.get(k, 1.0)
        for k in averaged
    }

    overall = sum(weighted.values()) / len(weighted)

    if overall >= 3:
        risk = "High"
    elif overall >= 2:
        risk = "Moderate"
    else:
        risk = "Low"

    top_drivers = sorted(weighted.items(), key=lambda x: x[1], reverse=True)[:3]

    outputs = DOMAIN_OUTPUTS[domain]

    return {
        "risk": risk,
        "missing_variable": outputs["missing"],
        "distortion": outputs["distortion"],
        "lever": outputs["lever"],
        "drivers": top_drivers,
    }
