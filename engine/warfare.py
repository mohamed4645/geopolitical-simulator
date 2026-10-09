from __future__ import annotations

import random
from typing import Dict, List

from models.state import GameState


EVENT_POOL = [
    {
        "id": "food_riot",
        "title": "Food Riot and Urban Instability",
        "condition": lambda state: state.kpis.get("inflation", 50) > 15 and state.kpis.get("sectarian_stability", 50) < 45,
        "description_templates": [
            "Rising prices are pushing urban residents into spontaneous protest as food queues collapse.",
            "Market shortages and a toxic rumor campaign have turned bread shortages into a political flashpoint.",
            "The capital is boiling over as public anger compounds with neighborhood-level unrest.",
        ],
        "impact_preview": "Public panic, food shortages, and delayed relief packages.",
        "options": [
            {"label": "Open emergency grain reserves and mobilize local councils", "effects": {"food_security": 10, "public_approval": 3}, "budget_cost": 6, "lag_effects": {"public_discontent": -8}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Use force to clear markets and impose rationing", "effects": {"public_approval": -8, "military_readiness": 2, "sectarian_stability": -6}, "budget_cost": 4, "lag_effects": {"religious_friction": 8}, "lag_delay": 1, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Negotiate with suppliers and hold a national price freeze", "effects": {"inflation": -8, "trade_balance": -5, "public_approval": 2}, "budget_cost": 5, "lag_effects": {"budget_balance": -4}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 1}},
        ],
    },
    {
        "id": "cyber_attack",
        "title": "Cyber Sovereignty Crisis",
        "condition": lambda state: state.kpis.get("digital_sovereignty", 50) < 55 or state.kpis.get("energy_security", 50) < 60,
        "description_templates": [
            "A coordinated cyber intrusion is disrupting civilian communications and energy grid telemetry.",
            "Foreign-linked ransomware operators are using open-source exploit chains to target strategic infrastructure.",
            "Critical systems are blinking off as the digital frontier becomes a battlefield.",
        ],
        "impact_preview": "System degradation, infrastructure vulnerability, and a cyber security mobilization push.",
        "options": [
            {"label": "Nationalize cybersecurity response and isolate strategic networks", "effects": {"digital_sovereignty": 10, "energy_security": 4, "public_approval": 2}, "budget_cost": 6, "lag_effects": {"crisis_resilience": 6}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Outsource technical remediation to commercial vendors", "effects": {"budget_balance": 2, "digital_sovereignty": -4}, "budget_cost": 3, "lag_effects": {"proxy_war_influence": 6}, "lag_delay": 1, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Launch a retaliatory cyber operation against suspected networks", "effects": {"military_readiness": 4, "international_law": -7, "proxy_war_influence": 8}, "budget_cost": 5, "lag_effects": {"international_law_violations": 9}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 2}},
        ],
    },
    {
        "id": "border_incident",
        "title": "Border Security Escalation",
        "condition": lambda state: state.kpis.get("military_readiness", 50) > 60 or state.kpis.get("eez_control", 50) < 65,
        "description_templates": [
            "A disputed maritime boundary is heating up as patrols and naval assets converge near strategic waters.",
            "Local militias and state-sponsored elements are provoking a fragile front line in a contested region.",
            "A routine exercise has triggered a broad escalation in military signaling across the border.",
        ],
        "impact_preview": "Risk of escalation, local mobilization, and wider military calculus.",
        "options": [
            {"label": "De-escalate through diplomatic backchannels and joint monitoring", "effects": {"international_law": 6, "public_approval": 3, "military_readiness": -2}, "budget_cost": 4, "lag_effects": {"trade_balance": 3}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Increase surveillance and preemptive military readiness", "effects": {"military_readiness": 8, "public_approval": 5, "international_law": -4}, "budget_cost": 7, "lag_effects": {"proxy_war_influence": 8}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Issue a sharp public ultimatum and mobilize reserve forces", "effects": {"military_readiness": 10, "public_approval": 4, "international_law": -9}, "budget_cost": 8, "lag_effects": {"religious_friction": 7, "proxy_war_influence": 10}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 2}},
        ],
    },
    {
        "id": "environmental_disaster",
        "title": "Climate and Water Shock",
        "condition": lambda state: state.kpis.get("environmental_health", 50) < 55 or state.kpis.get("food_security", 50) < 60,
        "description_templates": [
            "A prolonged drought and flood cycle is straining irrigation networks and threatening harvests.",
            "Crop losses, water contamination, and migration pressure are deepening the national resilience crisis.",
            "The climate front is no longer abstract; it is hitting rural communities and urban supply lines directly.",
        ],
        "impact_preview": "Agricultural losses, urban migration, and humanitarian capacity strain.",
        "options": [
            {"label": "Deploy emergency water infrastructure and urban support networks", "effects": {"food_security": 8, "public_approval": 5, "environmental_health": 6}, "budget_cost": 6, "lag_effects": {"budget_balance": -2}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Prioritize industrial water use and slash public subsidies", "effects": {"budget_balance": 4, "food_security": -7, "public_approval": -8}, "budget_cost": 4, "lag_effects": {"public_discontent": 8}, "lag_delay": 1, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Launch a national climate adaptation program", "effects": {"environmental_health": 12, "food_security": 5, "crisis_resilience": 7}, "budget_cost": 7, "lag_effects": {"budget_balance": -4}, "lag_delay": 3, "hidden_effects": {"implementation_lag_queue": 1}},
        ],
    },
    {
        "id": "diplomatic_isolation",
        "title": "Diplomatic Isolation Pressure",
        "condition": lambda state: state.hidden.get("international_law_violations", 0) > 50 or state.kpis.get("international_law", 50) < 45,
        "description_templates": [
            "International partners are withholding cooperation as legal and ethical breach concerns rise.",
            "Sanctions and diplomacy friction are accumulating as investors and allies reduce risk tolerance.",
            "The state’s position in global institutions is weakening under the weight of reputational damage.",
        ],
        "impact_preview": "Widening diplomatic isolation, sanctions risk, and governance costs.",
        "options": [
            {"label": "Pursue a reform push with independent investigations and transparency", "effects": {"international_law": 10, "public_approval": 4, "governance_quality": 6}, "budget_cost": 5, "lag_effects": {"budget_balance": -2}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Reject external oversight and double down on state control", "effects": {"international_law": -8, "public_approval": -4, "military_readiness": 3}, "budget_cost": 3, "lag_effects": {"proxy_war_influence": 8}, "lag_delay": 1, "hidden_effects": {"implementation_lag_queue": 1}},
            {"label": "Use economic diplomacy and targeted trade incentives to rebuild trust", "effects": {"trade_balance": 7, "international_law": 5, "budget_balance": -1}, "budget_cost": 4, "lag_effects": {"public_approval": 2}, "lag_delay": 2, "hidden_effects": {"implementation_lag_queue": 1}},
        ],
    },
]


