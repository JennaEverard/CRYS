import math
import numpy as np

def calc_sensitivity(fA_21):
    print(fA_21)
    # convert these to input fields
    small_vol = 0.1903106576 #mL or cc
    large_vol_diameter = 15.2  # cm
    large_vol_height = 34.608  # cm
    temperature = 30.8  # celsius
    relative_humidity = 45.6  # %
    pressure = 992.5  # mbar

    radius = large_vol_diameter / 2
    large_volume = math.pi * (radius ** 2) * large_vol_height

    # Determining pressure of dry air
    pressure_function = 1.0016 + 3.15 * 10 ** -6 * pressure - 0.074 * pressure ** -1
    saturation_vapor_pressure = pressure_function * 6.1094 * math.exp((17.625 * temperature) / (243.04 + temperature))
    actual_vapor_pressure = (relative_humidity / 100) * saturation_vapor_pressure  # mbar

    pressure_dry_air = pressure - actual_vapor_pressure

    # Neon is 0.0018% of atmosphere
    pressure_neon = pressure_dry_air * 0.000018  # mbar
    pressure_neon_Pa = pressure_neon * 100  # Pa

    # First loaded into small volume - calculate moles of neon there
    small_volume_m3 = small_vol * 0.000001  # m^3
    R = 8.314  # m^3 Pa / K mol
    temp_K = temperature + 273.15  # K
    moles_small_volume = (pressure_neon_Pa * small_volume_m3) / (R * temp_K)

    # Use P1 V1 = P2 V2 to calculate neon pressure in large volume
    large_volume_m3 = large_volume * 0.000001  # m^3
    pressure_neon_large = (pressure_neon_Pa * small_volume_m3) / large_volume_m3

    # Now calculate moles of neon when small volume is filled from large volume
    moles_neon = (pressure_neon_large * small_volume_m3) / (R * temp_K)
    moles_21 = moles_neon * 0.0027
    print(moles_21)

    return fA_21 / moles_21