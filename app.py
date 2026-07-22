"""
Smart Energy Analytics
------------------------
3-page app: Login -> Input (drill-down) -> Results & Recommendations.
No ML — the slab-based calculation is the real bill.
"""

import pandas as pd
import streamlit as st

from core_logic import (
    APPLIANCE_WATTAGE,
    DUTY_CYCLE,
    APPLIANCE_DISPLAY_NAMES,
    NAV_TREE,
    CATEGORY_CAPTIONS,
    SUBTYPE_CAPTIONS,
    DEFAULT_HOURS,
    TARIFF_SLABS,
    calculate_units_consumed,
    calculate_slab_bill,
)

st.set_page_config(
    page_title="Smart Energy Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# GLOBAL THEME
# ============================================================
st.markdown(
    """
    <style>
        .stApp { background: radial-gradient(circle at 50% 0%, #1a2540 0%, #0e1117 55%); }
        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.04); border: 1px solid rgba(120,170,255,0.25);
            border-radius: 12px; padding: 14px 16px; box-shadow: 0 0 20px rgba(59,130,246,0.08);
        }
        [data-testid="stMetricLabel"] { font-weight: 600; }
        div.stButton > button {
            border-radius: 8px; font-weight: 600;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6); border: none; color: white;
            transition: filter 0.15s ease;
        }
        div.stButton > button:hover { filter: brightness(1.15); }
        .app-title {
            font-size: 2rem; font-weight: 800;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: -6px;
        }
        .app-subtitle { color: #9aa4b2; font-size: 1rem; margin-top: 4px; margin-bottom: 6px; }

        /* ---------- LOGIN PAGE ---------- */
        .login-wrapper { display: flex; justify-content: center; margin-top: 7vh; }
        .login-card {
            position: relative; overflow: hidden;
            background: rgba(255,255,255,0.04); border: 1px solid rgba(120,170,255,0.25);
            border-radius: 20px; padding: 48px 40px; width: 100%; max-width: 430px;
            text-align: center; box-shadow: 0 0 40px rgba(59,130,246,0.15);
        }
        /* Faint animated circuit-style backdrop lines */
        .login-card::before {
            content: ""; position: absolute; inset: -50%;
            background: repeating-linear-gradient(
                115deg, rgba(96,165,250,0.05) 0px, rgba(96,165,250,0.05) 2px,
                transparent 2px, transparent 40px
            );
            animation: drift 14s linear infinite;
            pointer-events: none;
        }
        @keyframes drift {
            0% { transform: translate(0,0); }
            100% { transform: translate(40px, 40px); }
        }
        .login-icon-wrap { position: relative; z-index: 1; margin-bottom: 4px; }
        .login-icon {
            font-size: 52px;
            filter: drop-shadow(0 0 12px rgba(96,165,250,0.8));
            animation: pulse 2.4s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); filter: drop-shadow(0 0 8px rgba(96,165,250,0.6)); }
            50% { transform: scale(1.08); filter: drop-shadow(0 0 20px rgba(96,165,250,1)); }
        }
        .login-title {
            position: relative; z-index: 1;
            font-size: 1.6rem; font-weight: 800; margin-bottom: 6px;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        /* Rotating tagline — 3 lines cross-fading, pure CSS, no JS needed */
        .rotator { position: relative; z-index: 1; height: 22px; margin-bottom: 22px; }
        .rotator span {
            position: absolute; left: 0; right: 0;
            color: #c7d2fe; font-size: 0.92rem; font-style: italic;
            opacity: 0; animation: rotate-fade 9s infinite;
        }
        .rotator span:nth-child(1) { animation-delay: 0s; }
        .rotator span:nth-child(2) { animation-delay: 3s; }
        .rotator span:nth-child(3) { animation-delay: 6s; }
        @keyframes rotate-fade {
            0% { opacity: 0; }
            5% { opacity: 1; }
            28% { opacity: 1; }
            33% { opacity: 0; }
            100% { opacity: 0; }
        }
        .login-trust-strip {
            position: relative; z-index: 1;
            margin-top: 24px; padding-top: 16px; border-top: 1px solid rgba(120,170,255,0.15);
            color: #6b7688; font-size: 0.78rem; letter-spacing: 0.3px;
        }
        div[data-testid="stTextInput"] input {
            border: 1px solid rgba(120,170,255,0.35) !important; background: rgba(255,255,255,0.03) !important;
            transition: box-shadow 0.2s ease, border-color 0.2s ease;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: rgba(96,165,250,0.9) !important;
            box-shadow: 0 0 14px rgba(96,165,250,0.45) !important;
        }
        .shake-error {
            animation: shake 0.4s ease; color: #f87171; font-size: 0.85rem; margin-top: 6px;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20% { transform: translateX(-6px); }
            40% { transform: translateX(6px); }
            60% { transform: translateX(-4px); }
            80% { transform: translateX(4px); }
        }

        /* ---------- CATEGORY PILL NAV (center panel, replaces sidebar categories) ---------- */
        .pill-caption { color: #7dd3fc; font-size: 0.85rem; margin: 4px 0 10px 0; }
        .breadcrumb { font-size: 0.95rem; color: #9aa4b2; margin-bottom: 4px; }
        .breadcrumb b { color: #a78bfa; }
        .not-sure-caption { color: #7dd3fc; font-size: 0.78rem; margin-top: -6px; }
        .field-label { font-weight: 600; margin-top: 8px; margin-bottom: -4px; }
        .added-chip {
            display: inline-block; background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.35);
            border-radius: 20px; padding: 4px 12px; margin: 3px; font-size: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOGIN GATE
# ============================================================
def check_password():
    def password_entered():
        correct_password = st.secrets.get("app_password", None)
        if correct_password is None:
            st.session_state["password_correct"] = False
            st.session_state["config_error"] = True
            return
        if st.session_state["password"] == correct_password:
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
                <div class="login-icon-wrap"><div class="login-icon">⚡</div></div>
                <div class="login-title">Smart Energy Analytics</div>
                <div class="rotator">
                    <span>Know your real electricity bill before it arrives.</span>
                    <span>Real DISCOM tariffs. No ML guesswork.</span>
                    <span>40+ appliances. One honest number.</span>
                </div>
        """,
        unsafe_allow_html=True,
    )

    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.text_input(
            "Access code", type="password", on_change=password_entered,
            key="password", placeholder="Enter access code", label_visibility="collapsed",
        )
        if st.session_state.get("config_error", False):
            st.error("App isn't configured correctly (missing password setting). Contact the app owner.")
        elif "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.markdown('<div class="shake-error">Incorrect password. Please try again.</div>', unsafe_allow_html=True)

    st.markdown(
        """
                <div class="login-trust-strip">Powered by real DISCOM tariff data · 15 cities supported · No ML guesswork</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
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


def format_currency(value: float) -> str:
    return f"₹ {value:,.2f}"


# ============================================================
# SESSION STATE INIT
# ============================================================
defaults = {
    "stage": "input",
    "nav_category": None,
    "nav_subtype": None,
    "nav_leaf": None,
    "nav_variant_group": None,
    "nav_leaf_options": None,
    "added_appliances": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def go_category(cat):
    st.session_state.nav_category = cat
    st.session_state.nav_subtype = None
    st.session_state.nav_leaf = None
    st.session_state.nav_variant_group = None
    st.session_state.nav_leaf_options = None


def go_subtype(subtype):
    st.session_state.nav_subtype = subtype
    st.session_state.nav_leaf = None
    st.session_state.nav_variant_group = None
    st.session_state.nav_leaf_options = None


def go_leaf(leaf):
    st.session_state.nav_leaf = leaf


def reset_to_category_subtypes():
    """Goes back to the subtype-icon screen for the CURRENT category.
    Used after adding an appliance — never re-triggers the single-leaf
    auto-skip because subtype is cleared too (this was the loop bug)."""
    st.session_state.nav_subtype = None
    st.session_state.nav_leaf = None
    st.session_state.nav_variant_group = None
    st.session_state.nav_leaf_options = None


def back_to_subtype_list():
    st.session_state.nav_subtype = None
    st.session_state.nav_leaf = None
    st.session_state.nav_variant_group = None
    st.session_state.nav_leaf_options = None


def back_to_variant_list():
    st.session_state.nav_leaf = None


def apply_default_hours(appliance_key):
    st.session_state[f"hours_{appliance_key}"] = DEFAULT_HOURS.get(appliance_key, 1.0)
    st.session_state[f"hours_num_{appliance_key}"] = DEFAULT_HOURS.get(appliance_key, 1.0)
    st.session_state[f"used_default_{appliance_key}"] = True


def sync_hours_from_number(appliance_key):
    st.session_state[f"hours_{appliance_key}"] = st.session_state[f"hours_num_{appliance_key}"]


def sync_hours_from_slider(appliance_key):
    st.session_state[f"hours_num_{appliance_key}"] = st.session_state[f"hours_{appliance_key}"]


# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="app-title">⚡ Smart Energy Analytics</div>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Know your real electricity bill before it arrives.</p>', unsafe_allow_html=True)
st.divider()

# ============================================================
# SIDEBAR — city/month + added-appliance summary + pinned Calculate
# (Category navigation intentionally lives in the CENTER panel now,
#  not the sidebar — this avoids the sidebar staying open/stuck on
#  mobile after every tap, which was a real bug in the old design.)
# ============================================================
with st.sidebar:
    st.header("Your Household")

    if st.session_state.added_appliances:
        st.caption(f"✓ {len(st.session_state.added_appliances)} appliance(s) added")
        chips_html = "".join(
            f'<span class="added-chip">{APPLIANCE_DISPLAY_NAMES.get(k, k)}</span>'
            for k in st.session_state.added_appliances
        )
        st.markdown(chips_html, unsafe_allow_html=True)
        st.write("")
    else:
        st.caption("No appliances added yet. Use the category tabs to start.")

    st.subheader("Location & Month")
    city = st.selectbox("City", CITIES, key="city_select")
    month_name = st.selectbox("Month", MONTH_NAMES, index=0, key="month_select")

    st.write("")
    calculate_clicked = st.button("⚡ Calculate My Bill", use_container_width=True)
    if calculate_clicked:
        if not st.session_state.added_appliances:
            st.warning("Add at least one appliance first.")
        else:
            st.session_state.stage = "results"

# ============================================================
# MAIN AREA — wrapped in try/except so a stray widget-key clash
# from rapid clicking shows an error message instead of crashing
# the script and wiping session_state (which was kicking users
# back to the login screen).
# ============================================================
try:
    if st.session_state.stage == "input":

        # ---------------- Category pill row (center panel) ----------------
        st.subheader("Add Your Appliances")
        cat_names = list(NAV_TREE.keys())
        row1, row2 = cat_names[:4], cat_names[4:]
        cols1 = st.columns(len(row1))
        for i, cname in enumerate(row1):
            with cols1[i]:
                if st.button(cname, key=f"catpill_{cname}", use_container_width=True):
                    go_category(cname)
        if row2:
            cols2 = st.columns(len(row2))
            for i, cname in enumerate(row2):
                with cols2[i]:
                    if st.button(cname, key=f"catpill_{cname}", use_container_width=True):
                        go_category(cname)

        st.divider()

        if st.session_state.nav_category is None:
            st.info("👆 Pick a category above to start adding your appliances.")
        else:
            cat = st.session_state.nav_category
            subtype = st.session_state.nav_subtype
            leaf = st.session_state.nav_leaf

            # --- Breadcrumb ---
            crumb_parts = [f'<b>{cat}</b>']
            if subtype:
                crumb_parts.append(subtype)
            if leaf:
                crumb_parts.append(APPLIANCE_DISPLAY_NAMES.get(leaf, leaf))
            st.markdown(f'<div class="breadcrumb">{" &nbsp;›&nbsp; ".join(crumb_parts)}</div>', unsafe_allow_html=True)

            if leaf:
                st.button("← Back", key="back_lvl3", on_click=back_to_variant_list)
            elif subtype:
                st.button("← Back", key="back_lvl2", on_click=back_to_subtype_list)

            st.write("")

            def render_appliance_input(leaf_key, category_name):
                """Shared final-input renderer — used for both single-leaf
                auto-resolved appliances AND multi-variant picked leaves.
                No st.rerun() calls here, so no rerun-loop is possible."""
                display_name = APPLIANCE_DISPLAY_NAMES.get(leaf_key, leaf_key)
                st.subheader(display_name)

                st.markdown('<p class="field-label">No. of Units</p>', unsafe_allow_html=True)
                st.caption("How many of this exact appliance do you have?")
                st.number_input(
                    "Count", min_value=0, max_value=20, value=1,
                    key=f"count_{leaf_key}", label_visibility="collapsed",
                )

                st.markdown('<p class="field-label">Daily Usage Hours</p>', unsafe_allow_html=True)
                st.caption("How many hours per day does it run, on average?")

                if f"hours_{leaf_key}" not in st.session_state:
                    st.session_state[f"hours_{leaf_key}"] = 0.0
                if f"hours_num_{leaf_key}" not in st.session_state:
                    st.session_state[f"hours_num_{leaf_key}"] = st.session_state[f"hours_{leaf_key}"]

                col_slider, col_num = st.columns([3, 1])
                with col_slider:
                    st.slider(
                        "Hours (slider)", min_value=0.0, max_value=24.0, step=0.5,
                        key=f"hours_{leaf_key}", on_change=sync_hours_from_slider, args=(leaf_key,),
                        label_visibility="collapsed",
                    )
                with col_num:
                    st.number_input(
                        "Hours (exact)", min_value=0.0, max_value=24.0, step=0.5,
                        key=f"hours_num_{leaf_key}", on_change=sync_hours_from_number, args=(leaf_key,),
                        label_visibility="collapsed",
                    )

                if DEFAULT_HOURS.get(leaf_key) is not None:
                    st.button(
                        "Not sure? Use typical average",
                        key=f"btn_default_{leaf_key}", on_click=apply_default_hours, args=(leaf_key,),
                    )
                    if st.session_state.get(f"used_default_{leaf_key}", False):
                        st.markdown(
                            f'<p class="not-sure-caption">Set to typical average: {DEFAULT_HOURS[leaf_key]} hrs/day</p>',
                            unsafe_allow_html=True,
                        )

                st.write("")
                if st.button("✓ Add this appliance", key=f"confirm_{leaf_key}", use_container_width=True):
                    final_hours = st.session_state[f"hours_{leaf_key}"]
                    final_count = st.session_state[f"count_{leaf_key}"]
                    if final_count > 0 and final_hours > 0:
                        st.session_state.added_appliances[leaf_key] = {"count": final_count, "hours": final_hours}
                        st.success(f"✓ Added {display_name}. Choose another appliance from {category_name}, or switch category above.")
                        reset_to_category_subtypes()
                        st.rerun()
                    else:
                        st.warning("Set both count and hours above 0 before adding.")

            # ---------------- LEVEL 1: subtype selection ----------------
            if subtype is None:
                st.caption(CATEGORY_CAPTIONS.get(cat, "Choose the type of appliance"))
                subtypes = list(NAV_TREE[cat].keys())
                cols = st.columns(min(len(subtypes), 4))
                for i, st_name in enumerate(subtypes):
                    with cols[i % len(cols)]:
                        if st.button(st_name, key=f"subtype_btn_{cat}_{st_name}", use_container_width=True):
                            go_subtype(st_name)

            # ---------------- LEVEL 2: variant / size selection ----------------
            elif leaf is None:
                node = NAV_TREE[cat][subtype]

                if isinstance(node, dict):
                    # e.g. Air Conditioner -> {Window AC: [...], Split AC: [...]}
                    if SUBTYPE_CAPTIONS.get(subtype):
                        st.caption(SUBTYPE_CAPTIONS[subtype])

                    if st.session_state.nav_variant_group is None:
                        variant_names = list(node.keys())
                        cols = st.columns(min(len(variant_names), 4))
                        for i, v_name in enumerate(variant_names):
                            with cols[i % len(cols)]:
                                if st.button(v_name, key=f"variant_btn_{cat}_{subtype}_{v_name}", use_container_width=True):
                                    st.session_state.nav_variant_group = v_name
                    else:
                        v_name = st.session_state.nav_variant_group
                        st.caption(f"{v_name} — choose the size/tonnage")
                        leaf_options = node[v_name]
                        if len(leaf_options) == 1:
                            render_appliance_input(leaf_options[0], cat)
                        else:
                            cols2 = st.columns(min(len(leaf_options), 4))
                            for i, leaf_key in enumerate(leaf_options):
                                label = APPLIANCE_DISPLAY_NAMES.get(leaf_key, leaf_key)
                                with cols2[i % len(cols2)]:
                                    if st.button(label, key=f"leaf_btn_{leaf_key}", use_container_width=True):
                                        go_leaf(leaf_key)
                        st.write("")
                        st.button("← Change type", key=f"back_variant_{subtype}",
                                   on_click=lambda: st.session_state.update(nav_variant_group=None))
                else:
                    # subtype maps directly to a flat list of leaf keys
                    leaf_options = node
                    if SUBTYPE_CAPTIONS.get(subtype):
                        st.caption(SUBTYPE_CAPTIONS[subtype])

                    if len(leaf_options) == 1:
                        # Single-option appliance (e.g. WiFi Router, Microwave) —
                        # render input directly, NO rerun, NO state loop.
                        render_appliance_input(leaf_options[0], cat)
                    else:
                        st.caption("Choose the size/type")
                        cols2 = st.columns(min(len(leaf_options), 4))
                        for i, leaf_key in enumerate(leaf_options):
                            label = APPLIANCE_DISPLAY_NAMES.get(leaf_key, leaf_key)
                            with cols2[i % len(cols2)]:
                                if st.button(label, key=f"leaf_btn_{leaf_key}", use_container_width=True):
                                    go_leaf(leaf_key)

            # ---------------- LEVEL 3: final input (multi-variant path) ----------------
            else:
                render_appliance_input(leaf, cat)

    # ============================================================
    # RESULTS & RECOMMENDATIONS STAGE (Page 3)
    # ============================================================
    elif st.session_state.stage == "results":
        appliance_inputs = st.session_state.added_appliances
        units_consumed = calculate_units_consumed(appliance_inputs)
        real_bill = calculate_slab_bill(units_consumed, city)

        if st.button("← Edit appliances"):
            st.session_state.stage = "input"
            st.rerun()

        st.subheader("💰 Your Estimated Bill")
        st.metric("Your Estimated Bill", format_currency(real_bill))
        st.caption(f"Based on {units_consumed} kWh consumed, using {city}'s official tariff rates for {month_name}.")

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
        tips = []
        ac_keys = [k for k in appliance_inputs if "AC" in k]
        ac_hours_max = max([appliance_inputs[k]["hours"] for k in ac_keys], default=0)
        if len(ac_keys) >= 2 and ac_hours_max >= 6:
            tips.append(("warning", "Your air conditioners run for long hours daily. Switching to Eco mode can lower your bill."))
        if units_consumed > 400:
            tips.append(("info", "Your usage is high enough to fall into a costlier tariff slab. Reducing usage even slightly can help."))
        if tips:
            for tip_type, message in tips:
                getattr(st, tip_type)(message)
        else:
            st.success("Your usage looks efficient. No changes needed right now.")

        st.divider()

        with st.expander("What's driving your bill", expanded=True):
            contributions = {}
            for k, v in appliance_inputs.items():
                wattage = APPLIANCE_WATTAGE.get(k, 0)
                duty = DUTY_CYCLE.get(k, 1.0)
                contributions[k] = v["count"] * v["hours"] * wattage * duty

            total = sum(contributions.values())
            if total == 0:
                st.info("No appliances added yet.")
            else:
                sorted_items = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
                top_name = APPLIANCE_DISPLAY_NAMES.get(sorted_items[0][0], sorted_items[0][0])
                st.write(f"**{top_name}** has the biggest effect on your bill.")
                st.write("")
                for k, value in sorted_items:
                    share = value / total
                    display_name = APPLIANCE_DISPLAY_NAMES.get(k, k)
                    tag = "High impact" if share >= 0.30 else "Medium impact" if share >= 0.10 else "Low impact"
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.progress(share, text=display_name)
                    with col_b:
                        st.caption(tag)

        with st.expander("Your inputs"):
            summary_rows = [
                {"Appliance": APPLIANCE_DISPLAY_NAMES.get(k, k), "Count": v["count"], "Hours/day": v["hours"]}
                for k, v in appliance_inputs.items()
            ]
            st.dataframe(pd.DataFrame(summary_rows), hide_index=True, use_container_width=True)
            st.caption(f"{city} · {month_name}")

except Exception as e:
    # Catches rare widget-key clashes from rapid clicking WITHOUT wiping
    # session_state — this is what was kicking users back to the login
    # screen before. The user stays logged in and can just retry.
    st.error("Something glitched for a moment. Please tap again — your login and progress are safe.")
    st.caption(f"(Technical detail: {type(e).__name__})")
