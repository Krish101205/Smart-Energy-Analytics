# ============================================================
# STEP 1: Appliance wattage table + units (kWh) calculation
# ============================================================
APPLIANCE_WATTAGE = {
    "Fan": 75,
    "Refrigerator": 150,
    "AirConditioner": 1500,
    "Television": 100,
    "Monitor": 40,
    "MotorPump": 750,
}


def calculate_units_consumed(
    fan, fan_hours,
    refrigerator, refrigerator_hours,
    ac, ac_hours,
    tv, tv_hours,
    monitor, monitor_hours,
    motor, motor_hours,
):
    """
    Estimates real electricity units (kWh) consumed in a month.
    Each appliance now has its OWN daily usage hours, which is far more
    realistic than sharing one 'monthly hours' number across everything
    (a fridge runs ~24 hrs/day, an AC maybe 6-8 hrs/day — they're never equal).

    units (kWh) = sum over appliances of:
        (count * wattage * hours_per_day * 30 days) / 1000
    """
    daily_watt_hours = (
        fan * APPLIANCE_WATTAGE["Fan"] * fan_hours
        + refrigerator * APPLIANCE_WATTAGE["Refrigerator"] * refrigerator_hours
        + ac * APPLIANCE_WATTAGE["AirConditioner"] * ac_hours
        + tv * APPLIANCE_WATTAGE["Television"] * tv_hours
        + monitor * APPLIANCE_WATTAGE["Monitor"] * monitor_hours
        + motor * APPLIANCE_WATTAGE["MotorPump"] * motor_hours
    )
    units_consumed = (daily_watt_hours * 30) / 1000  # 30 days/month, Wh -> kWh
    return round(units_consumed, 2)
# ============================================================
# STEP 2: Real city-wise tariff slabs (based on 2025-26 SERC/DISCOM data)
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
# STEP 3: Calculate real bill using slab-based tariff
# ============================================================
def calculate_slab_bill(units_consumed, city):
    """
    Calculates the electricity bill using real, city-specific slab tariffs.
    Returns None if the city isn't in our tariff table.

    Example: if slabs are [(100, 3.5), (300, 5.0), (None, 7.0)]
    and units_consumed = 250, then:
        - first 100 units  -> 100 * 3.5
        - next 150 units   -> 150 * 5.0   (100 to 250)
    """
    if city not in TARIFF_SLABS:
        return None

    slabs = TARIFF_SLABS[city]
    remaining_units = units_consumed
    previous_limit = 0
    total_bill = 0.0

    for units_upto, rate in slabs:
        if units_upto is None:
            # Last slab — everything remaining is billed at this rate
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
    test_units = calculate_units_consumed(
        fan=2, fan_hours=8,
        refrigerator=1, refrigerator_hours=24,
        ac=1, ac_hours=6,
        tv=1, tv_hours=4,
        monitor=1, monitor_hours=3,
        motor=0, motor_hours=0,
    )
    print("Units consumed:", test_units, "kWh")

    for city in ["New Delhi", "Mumbai", "Chennai", "Shimla"]:
        bill = calculate_slab_bill(test_units, city)
        print(f"Real bill in {city}: ₹{bill}")