"""
Smart Energy Analytics
------------------------
Estimates a household's monthly electricity bill using real appliance
power consumption and official city-wise tariff rates.
"""

import altair as alt
import joblib
import pandas as pd
import streamlit as st

from core_logic import (
    APPLIANCE_WATTAGE,
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
# GLOBAL THEME (electric / energy look, used on every page)
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
        div.stButton > button, div.stFormSubmitButton > button {
            border-radius: 8px;
            font-weight: 600;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            border: none;
            color: white;
        }
        div.stButton > button:hover, div.stFormSubmitButton > button:hover {
            filter: brightness(1.1);
        }
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
MODEL_PATH = "models/electricity_bill_model_v2.pkl"
CITY_ENCODER_PATH = "models/city_encoder_v2.pkl"

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

CITIES = list(TARIFF_SLABS.keys())


# ============================================================
# CACHED LOADERS
# ============================================================
@st.cache_resource(show_spinner="Loading...")
def load_model_artifacts():
    model = joblib.load(MODEL_PATH)
    city_encoder = joblib.load(CITY_ENCODER_PATH)
    return model, city_encoder


model, city_encoder = load_model_artifacts()


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def format_currency(value: float) -> str:
    return f"₹ {value:,.2f}"


def generate_energy_tips(ac, ac_hours, units_consumed):
    tips = []
    if ac >= 2 and ac_hours >= 6:
        tips.append(("warning", "Your air conditioners run for long hours daily. Switching to Eco mode can lower your bill."))
    if units_consumed > 400:
        tips.append(("info", "Your usage is high enough to fall into a costlier tariff slab. Reducing usage even slightly can help."))
    return tips


# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="app-title">⚡ Smart Energy Analytics</div>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Know your real electricity bill before it arrives.</p>', unsafe_allow_html=True)
st.divider()

# ============================================================
# SIDEBAR — INPUT FORM
# ============================================================
with st.sidebar:
    st.header("Your Household")

    with st.form("prediction_form"):
        st.subheader("Appliances")

        col1, col2 = st.columns(2)
        with col1:
            fan = st.number_input("Fans", min_value=0, max_value=40, value=2)
            refrigerator = st.number_input("Refrigerators", min_value=0, max_value=10, value=1)
            ac = st.number_input("Air Conditioners", min_value=0, max_value=10, value=1)
        with col2:
            tv = st.number_input("Televisions", min_value=0, max_value=30, value=1)
            monitor = st.number_input("Monitors", min_value=0, max_value=20, value=1)
            motor = st.number_input("Motor Pumps", min_value=0, max_value=10, value=0)

        st.subheader("Daily Usage (hours)")

        col3, col4 = st.columns(2)
        with col3:
            fan_hours = st.slider("Fans", 0, 24, 8, key="fan_hours")
            refrigerator_hours = st.slider("Refrigerator", 0, 24, 24, key="fridge_hours")
            ac_hours = st.slider("AC", 0, 24, 6, key="ac_hours")
        with col4:
            tv_hours = st.slider("Television", 0, 24, 4, key="tv_hours")
            monitor_hours = st.slider("Monitor", 0, 24, 3, key="monitor_hours")
            motor_hours = st.slider("Motor Pump", 0, 24, 0, key="motor_hours")

        st.subheader("Location & Month")
        city = st.selectbox("City", CITIES)
        month_name = st.selectbox("Month", MONTH_NAMES, index=0)
        month = MONTH_NAMES.index(month_name) + 1

        submitted = st.form_submit_button("Calculate My Bill", use_container_width=True)

# ============================================================
# RESULTS
# ============================================================
if submitted:
    units_consumed = calculate_units_consumed(
        fan, fan_hours,
        refrigerator, refrigerator_hours,
        ac, ac_hours,
        tv, tv_hours,
        monitor, monitor_hours,
        motor, motor_hours,
    )
    real_bill = calculate_slab_bill(units_consumed, city)

    city_encoded = city_encoder.transform([city])[0]
    input_data = [[
        fan, fan_hours,
        refrigerator, refrigerator_hours,
        ac, ac_hours,
        tv, tv_hours,
        monitor, monitor_hours,
        motor, motor_hours,
        month, city_encoded,
    ]]
    ml_prediction = float(model.predict(input_data)[0])

    st.subheader("Your Estimated Bill")
    m1, m2, m3 = st.columns(3)
    m1.metric("Units Consumed", f"{units_consumed} kWh")
    m2.metric("Estimated Bill", format_currency(real_bill))
    m3.metric("Quick Estimate (AI)", format_currency(ml_prediction))
    st.caption("The Estimated Bill is your accurate figure, calculated from your city's actual tariff. The AI estimate is shown alongside for comparison.")

    st.divider()

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

    st.subheader("Ways to Save")
    tips = generate_energy_tips(ac, ac_hours, units_consumed)
    if tips:
        for tip_type, message in tips:
            getattr(st, tip_type)(message)
    else:
        st.success("Your usage looks efficient. No changes needed right now.")

    st.divider()

    with st.expander("What's driving your bill"):
        appliance_inputs = {
            "Air Conditioners": (ac, ac_hours, APPLIANCE_WATTAGE["AirConditioner"]),
            "Refrigerator": (refrigerator, refrigerator_hours, APPLIANCE_WATTAGE["Refrigerator"]),
            "Fans": (fan, fan_hours, APPLIANCE_WATTAGE["Fan"]),
            "Motor Pump": (motor, motor_hours, APPLIANCE_WATTAGE["MotorPump"]),
            "Television": (tv, tv_hours, APPLIANCE_WATTAGE["Television"]),
            "Monitor": (monitor, monitor_hours, APPLIANCE_WATTAGE["Monitor"]),
        }

        contributions = {
            name: count * hours * watt
            for name, (count, hours, watt) in appliance_inputs.items()
        }
        total = sum(contributions.values())

        if total == 0:
            st.info("Add some appliances to see what's driving your bill.")
        else:
            sorted_items = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
            top_name = sorted_items[0][0]
            st.write(f"**{top_name}** has the biggest effect on your bill.")
            st.write("")

            for name, value in sorted_items:
                share = value / total
                if share >= 0.30:
                    tag = "High impact"
                elif share >= 0.10:
                    tag = "Medium impact"
                elif share > 0:
                    tag = "Low impact"
                else:
                    tag = "Not in use"

                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.progress(share, text=name)
                with col_b:
                    st.caption(tag)

        st.caption("See where your electricity is really going.")

    with st.expander("Your inputs"):
        summary_df = pd.DataFrame({
            "Appliance": ["Fans", "Refrigerators", "Air Conditioners", "Televisions", "Monitors", "Motor Pumps"],
            "Count": [fan, refrigerator, ac, tv, monitor, motor],
            "Hours/day": [fan_hours, refrigerator_hours, ac_hours, tv_hours, monitor_hours, motor_hours],
        })
        st.dataframe(summary_df, hide_index=True, use_container_width=True)
        st.caption(f"{city} · {month_name}")

else:
    st.info("Fill in your household details and select **Calculate My Bill** to get started.")