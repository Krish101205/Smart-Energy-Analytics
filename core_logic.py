# ============================================================
# STEP 1: Appliance wattage database (locked version)
# ============================================================
# Wattage values represent the TYPICAL/AVERAGE rating for that
# appliance range/type — not an exact spec. Users pick the closest
# match to their device rather than needing to know exact watts.

APPLIANCE_WATTAGE = {
    # Cooling & Climate
    "WindowAC_1.0Ton": 1200,
    "WindowAC_1.5Ton": 1800,
    "WindowAC_2.0Ton": 2200,
    "SplitAC_1.0Ton": 1000,
    "SplitAC_1.5Ton": 1500,
    "SplitAC_2.0Ton": 2000,
    "Cooler": 200,
    "CeilingFan_Standard": 75,
    "CeilingFan_BLDC": 30,
    "RoomHeater_Fan": 1500,
    "RoomHeater_OilFilled": 2000,
    "ExhaustFan": 40,

    # Kitchen
    "Refrigerator_SingleDoor": 100,
    "Refrigerator_DoubleDoor": 150,
    "Refrigerator_SideBySide": 250,
    "MicrowaveOven": 1200,
    "InductionCooktop": 1500,
    "AirFryer": 1500,
    "ElectricKettle": 1500,
    "MixerGrinder": 500,

    # Lighting & Routine
    "LEDBulb": 9,
    "TubeLight_LED": 20,
    "TubeLight_Legacy": 40,
    "WiFiRouter": 12,

    # Water & Laundry
    "WashingMachine_Cold": 500,
    "WashingMachine_Hot": 2200,
    "Geyser_Instant": 3000,
    "Geyser_Storage": 2000,
    "MotorPump_Half_HP": 375,
    "MotorPump_One_HP": 750,
    "WaterPurifier_RO": 60,

    # Entertainment & IT
    "Television_Small": 60,
    "Television_Large": 120,
    "Television_Old_CRT": 150,
    "Monitor": 40,
    "Laptop_Charger": 65,
    "GamingConsole": 150,

    # Utility
    "ElectricIron_Dry": 750,
    "ElectricIron_Steam": 1200,
    "VacuumCleaner": 1200,

    # Mobile Charging
    "MobileCharger_Slow": 10,
    "MobileCharger_Standard": 18,
    "MobileCharger_Fast": 33,
    "MobileCharger_UltraFast": 65,
}


# ============================================================
# Duty cycle table
# ------------------------------------------------------------
# Only compressor/thermostat-cycled appliances go here. Everything
# NOT in this dict defaults to duty_cycle = 1.0 (full wattage x hours),
# which is correct for fans, lights, TVs, chargers, etc.
# ============================================================
DUTY_CYCLE = {
    "WindowAC_1.0Ton": 0.65,
    "WindowAC_1.5Ton": 0.65,
    "WindowAC_2.0Ton": 0.65,
    "SplitAC_1.0Ton": 0.65,
    "SplitAC_1.5Ton": 0.65,
    "SplitAC_2.0Ton": 0.65,
    "Refrigerator_SingleDoor": 0.35,
    "Refrigerator_DoubleDoor": 0.35,
    "Refrigerator_SideBySide": 0.35,
    "Geyser_Instant": 0.40,
    "Geyser_Storage": 0.40,
    "RoomHeater_Fan": 0.50,
    "RoomHeater_OilFilled": 0.50,
    "WaterPurifier_RO": 0.30,
}


