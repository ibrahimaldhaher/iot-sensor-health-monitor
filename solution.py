"""Lecture 1 - Python Programming Question: IoT Sensor Data.

The literal answer to the exercise, in plain Python with no dependencies and no
imports, so it can be read straight off the page or pasted into any interpreter.

    Write a Python program that:
      1. Stores the temperature and vibration measurements in two Python lists.
      2. Calculates the average temperature and average vibration.
      3. For each measurement, determines whether the machine is Normal or
         Abnormal using these rules:
             Temperature > 80 C  -> Abnormal
             Vibration    > 5.0  -> Abnormal
             Otherwise           -> Normal
      4. Prints the status of the machine for each measurement.
      5. Prints the total number of abnormal measurements.

The engineered version of the same logic - typed, configurable and unit-tested -
lives in ``src/iot_monitor/``.
"""

# 1. Measurements ----------------------------------------------------------
temperature = [72, 75, 83, 78, 85]
vibration = [2.1, 3.0, 6.2, 2.8, 5.5]

TEMPERATURE_LIMIT = 80.0
VIBRATION_LIMIT = 5.0

# 2. Averages --------------------------------------------------------------
average_temperature = sum(temperature) / len(temperature)
average_vibration = sum(vibration) / len(vibration)

print("IoT Sensor Data - Industrial Motor Monitoring")
print("=" * 52)
print(f"Average temperature : {average_temperature:.2f} C")
print(f"Average vibration   : {average_vibration:.2f}")
print("-" * 52)

# 3 & 4. Per-measurement status -------------------------------------------
abnormal_count = 0

for i in range(len(temperature)):
    t = temperature[i]
    v = vibration[i]

    if t > TEMPERATURE_LIMIT or v > VIBRATION_LIMIT:
        status = "Abnormal"
        abnormal_count += 1
    else:
        status = "Normal"

    print(f"Measurement {i + 1}: T = {t:5.1f} C | V = {v:4.2f} -> {status}")

# 5. Total abnormal measurements ------------------------------------------
print("-" * 52)
print(f"Total abnormal measurements: {abnormal_count} out of {len(temperature)}")
