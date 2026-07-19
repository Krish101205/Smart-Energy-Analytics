"""
generate_dataset.py
--------------------
Generates a NEW, realistic electricity bill dataset using core_logic.py's
real wattage-based unit calculation and real city tariff slabs.
"""

import random
import pandas as pd
from core_logic import calculate_units_consumed, calculate_slab_bill, TARIFF_SLABS

# Only use cities we have real tariff data for
CITIES = list(TARIFF_SLABS.keys())

NUM_ROWS = 45000


def generate_row():
    """Generates one realistic household's full data row, including REAL bill."""
    fan = random.randint(0, 8)
    refrigerator = random.randint(0, 2)
    ac = random.randint(0, 3)
    tv = random.randint(0, 3)
    monitor = random.randint(0, 3)
    motor = random.randint(0, 1)
    month = random.randint(1, 12)
    city = random.choice(CITIES)

    # Realistic daily usage hours per appliance type
    fan_hours = random.randint(0, 16) if fan > 0 else 0
    refrigerator_hours = 24 if refrigerator > 0 else 0  # fridges run all day
    ac_hours = random.randint(0, 10) if ac > 0 else 0
    tv_hours = random.randint(0, 8) if tv > 0 else 0
    monitor_hours = random.randint(0, 10) if monitor > 0 else 0
    motor_hours = random.randint(0, 3) if motor > 0 else 0

    units_consumed = calculate_units_consumed(
        fan, fan_hours,
        refrigerator, refrigerator_hours,
        ac, ac_hours,
        tv, tv_hours,
        monitor, monitor_hours,
        motor, motor_hours,
    )
    electricity_bill = calculate_slab_bill(units_consumed, city)

    return {
        "Fan": fan,
        "FanHours": fan_hours,
        "Refrigerator": refrigerator,
        "RefrigeratorHours": refrigerator_hours,
        "AirConditioner": ac,
        "AirConditionerHours": ac_hours,
        "Television": tv,
        "TelevisionHours": tv_hours,
        "Monitor": monitor,
        "MonitorHours": monitor_hours,
        "MotorPump": motor,
        "MotorPumpHours": motor_hours,
        "Month": month,
        "City": city,
        "UnitsConsumed": units_consumed,
        "ElectricityBill": electricity_bill,
    }


if __name__ == "__main__":
    rows = [generate_row() for _ in range(NUM_ROWS)]
    df = pd.DataFrame(rows)

    print(df.head(10))
    print("\nTotal rows generated:", len(df))
    print("\nBill stats:")
    print(df["ElectricityBill"].describe())

    # Save to a new CSV file (separate from the old one, so nothing old is overwritten)
    output_path = "data/raw/electricity_bill_dataset_v2.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved new dataset to: {output_path}")