# ============================================================
# Display names — user-facing labels with visible ranges
# ============================================================
APPLIANCE_DISPLAY_NAMES = {
    "WindowAC_1.0Ton": "Window AC — 1 Ton",
    "WindowAC_1.5Ton": "Window AC — 1.5 Ton",
    "WindowAC_2.0Ton": "Window AC — 2 Ton",
    "SplitAC_1.0Ton": "Split AC — 1 Ton (Inverter/Non-Inverter)",
    "SplitAC_1.5Ton": "Split AC — 1.5 Ton (Inverter/Non-Inverter)",
    "SplitAC_2.0Ton": "Split AC — 2 Ton (Inverter/Non-Inverter)",
    "Cooler": "Air Cooler",
    "CeilingFan_Standard": "Ceiling Fan — Regular (70-80W)",
    "CeilingFan_BLDC": "Ceiling Fan — 5-Star Energy Saving (28-35W)",
    "RoomHeater_Fan": "Room Heater — Fan/Blower Type (1200-1500W)",
    "RoomHeater_OilFilled": "Room Heater — Oil Filled Radiator (1800-2200W)",
    "ExhaustFan": "Exhaust Fan (Kitchen/Bathroom)",

    "Refrigerator_SingleDoor": "Refrigerator — Single Door (Small, 150-200L)",
    "Refrigerator_DoubleDoor": "Refrigerator — Double Door (Medium, 250-350L)",
    "Refrigerator_SideBySide": "Refrigerator — Side-by-Side / Large (500L+)",
    "MicrowaveOven": "Microwave Oven",
    "InductionCooktop": "Induction Cooktop / Stove",
    "AirFryer": "Air Fryer",
    "ElectricKettle": "Electric Kettle",
    "MixerGrinder": "Mixer Grinder",

    "LEDBulb": "LED Bulb",
    "TubeLight_LED": "Tube Light — LED (18-22W)",
    "TubeLight_Legacy": "Tube Light — Old/Tubular (36-40W)",
    "WiFiRouter": "WiFi Router",

    "WashingMachine_Cold": "Washing Machine — No Water Heater (400-600W)",
    "WashingMachine_Hot": "Washing Machine — With Water Heater (2000-2400W)",
    "Geyser_Instant": "Water Geyser — Instant (3-6L, 2500-3500W)",
    "Geyser_Storage": "Water Geyser — Storage (10-25L, 1500-2500W)",
    "MotorPump_Half_HP": "Motor Water Pump — 0.5 HP (Home Use)",
    "MotorPump_One_HP": "Motor Water Pump — 1 HP (Borewell/Deep)",
    "WaterPurifier_RO": "Water Purifier (RO)",

    "Television_Small": "Television — Small LED (24-32 inch)",
    "Television_Large": "Television — Large LED (40-55 inch)",
    "Television_Old_CRT": "Television — Old CRT/Plasma",
    "Monitor": "Computer Monitor",
    "Laptop_Charger": "Laptop Charger",
    "GamingConsole": "Gaming Console (PS5/Xbox)",

    "ElectricIron_Dry": "Electric Iron — Dry (700-800W)",
    "ElectricIron_Steam": "Electric Iron — Steam (1000-1600W)",
    "VacuumCleaner": "Vacuum Cleaner",

    "MobileCharger_Slow": "Mobile Charger — Slow (5-10W)",
    "MobileCharger_Standard": "Mobile Charger — Standard (10-20W)",
    "MobileCharger_Fast": "Mobile Charger — Fast (20-33W)",
    "MobileCharger_UltraFast": "Mobile Charger — Ultra Fast (45-67W+)",
}


# ============================================================
# Category grouping — for grouped expanders in the UI (Step 2)
# Each category also carries an emoji, used ONLY at the category
# header level in the UI (not per-appliance-row).
# ============================================================
APPLIANCE_CATEGORIES = {
    "❄️ Cooling & Climate": [
        "WindowAC_1.0Ton", "WindowAC_1.5Ton", "WindowAC_2.0Ton",
        "SplitAC_1.0Ton", "SplitAC_1.5Ton", "SplitAC_2.0Ton",
        "Cooler", "CeilingFan_Standard", "CeilingFan_BLDC",
        "RoomHeater_Fan", "RoomHeater_OilFilled", "ExhaustFan",
    ],
    "🍳 Kitchen": [
        "Refrigerator_SingleDoor", "Refrigerator_DoubleDoor", "Refrigerator_SideBySide",
        "MicrowaveOven", "InductionCooktop", "AirFryer", "ElectricKettle", "MixerGrinder",
    ],
    "💡 Lighting & Routine": [
        "LEDBulb", "TubeLight_LED", "TubeLight_Legacy", "WiFiRouter",
    ],
    "🚿 Water & Laundry": [
        "WashingMachine_Cold", "WashingMachine_Hot",
        "Geyser_Instant", "Geyser_Storage",
        "MotorPump_Half_HP", "MotorPump_One_HP", "WaterPurifier_RO",
    ],
    "📺 Entertainment & IT": [
        "Television_Small", "Television_Large", "Television_Old_CRT",
        "Monitor", "Laptop_Charger", "GamingConsole",
    ],
    "🧺 Utility": [
        "ElectricIron_Dry", "ElectricIron_Steam", "VacuumCleaner",
    ],
    "📱 Mobile Charging": [
        "MobileCharger_Slow", "MobileCharger_Standard",
        "MobileCharger_Fast", "MobileCharger_UltraFast",
    ],
}


