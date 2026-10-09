from __future__ import annotations

from models.state import GameState


def resolve_warfare(state: GameState, opponent_name: str = "Regional Block", conflict_type: str = "border_incident") -> dict:
    actor = state.ai_actors.get(opponent_name, state.ai_actors.get("Regional Block"))
    player_military = state.kpis.get("military_readiness", 50.0)
    player_logistics = state.kpis.get("logistics_capacity", 50.0)
    player_eez = state.kpis.get("eez_control", 50.0)
    player_public = state.kpis.get("public_approval", 50.0)
    player_law = state.kpis.get("international_law", 50.0)

    opponent_power = actor.military_strength + actor.aggression * 0.4 + actor.influence * 0.2
    tactical_score = player_military + player_logistics + player_eez + player_public * 0.2 + player_law * 0.2 - opponent_power

    if conflict_type == "invasion":
        tactical_score -= 10

    if tactical_score >= 12:
        result = "victory"
        summary = f"{state.country_name} secures a favorable outcome in the {conflict_type} against {opponent_name}."
        state.kpis["military_readiness"] = min(100.0, state.kpis.get("military_readiness", 50.0) + 6)
        state.kpis["public_approval"] = min(100.0, state.kpis.get("public_approval", 50.0) + 4)
        state.hidden["proxy_war_influence"] = max(0.0, state.hidden.get("proxy_war_influence", 0.0) - 8)
    elif tactical_score <= -12:
        result = "defeat"
        summary = f"{state.country_name} suffers a costly setback in the {conflict_type} under pressure from {opponent_name}."
        state.kpis["military_readiness"] = max(0.0, state.kpis.get("military_readiness", 50.0) - 11)
        state.kpis["public_approval"] = max(0.0, state.kpis.get("public_approval", 50.0) - 10)
        state.hidden["public_discontent"] = min(100.0, state.hidden.get("public_discontent", 0.0) + 8)
        state.hidden["proxy_war_influence"] = min(100.0, state.hidden.get("proxy_war_influence", 0.0) + 10)
    else:
        result = "standoff"
        summary = f"The {conflict_type} settles into a strategic standoff between {state.country_name} and {opponent_name}."
        state.kpis["military_readiness"] = max(0.0, min(100.0, state.kpis.get("military_readiness", 50.0) + 1))
        state.kpis["public_approval"] = max(0.0, min(100.0, state.kpis.get("public_approval", 50.0) - 1))

    state.event_log.append(summary)
    return {"result": result, "summary": summary}
