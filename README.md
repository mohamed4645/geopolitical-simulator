# Geopolitical Simulator

A turn-based geopolitical strategy game powered by Python and Streamlit.

## Features
- 10-sector strategic model across macroeconomics, security, diplomacy, science, health, agriculture, energy, governance, trade, and crisis management.
- Dynamic event generation with threshold-based triggers and delayed consequences.
- AI actors for the US, China, Russia, and regional neighbors.
- Budget allocation sliders and interactive scenario cards.
- Warfare, sanctions, and instability resolution logic.

## Local setup

1. Clone the repository.
2. Create a virtual environment:
   python -m venv .venv
   . .venv/bin/activate   # Windows: .venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Run the app:
   streamlit run app.py
5. Open the local URL shown by Streamlit.

## Game loop
- Each turn begins by applying delayed policies in the Implementation Lag Queue.
- AI rivals react to your posture and global developments.
- The dashboard updates with GDP, inflation, public approval, security readiness, debt, and law status.
- 3 to 5 procedural crisis cards appear for player choices.
- Budget and directives are resolved into trade-offs and long-term strategic effects.

## Default objective
Build national strength through balanced statecraft while avoiding economic collapse, military defeat, coups, revolution, or ecological disaster.