# ============================================================
# Helper captions — shown once per category in the UI (Step 2)
# ============================================================
CATEGORY_HELPER_TEXT = {
    "❄️ Cooling & Climate": "Not sure of your AC's tonnage? Check the sticker on the indoor/outdoor unit, or your purchase invoice.",
    "🍳 Kitchen": "Most kitchen appliances draw similar power regardless of brand — just enter how many you use.",
    "💡 Lighting & Routine": "Count all bulbs/tubes of that type in your home, not just one room.",
    "🚿 Water & Laundry": "Check your geyser/pump's rating plate if unsure — it's usually printed in watts (W) near the power cord.",
    "📺 Entertainment & IT": "Screen size is the best guide here — measure diagonally if unsure.",
    "🧺 Utility": "",
    "📱 Mobile Charging": "Check the wattage printed on your charger brick (e.g. '5V⎓3A' ≈ 15W) or your phone's box to pick the closest match.",
}


# ============================================================
# Default / typical daily usage hours per appliance
# ------------------------------------------------------------
# Used ONLY when the user taps "Not sure?" next to a slider in the
# UI (Step 2). Never silently pre-filled — always an explicit,
# user-triggered action so the number stays honest/transparent.
# ============================================================
DEFAULT_HOURS = {
    # Always-on / near-constant
    "Refrigerator_SingleDoor": 24,
    "Refrigerator_DoubleDoor": 24,
    "Refrigerator_SideBySide": 24,
    "WiFiRouter": 24,

    # Daily but limited
    "CeilingFan_Standard": 8,
    "CeilingFan_BLDC": 8,
    "LEDBulb": 5,
    "TubeLight_LED": 5,
    "TubeLight_Legacy": 5,
    "Television_Small": 3,
    "Television_Large": 3,
    "Television_Old_CRT": 3,
    "WindowAC_1.0Ton": 6,
    "WindowAC_1.5Ton": 6,
    "WindowAC_2.0Ton": 6,
    "SplitAC_1.0Ton": 6,
    "SplitAC_1.5Ton": 6,
    "SplitAC_2.0Ton": 6,
    "Cooler": 7,

    # Short / occasional bursts
    "Geyser_Instant": 1,
    "Geyser_Storage": 1,
    "WashingMachine_Cold": 1,
    "WashingMachine_Hot": 1,
    "ElectricIron_Dry": 0.5,
    "ElectricIron_Steam": 0.5,
    "MicrowaveOven": 0.5,
    "InductionCooktop": 1,
    "ElectricKettle": 0.5,
    "AirFryer": 0.5,
    "MixerGrinder": 0.3,
    "VacuumCleaner": 0.5,

    # Situational, lower default
    "RoomHeater_Fan": 3,
    "RoomHeater_OilFilled": 3,
    "MotorPump_Half_HP": 1,
    "MotorPump_One_HP": 1,
    "ExhaustFan": 2,
    "WaterPurifier_RO": 2,
    "Laptop_Charger": 4,
    "GamingConsole": 2,
    "MobileCharger_Slow": 2,
    "MobileCharger_Standard": 2,
    "MobileCharger_Fast": 2,
    "MobileCharger_UltraFast": 2,
    "Monitor": 5,
}


# ============================================================
# STEP 1 CORE FIX: units consumed calculation
# ------------------------------------------------------------
# Refactored to accept a dict instead of 12 hardcoded params.
# This fixes the original bug: duty cycle is now applied to
# compressor/thermostat appliances instead of full wattage x
# hours for everything.
# ============================================================
def calculate_units_consumed(appliance_inputs: dict) -> float:
    """
    appliance_inputs = {
        "SplitAC_1.5Ton": {"count": 1, "hours": 6},
        "Refrigerator_DoubleDoor": {"count": 1, "hours": 24},
        "CeilingFan_Standard": {"count": 3, "hours": 8},
        ...
    }

    units (kWh) = sum over appliances of:
        (count * wattage * duty_cycle * hours_per_day * 30 days) / 1000

    Appliances not in DUTY_CYCLE default to duty_cycle = 1.0
    (full wattage x hours, correct for non-cycling devices).
    """
    total_daily_watt_hours = 0

    for appliance, values in appliance_inputs.items():
        count = values.get("count", 0)
        hours = values.get("hours", 0)
        wattage = APPLIANCE_WATTAGE.get(appliance, 0)
        duty = DUTY_CYCLE.get(appliance, 1.0)

        total_daily_watt_hours += count * wattage * duty * hours

    units_consumed = (total_daily_watt_hours * 30) / 1000  # Wh -> kWh, 30 days/month
    return round(units_consumed, 2)


