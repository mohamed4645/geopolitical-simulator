from __future__ import annotations

from typing import Dict, List

from models.state import GameState


def normalize(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def update_kpi(state: GameState, key: str, delta: float) -> None:
    state.kpis[key] = normalize(state.kpis.get(key, 50.0) + delta)


def apply_lag_queue(state: GameState) -> None:
    if not state.lag_queue:
        return

    still_pending = []
    for effect in state.lag_queue:
        if effect["resolve_turn"] <= state.turn:
            for key, delta in effect["effects"].items():
                if key in state.kpis:
                    update_kpi(state, key, delta)
            if "hidden_effects" in effect:
                for key, delta in effect["hidden_effects"].items():
                    state.hidden[key] = normalize(state.hidden.get(key, 50.0) + delta)
            state.event_log.append(effect["description"])
        else:
            still_pending.append(effect)
    state.lag_queue = still_pending


def sector_score_from_values(values: List[float]) -> float:
    if not values:
        return 50.0
    return sum(values) / len(values)


def compute_sector_summary(state: GameState) -> Dict[str, float]:
    summary: Dict[str, float] = {}
    for sector_name, slug in zip(
        [
            "Macroeconomics & Public Finance",
            "Military Defense & National Security",
            "Foreign Policy & Geopolitics",
            "Tech, Science & Digital Sovereignty",
            "Health, Society & Human Capital",
            "Agriculture, Food & Water Security",
            "Energy, Mining & Infrastructure",
            "Governance, Judiciary & Internal Politics",
            "Tourism, Aviation & Foreign Trade",
            "Crisis Management, Environment & Disasters",
        ],
        ["macro", "security", "diplomacy", "technology", "society", "food", "energy", "governance", "trade", "crisis"],
    ):
        values = []
        for key, value in state.metrics.items():
            if key.startswith(f"{sector_name.lower()}::"):
                values.append(value)
        if not values:
            values = [float(state.kpis.get(k, 50.0)) for k in [
                "gdp_growth",
                "military_readiness",
                "international_law",
                "digital_sovereignty",
                "public_approval",
                "food_security",
                "energy_security",
                "governance_quality",
                "trade_balance",
                "environmental_health",
            ]]
        summary[sector_name] = sector_score_from_values(values)
    return summary


def resolve_budget_allocations(state: GameState, allocations: Dict[str, float]) -> None:
    boost_map = {
        "macro": ("gdp_growth", 0.25),
        "security": ("military_readiness", 0.30),
        "diplomacy": ("international_law", 0.22),
        "technology": ("digital_sovereignty", 0.28),
        "society": ("public_approval", 0.24),
        "food": ("food_security", 0.26),
        "energy": ("energy_security", 0.25),
        "governance": ("governance_quality", 0.20),
        "trade": ("trade_balance", 0.18),
        "crisis": ("crisis_resilience", 0.23),
    }

    for key, share in allocations.items():
        if key in boost_map:
            kpi_name, factor = boost_map[key]
            delta = (share / 10.0) * factor * 4.5
            update_kpi(state, kpi_name, delta)

    state.kpis["budget_balance"] = normalize(state.kpis.get("budget_balance", 60.0) + (sum(allocations.values()) / 100.0) * 2.5 - 2.0)


def advance_game_turn(state: GameState) -> None:
    state.turn += 1
    state.kpis["gdp_growth"] = normalize(state.kpis.get("gdp_growth", 50.0) + 0.5)
    state.hidden["implementation_lag_queue"] = max(0.0, state.hidden.get("implementation_lag_queue", 0.0) - 1.0)
    state.event_log.append(f"Turn {state.turn} begins; strategic posture recalculated.")


def evaluate_turn(state: GameState, allocations: Dict[str, float]) -> Dict[str, float]:
    apply_lag_queue(state)
    resolve_budget_allocations(state, allocations)

    state.kpis["inflation"] = normalize(state.kpis.get("inflation", 50.0) + (state.hidden.get("public_discontent", 0.0) / 100.0) * 3.5 - (state.kpis.get("budget_balance", 50.0) / 100.0) * 2.0)
    state.kpis["debt_ratio"] = normalize(state.kpis.get("debt_ratio", 50.0) + (state.kpis.get("inflation", 50.0) / 20.0) - (state.kpis.get("gdp_growth", 50.0) / 18.0))
    state.kpis["public_approval"] = normalize(state.kpis.get("public_approval", 50.0) + (state.kpis.get("budget_balance", 50.0) / 30.0) - (state.hidden.get("public_discontent", 0.0) / 25.0) - (state.kpis.get("inflation", 50.0) / 35.0))
    state.kpis["sectarian_stability"] = normalize(state.kpis.get("sectarian_stability", 50.0) + (state.kpis.get("governance_quality", 50.0) / 25.0) - (state.hidden.get("religious_friction", 0.0) / 20.0))
    state.kpis["international_law"] = normalize(state.kpis.get("international_law", 50.0) + (state.kpis.get("diplomatic_weight", 50.0) / 35.0) - (state.hidden.get("international_law_violations", 0.0) / 18.0))
    state.kpis["environmental_health"] = normalize(state.kpis.get("environmental_health", 50.0) - (state.hidden.get("ecological_damage", 0.0) / 30.0) + (state.kpis.get("crisis_resilience", 50.0) / 35.0))
    state.hidden["public_discontent"] = normalize(state.hidden.get("public_discontent", 20.0) + max(0.0, state.kpis["inflation"] - 50.0) / 12.0 - (state.kpis["public_approval"] / 40.0))
    state.hidden["religious_friction"] = normalize(state.hidden.get("religious_friction", 25.0) + state.kpis["sectarian_stability"] / 40.0 - state.kpis["governance_quality"] / 32.0)
    state.hidden["proxy_war_influence"] = normalize(state.hidden.get("proxy_war_influence", 20.0) + max(0.0, state.kpis["military_readiness"] - 65.0) / 20.0)
    state.hidden["international_law_violations"] = normalize(state.hidden.get("international_law_violations", 18.0) + (state.hidden.get("proxy_war_influence", 0.0) / 25.0) - (state.kpis.get("international_law", 50.0) / 40.0))

    sector_summary = compute_sector_summary(state)
    state.event_log.append(f"Turn {state.turn} evaluation completed. Aggregate strategic posture: {sum(sector_summary.values()) / len(sector_summary):.1f}/100.")
    return sector_summary
