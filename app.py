import streamlit as st

st.set_page_config(
    page_title="Wire Run Calculator",
    page_icon="🧵",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(160deg, #061426 0%, #0b2340 55%, #071426 100%);
        color: #f4f8ff;
    }
    .block-container {
        max-width: 760px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .hero {
        padding: 1.3rem 1.2rem;
        border: 1px solid #1d5b91;
        border-radius: 20px;
        background: linear-gradient(120deg, #0d3158, #08203a);
        margin-bottom: 1.2rem;
    }
    .hero h1 { margin: 0; font-size: 1.9rem; color: #ffffff; }
    .hero p { margin: .5rem 0 0; color: #8bd5ff; }
    .result {
        padding: 1rem;
        border: 1px solid #23496d;
        border-radius: 16px;
        background: rgba(14, 42, 70, .9);
        margin-bottom: .7rem;
    }
    .result-label {
        font-size: .82rem;
        color: #a8c3e2;
        font-weight: 700;
        letter-spacing: .06em;
    }
    .result-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: .2rem;
    }
    .note {
        padding: .9rem 1rem;
        border-radius: 12px;
        background: #0a2a4a;
        border: 1px solid #1266a7;
        color: #c2def6;
        font-size: .9rem;
    }
    div.stButton > button {
        width: 100%;
        min-height: 3.2rem;
        border-radius: 12px;
        border: 0;
        background: linear-gradient(90deg, #168bff, #0759e8);
        color: white;
        font-weight: 800;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "previous_finish" not in st.session_state:
    st.session_state.previous_finish = 1500
if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.markdown(
    """
    <div class="hero">
      <h1>🧵 Wire Run Calculator</h1>
      <p>Fast • Clear • Production-ready</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Input Values")

reuse = st.checkbox(
    "Use Previous Finish Length",
    value=False,
    help="Use the Finish Length from your last calculation in this open session.",
)

hub = st.number_input(
    "Hub Number (Start Number)", min_value=0, step=1, value=19978
)

default_finish = (
    int(st.session_state.previous_finish)
    if st.session_state.previous_finish
    else 1500
)
finish = st.number_input(
    "Finish Length",
    min_value=1,
    step=1,
    value=default_finish,
    disabled=reuse,
)

if reuse:
    finish = int(st.session_state.previous_finish)

payoff = st.number_input("Payoff Reel Number", min_value=0, step=1, value=2000)

st.markdown(
    """
    <div class="note">
    <b>Calculation rules</b><br>
    FL = Payoff Reel ÷ Finish Length (decimal ignored)<br>
    Total Wire Run = Finish Length × FL + FL × 3 + 6<br>
    If Total Wire Run is odd, add 1 to make it even.<br>
    Top = Hub Number + adjusted Total Wire Run<br>
    Weld Number = Top − 1700
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("CALCULATE"):
    fl = int(payoff) // int(finish)
    total_wire_run = int(finish) * fl + fl * 3 + 6

    if total_wire_run % 2 != 0:
        total_wire_run += 1

    top = int(hub) + total_wire_run
    weld = top - 1700

    st.session_state.previous_finish = int(finish)
    st.session_state.last_result = {
        "FL": fl,
        "Total Wire Run": total_wire_run,
        "Top": top,
        "Weld Number": weld,
    }

if st.session_state.last_result:
    st.subheader("Calculation Results")
    result = st.session_state.last_result
    colors = {
        "FL": "#10c997",
        "Total Wire Run": "#21c8f5",
        "Top": "#b58aff",
        "Weld Number": "#ffad55",
    }
    for name in ["FL", "Total Wire Run", "Top", "Weld Number"]:
        st.markdown(
            f"""
            <div class="result">
              <div class="result-label" style="color:{colors[name]}">{name.upper()}</div>
              <div class="result-value">{result[name]:,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.success(
        "Calculation complete • Finish Length saved for this session: "
        f"{int(st.session_state.previous_finish):,}"
    )

    top = result["Top"]
    if top >= 1_000_000:
        st.error(
            "🚨 PRINTER RESET REQUIRED NOW — Top has reached or exceeded 1,000,000. "
            "Follow your workplace reset procedure."
        )
    elif top > 990_000:
        remaining = 1_000_000 - top
        st.warning(
            "⚠️ PRINTER RESET SOON — Top is above 990,000. "
            f"Only {remaining:,} numbers remain before 1,000,000."
        )

st.caption("Tip: Deploy this app online, then use Safari → Share → Add to Home Screen.")