# ============================================================
# Real city-wise tariff slabs (unchanged from original)
# ============================================================
TARIFF_SLABS = {
    "New Delhi":    [(200, 3.00), (400, 4.50), (600, 6.50), (800, 7.00), (None, 8.00)],
    "Mumbai":       [(100, 4.25), (300, 10.25), (500, 13.80), (None, 13.20)],
    "Pune":         [(100, 4.25), (300, 10.25), (500, 13.80), (None, 13.20)],
    "Navi Mumbai":  [(100, 4.25), (300, 10.25), (500, 13.80), (None, 13.20)],
    "Nagpur":       [(100, 4.25), (300, 10.25), (500, 13.80), (None, 13.20)],
    "Ratnagiri":    [(100, 4.25), (300, 10.25), (500, 13.80), (None, 13.20)],
    "Ahmedabad":    [(50, 3.05), (250, 4.25), (None, 5.20)],
    "Vadodara":     [(50, 3.05), (250, 4.25), (None, 5.20)],
    "Dahej":        [(50, 3.05), (250, 4.25), (None, 5.20)],
    "Hyderabad":    [(100, 2.60), (200, 4.50), (400, 7.00), (None, 9.00)],
    "Chennai":      [(100, 0.00), (200, 1.50), (500, 3.00), (None, 6.00)],
    "Kolkata":      [(100, 4.50), (300, 6.00), (None, 7.50)],
    "Faridabad":    [(50, 2.20), (150, 2.95), (300, 5.25), (500, 6.45), (None, 7.10)],
    "Gurgaon":      [(50, 2.20), (150, 2.95), (300, 5.25), (500, 6.45), (None, 7.10)],
    "Noida":        [(150, 5.50), (300, 6.00), (500, 6.50), (None, 6.85)],
    "Shimla":       [(125, 0.00), (300, 4.17), (None, 6.76)],
}


# ============================================================
# Calculate real bill using slab-based tariff (unchanged)
# ============================================================
def calculate_slab_bill(units_consumed, city):
    """
    Calculates the electricity bill using real, city-specific slab tariffs.
    Returns None if the city isn't in our tariff table.
    """
    if city not in TARIFF_SLABS:
        return None

    slabs = TARIFF_SLABS[city]
    remaining_units = units_consumed
    previous_limit = 0
    total_bill = 0.0

    for units_upto, rate in slabs:
        if units_upto is None:
            total_bill += remaining_units * rate
            remaining_units = 0
            break

        slab_size = units_upto - previous_limit
        units_in_this_slab = min(remaining_units, slab_size)

        if units_in_this_slab <= 0:
            break

        total_bill += units_in_this_slab * rate
        remaining_units -= units_in_this_slab
        previous_limit = units_upto

    return round(total_bill, 2)


# ============================================================
# Quick test (only runs when you execute this file directly)
# ============================================================
if __name__ == "__main__":
    # Simulate a household close to your friend's real scenario
    test_inputs = {
        "SplitAC_1.5Ton": {"count": 1, "hours": 6},
        "Refrigerator_DoubleDoor": {"count": 1, "hours": 24},
        "CeilingFan_Standard": {"count": 3, "hours": 10},
        "TubeLight_LED": {"count": 4, "hours": 6},
        "LEDBulb": {"count": 4, "hours": 6},
        "Television_Large": {"count": 1, "hours": 4},
        "WiFiRouter": {"count": 1, "hours": 24},
        "WashingMachine_Cold": {"count": 1, "hours": 1},
        "MobileCharger_Standard": {"count": 2, "hours": 3},
    }

    test_units = calculate_units_consumed(test_inputs)
    print("Units consumed:", test_units, "kWh")
    print("(Target: your friend's real bill was ~450-500 units)")

    for city in ["New Delhi", "Mumbai", "Chennai", "Shimla"]:
        bill = calculate_slab_bill(test_units, city)
        print(f"Real bill in {city}: ₹{bill}")