def generate_scenario_cards(state: GameState) -> List[Dict]:
    eligible = []
    for event in EVENT_POOL:
        if event["condition"](state):
            eligible.append(event)

    randomizer = random.Random(state.random_seed + state.turn * 13)
    if len(eligible) < 3:
        for event in EVENT_POOL:
            if event not in eligible:
                eligible.append(event)
        eligible = eligible[:5]

    cards = []
    generated = randomizer.sample(eligible, k=min(len(eligible), randomizer.randint(3, 5)))
    for event in generated:
        description = randomizer.choice(event["description_templates"])
        options = []
        for option in event["options"]:
            options.append({
                "label": option["label"],
                "effects": option["effects"],
                "budget_cost": option["budget_cost"],
                "lag_delay": option["lag_delay"],
                "lag_effects": option.get("lag_effects", {}),
                "hidden_effects": option.get("hidden_effects", {}),
            })
        cards.append({
            "id": event["id"],
            "title": event["title"],
            "description": description,
            "impact_preview": event["impact_preview"],
            "options": options,
        })
    return cards


def apply_scenario_choice(state: GameState, card: Dict, option_index: int) -> None:
    option = card["options"][option_index]
    for key, delta in option["effects"].items():
        current = state.kpis.get(key, 50.0)
        state.kpis[key] = max(0.0, min(100.0, current + delta))

    for key, delta in option.get("hidden_effects", {}).items():
        state.hidden[key] = max(0.0, min(100.0, state.hidden.get(key, 50.0) + delta))

    if option.get("lag_delay", 0):
        state.lag_queue.append({
            "resolve_turn": state.turn + option["lag_delay"],
            "effects": option.get("lag_effects", {}),
            "description": f"Delayed consequence from {card['title']}: {option['label']}",
            "hidden_effects": option.get("hidden_effects", {}),
        })

    state.scenario_history.append(f"Resolved {card['title']} with: {option['label']}")
    state.event_log.append(f"Scenario choice recorded: {card['title']} -> {option['label']}")
    state.kpis["budget_balance"] = max(0.0, min(100.0, state.kpis.get("budget_balance", 60.0) - option.get("budget_cost", 0)))
