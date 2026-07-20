"""
Smart Energy Analytics
------------------------
Estimates a household's monthly electricity bill using real appliance
power consumption (with duty-cycle correction) and official city-wise
electricity tariff rates. No ML — this is a pure calculator.
"""

import pandas as pd
import streamlit as st

from core_logic import (
    APPLIANCE_WATTAGE,
    DUTY_CYCLE,
    APPLIANCE_DISPLAY_NAMES,
    APPLIANCE_CATEGORIES,
    CATEGORY_HELPER_TEXT,
    DEFAULT_HOURS,
    TARIFF_SLABS,
    calculate_units_consumed,
    calculate_slab_bill,
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Smart Energy Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# GLOBAL THEME (electric / energy look)
# ============================================================
st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at 50% 0%, #1a2540 0%, #0e1117 55%);
        }
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(120, 170, 255, 0.25);
            border-radius: 12px;
            padding: 14px 16px;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.08);
        }
        [data-testid="stMetricLabel"] { font-weight: 600; }
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            border: none;
            color: white;
        }
        div.stButton > button:hover { filter: brightness(1.1); }
        .app-title {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: -6px;
        }
        .app-subtitle { color: #9aa4b2; font-size: 1rem; margin-top: 4px; margin-bottom: 6px; }
        div[data-testid="stTextInput"] input {
            border: 1px solid rgba(120, 170, 255, 0.35) !important;
            background: rgba(255, 255, 255, 0.03) !important;
        }
        .login-wrapper { display: flex; justify-content: center; margin-top: 10vh; }
        .login-card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(120, 170, 255, 0.25);
            border-radius: 20px;
            padding: 48px 40px;
            width: 100%;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 0 40px rgba(59, 130, 246, 0.15);
        }
        .login-icon {
            font-size: 52px;
            margin-bottom: 8px;
            filter: drop-shadow(0 0 12px rgba(96, 165, 250, 0.8));
            animation: pulse 2.4s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); filter: drop-shadow(0 0 8px rgba(96, 165, 250, 0.6)); }
            50% { transform: scale(1.08); filter: drop-shadow(0 0 20px rgba(96, 165, 250, 1)); }
        }
        .login-title {
            font-size: 1.6rem;
            font-weight: 800;
            margin-bottom: 6px;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .login-subtitle { color: #9aa4b2; font-size: 0.92rem; margin-bottom: 28px; }
        .category-helper { color: #8b9bb4; font-size: 0.85rem; margin-bottom: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOGIN GATE
# ============================================================
def check_password():
    """Returns True if the user entered the correct password."""

    def password_entered():
        if st.session_state["password"] == st.secrets["app_password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.markdown(
        """
        <div class="login-wrapper">
            <div class="login-card">
                <div class="login-icon">⚡</div>
                <div class="login-title">Smart Energy Analytics</div>
                <div class="login-subtitle">Know your real electricity bill before it arrives.</div>
        """,
        unsafe_allow_html=True,
    )

    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.text_input(
            "Access code",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="Enter access code",
            label_visibility="collapsed",
        )
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("That code didn't work. Try again.")

    st.markdown("</div></div>", unsafe_allow_html=True)
    return False


if not check_password():
    st.stop()
# ============================================================
# CONSTANTS
# ============================================================
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

CITIES = list(TARIFF_SLABS.keys())


# ============================================================
# HELPERS
# ============================================================
def format_currency(value: float) -> str:
    return f"₹ {value:,.2f}"


def set_default_hours(appliance_key: str):
    """Callback for the 'Not sure?' button — fills in the typical hours value."""
    st.session_state[f"hours_{appliance_key}"] = DEFAULT_HOURS.get(appliance_key, 1.0)


# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="app-title">⚡ Smart Energy Analytics</div>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Know your real electricity bill before it arrives.</p>', unsafe_allow_html=True)
st.divider()

# ============================================================
# SIDEBAR — CATEGORIZED APPLIANCE INPUTS
# ============================================================
with st.sidebar:
    st.header("Your Household")

    for category_name, appliance_keys in APPLIANCE_CATEGORIES.items():
        with st.expander(category_name, expanded=False):
            helper_text = CATEGORY_HELPER_TEXT.get(category_name, "")
            if helper_text:
                st.markdown(f'<div class="category-helper">{helper_text}</div>', unsafe_allow_html=True)

            for appliance_key in appliance_keys:
                display_name = APPLIANCE_DISPLAY_NAMES.get(appliance_key, appliance_key)
                count_key = f"count_{appliance_key}"
                hours_key = f"hours_{appliance_key}"

                st.markdown(f"**{display_name}**")
                row1, row2, row3 = st.columns([2, 3, 2])

                with row1:
                    st.number_input(
                        "Count", min_value=0, max_value=50, value=0,
                        key=count_key, label_visibility="collapsed",
                    )
                with row2:
                    if hours_key not in st.session_state:
                        st.session_state[hours_key] = 0.0
                    st.slider(
                        "Hours/day", min_value=0.0, max_value=24.0, step=0.5,
                        key=hours_key, label_visibility="collapsed",
                    )
                with row3:
                    st.button(
                        "Not sure?",
                        key=f"notsure_{appliance_key}",
                        on_click=set_default_hours,
                        args=(appliance_key,),
                        use_container_width=True,
                    )
                st.divider()

    st.subheader("Location & Month")
    city = st.selectbox("City", CITIES)
    month_name = st.selectbox("Month", MONTH_NAMES, index=0)
    month = MONTH_NAMES.index(month_name) + 1

    submitted = st.button("Calculate My Bill", use_container_width=True)
# ============================================================
# RESULTS
# ============================================================
if submitted:
    # --- Build the appliance_inputs dict from session state ---
    appliance_inputs = {}
    for category_name, appliance_keys in APPLIANCE_CATEGORIES.items():
        for appliance_key in appliance_keys:
            count = st.session_state.get(f"count_{appliance_key}", 0)
            hours = st.session_state.get(f"hours_{appliance_key}", 0.0)
            if count > 0 and hours > 0:
                appliance_inputs[appliance_key] = {"count": count, "hours": hours}

    if not appliance_inputs:
        st.warning("Enter at least one appliance with its count and daily hours before calculating.")
        st.stop()

    units_consumed = calculate_units_consumed(appliance_inputs)
    real_bill = calculate_slab_bill(units_consumed, city)

    # --- Hero result ---
    st.subheader("Your Estimated Bill")
    m1, m2 = st.columns(2)
    m1.metric("Units Consumed", f"{units_consumed} kWh")
    m2.metric("Estimated Bill", format_currency(real_bill))
    st.caption(f"{city} · {month_name}")

    st.divider()

    # --- Slab-wise breakdown ---
    with st.expander("See how this bill was calculated", expanded=True):
        slabs = TARIFF_SLABS[city]
        remaining = units_consumed
        previous_limit = 0
        breakdown_rows = []
        for units_upto, rate in slabs:
            units_in_slab = remaining if units_upto is None else min(remaining, units_upto - previous_limit)
            if units_in_slab <= 0:
                continue
            breakdown_rows.append({
                "Units": f"{previous_limit}-{units_upto if units_upto else '+'}",
                "Rate per unit": f"₹{rate}",
                "Units billed": round(units_in_slab, 2),
                "Amount": round(units_in_slab * rate, 2),
            })
            remaining -= units_in_slab
            if units_upto is not None:
                previous_limit = units_upto
        st.dataframe(pd.DataFrame(breakdown_rows), hide_index=True, use_container_width=True)
        st.metric("Total", format_currency(real_bill))

    st.divider()

    # --- What's driving your bill (grouped by category) ---
    with st.expander("What's driving your bill", expanded=True):
        category_contribution = {}
        for category_name, appliance_keys in APPLIANCE_CATEGORIES.items():
            total_wh = 0
            for appliance_key in appliance_keys:
                if appliance_key in appliance_inputs:
                    count = appliance_inputs[appliance_key]["count"]
                    hours = appliance_inputs[appliance_key]["hours"]
                    wattage = APPLIANCE_WATTAGE.get(appliance_key, 0)
                    duty = DUTY_CYCLE.get(appliance_key, 1.0)
                    total_wh += count * wattage * duty * hours
            if total_wh > 0:
                category_contribution[category_name] = total_wh

        total_wh_all = sum(category_contribution.values())
        sorted_categories = sorted(category_contribution.items(), key=lambda x: x[1], reverse=True)

        top_category = sorted_categories[0][0]
        st.write(f"**{top_category}** has the biggest effect on your bill.")
        st.write("")

        for category_name, wh in sorted_categories:
            share = wh / total_wh_all
            if share >= 0.30:
                tag = "High impact"
            elif share >= 0.10:
                tag = "Medium impact"
            else:
                tag = "Low impact"

            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.progress(share, text=category_name)
            with col_b:
                st.caption(tag)

        st.caption("See where your electricity is really going.")

    # --- Input summary ---
    with st.expander("Your inputs"):
        summary_rows = [
            {
                "Appliance": APPLIANCE_DISPLAY_NAMES.get(k, k),
                "Count": v["count"],
                "Hours/day": v["hours"],
            }
            for k, v in appliance_inputs.items()
        ]
        st.dataframe(pd.DataFrame(summary_rows), hide_index=True, use_container_width=True)

else:
    st.info("Fill in your appliances in the sidebar and select **Calculate My Bill** to get started.")