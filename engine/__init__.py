from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


SECTOR_NAMES = [
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
]

SECTOR_SLUGS = [
    "macro",
    "security",
    "diplomacy",
    "technology",
    "society",
    "food",
    "energy",
    "governance",
    "trade",
    "crisis",
]

PRIMARY_KPIS = {
    "gdp_growth",
    "inflation",
    "debt_ratio",
    "military_readiness",
    "public_approval",
    "sectarian_stability",
    "international_law",
    "food_security",
    "energy_security",
    "digital_sovereignty",
    "governance_quality",
    "trade_balance",
    "tourism_demand",
    "environmental_health",
    "crisis_resilience",
    "budget_balance",
    "currency_stability",
    "population_health",
    "logistics_capacity",
    "eez_control",
}

HIDDEN_METRICS = {
    "public_discontent",
    "religious_friction",
    "international_law_violations",
    "ecological_damage",
    "proxy_war_influence",
    "implementation_lag_queue",
}


@dataclass
class AIActor:
    name: str
    ideology: str
    aggression: float
    influence: float
    military_strength: float
    trade_volume: float
    diplomatic_weight: float
    risk_profile: float


@dataclass
class GameState:
    country_name: str
    turn: int = 1
    random_seed: int = 42
    kpis: Dict[str, float] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    hidden: Dict[str, float] = field(default_factory=dict)
    lag_queue: List[dict] = field(default_factory=list)
    ai_actors: Dict[str, AIActor] = field(default_factory=dict)
    event_log: List[str] = field(default_factory=list)
    scenario_history: List[str] = field(default_factory=list)
    policy_directives: List[str] = field(default_factory=list)
    scenarios: List[dict] = field(default_factory=list)


def generate_metric_catalog() -> Dict[str, Dict[str, float]]:
    catalog: Dict[str, Dict[str, float]] = {}
    for sector, slug in zip(SECTOR_NAMES, SECTOR_SLUGS):
        catalog[sector] = {}
        for idx in range(50):
            metric_name = f"{slug}_{idx + 1}"
            catalog[sector][metric_name] = 50.0
    return catalog


def build_country_baseline(country_name: str) -> GameState:
    state = GameState(country_name=country_name)
    catalog = generate_metric_catalog()
    for sector_name, metric_map in catalog.items():
        for metric_name, value in metric_map.items():
            state.metrics[f"{sector_name.lower()}::{metric_name}"] = value

    sector_baselines = {
        "Macroeconomics & Public Finance": {"gdp_growth": 2.3, "inflation": 4.1, "debt_ratio": 62.0, "currency_stability": 72.0, "budget_balance": 67.0},
        "Military Defense & National Security": {"military_readiness": 68.0, "logistics_capacity": 71.0, "eez_control": 74.0, "security": 66.0},
        "Foreign Policy & Geopolitics": {"international_law": 62.0, "diplomatic_weight": 63.0, "trade_balance": 60.0, "global_influence": 64.0},
        "Tech, Science & Digital Sovereignty": {"digital_sovereignty": 70.0, "innovation_capacity": 68.0, "research_output": 73.0},
        "Health, Society & Human Capital": {"population_health": 76.0, "public_approval": 64.0, "sectarian_stability": 70.0},
        "Agriculture, Food & Water Security": {"food_security": 74.0, "water_security": 72.0, "food_production": 78.0},
        "Energy, Mining & Infrastructure": {"energy_security": 70.0, "infrastructure_quality": 67.0, "supply_chain_stability": 69.0},
        "Governance, Judiciary & Internal Politics": {"governance_quality": 68.0, "rule_of_law": 66.0, "state_capacity": 74.0},
        "Tourism, Aviation & Foreign Trade": {"tourism_demand": 60.0, "aviation_capacity": 64.0, "trade_balance": 58.0},
        "Crisis Management, Environment & Disasters": {"crisis_resilience": 65.0, "environmental_health": 68.0, "disaster_readiness": 70.0},
    }

    for sector_name, metric_values in sector_baselines.items():
        for metric_name, value in metric_values.items():
            state.kpis[metric_name] = value

    state.hidden = {
        "public_discontent": 28.0,
        "religious_friction": 25.0,
        "international_law_violations": 18.0,
        "ecological_damage": 22.0,
        "proxy_war_influence": 20.0,
        "implementation_lag_queue": 0.0,
    }

    state.ai_actors = {
        "United States": AIActor("United States", "liberal democracy", 55.0, 88.0, 82.0, 76.0, 86.0),
        "China": AIActor("China", "state-capitalist autocracy", 68.0, 86.0, 88.0, 82.0, 79.0),
        "Russia": AIActor("Russia", "revisionist autocracy", 73.0, 68.0, 79.0, 52.0, 62.0),
        "Regional Block": AIActor("Regional Block", "fragmented coalition", 61.0, 60.0, 64.0, 55.0, 58.0),
    }

    state.event_log.append(f"Global strategic baseline established for {country_name}.")
    return state
