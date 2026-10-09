from __future__ import annotations

import streamlit as st

from models.state import build_country_baseline
from engine.evaluator import evaluate_turn, advance_game_turn
from engine.scenario_generator import generate_scenario_cards, apply_scenario_choice
from ui.dashboard import render_dashboard


st.set_page_config(layout="wide", page_title="Geopolitical Simulator")


def get_or_create_state(country: str):
    if "game_state" not in st.session_state:
        st.session_state.game_state = build_country_baseline(country)
    if st.session_state.game_state.country_name != country:
        st.session_state.game_state = build_country_baseline(country)
    return st.session_state.game_state


def main():
    st.title("Geopolitical Strategic Command")
    st.caption("Adaptive, turn-based geopolitical simulation based on a 10-sector state engine.")

    with st.sidebar:
        st.header("Campaign Setup")
        countries = [
            "United States",
            "China",
            "Russia",
            "India",
            "Brazil",
            "Turkey",
            "Indonesia",
            "Germany",
            "South Africa",
            "France",
        ]
        selected_country = st.selectbox("Choose a nation", countries, index=0)
        reset_button = st.button("Reset campaign")
        if reset_button:
            st.session_state.pop("game_state", None)
            st.session_state.pop("budget_allocations", None)
            st.rerun()

        st.markdown("---")
        st.subheader("Strategic directives")
        directive = st.text_area(
            "Custom national directive",
            value="Maintain strategic autonomy, reinforce public legitimacy, and avoid escalation into open war.",
            height=110,
        )
        if st.button("Issue directive"):
            state = get_or_create_state(selected_country)
            state.policy_directives.append(directive)
            state.event_log.append(f"Directive issued: {directive}")

    state = get_or_create_state(selected_country)

    if not hasattr(state, "scenarios") or not state.scenarios:
        state.scenarios = generate_scenario_cards(state)

    render_dashboard(state)

    st.subheader("Turn execution")
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Advance turn", use_container_width=True):
            state = st.session_state.game_state
            budgets = st.session_state.get("budget_allocations", {
                "macro": 20,
                "security": 20,
                "diplomacy": 15,
                "technology": 12,
                "society": 9,
                "food": 7,
                "energy": 8,
                "governance": 5,
                "trade": 3,
                "crisis": 1,
            })
            evaluate_turn(state, budgets)
            advance_game_turn(state)
            state.scenarios = generate_scenario_cards(state)
            st.session_state.game_state = state
            st.rerun()

    with col2:
        if st.button("Generate new scenarios", use_container_width=True):
            state.scenarios = generate_scenario_cards(state)
            st.session_state.game_state = state
            st.rerun()

    st.markdown("---")
    st.subheader("Crisis cards")

    if state.scenarios:
        for idx, card in enumerate(state.scenarios):
            with st.container(border=True):
                st.markdown(f"### {card['title']}")
                st.write(card["description"])
                options = card["options"]
                option_labels = [option["label"] for option in options]
                choice = st.radio(
                    "Choose a response:",
                    option_labels,
                    key=f"scenario_{idx}",
                    horizontal=False,
                )
                if st.button(f"Resolve scenario {idx + 1}", key=f"resolve_{idx}"):
                    option_index = option_labels.index(choice)
                    apply_scenario_choice(state, card, option_index)
                    state.scenarios = [
                        scenario for scenario in state.scenarios if scenario["id"] != card["id"]
                    ]
                    st.session_state.game_state = state
                    st.rerun()
                st.caption(f"Impact preview: {card.get('impact_preview', 'Strategic tradeoff risk level moderate.')}")
    else:
        st.info("No active crisis cards. Advance the turn to generate a new set of scenarios.")


if __name__ == "__main__":
    main()
