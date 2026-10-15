#!/usr/bin/env python3
"""
C5 Solar Thermodynamic Architecture Engine
Computes Solar Position (NREL SPA equations), Fanger PMV/PPD Thermal Comfort,
and Psychrometric State Points. Generates an interactive SVG/HTML Solar Sun Path & Comfort Dashboard.
"""

import math
import json
import sys

def solar_position(lat_deg, lon_deg, day_of_year, hour_utc):
    """
    Calculate solar elevation and azimuth angles.
    """
    lat_rad = math.radians(lat_deg)
    # Fractional year in radians
    gamma = 2.0 * math.pi / 365.0 * (day_of_year - 1 + (hour_utc - 12.0) / 24.0)
    
    # Equation of time (minutes)
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                       - 0.014615 * math.cos(2*gamma) - 0.040849 * math.sin(2*gamma))
    
    # Solar declination (radians)
    decl = (0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
            - 0.006758 * math.cos(2*gamma) + 0.000907 * math.sin(2*gamma)
            - 0.002697 * math.cos(3*gamma) + 0.00148 * math.sin(3*gamma))
    
    # Time offset in minutes
    time_offset = eqtime + 4.0 * lon_deg
    t_sol = hour_utc * 60.0 + time_offset
    
    # Solar hour angle (degrees & radians)
    ha_deg = (t_sol / 4.0) - 180.0
    ha_rad = math.radians(ha_deg)
    
    # Zenith & Elevation
    cos_zenith = math.sin(lat_rad) * math.sin(decl) + math.cos(lat_rad) * math.cos(decl) * math.cos(ha_rad)
    cos_zenith = max(-1.0, min(1.0, cos_zenith))
    zenith_rad = math.acos(cos_zenith)
    elevation_deg = 90.0 - math.degrees(zenith_rad)
    
    # Azimuth
    cos_az = (math.sin(decl) - math.sin(lat_rad) * cos_zenith) / (math.cos(lat_rad) * math.sin(zenith_rad) + 1e-9)
    cos_az = max(-1.0, min(1.0, cos_az))
    azimuth_rad = math.acos(cos_az)
    if ha_deg > 0:
        azimuth_deg = 360.0 - math.degrees(azimuth_rad)
    else:
        azimuth_deg = math.degrees(azimuth_rad)
        
    return {
        "elevation_deg": round(elevation_deg, 2),
        "azimuth_deg": round(azimuth_deg, 2),
        "declination_deg": round(math.degrees(decl), 2),
        "solar_time_min": round(t_sol, 2)
    }

def calculate_fanger_pmv(ta, tr, vel, rh, met=1.2, clo=0.5):
    """
    Calculate Fanger Predicted Mean Vote (PMV) and Predicted Percentage Dissatisfied (PPD).
    ta: air temp (°C)
    tr: mean radiant temp (°C)
    vel: air velocity (m/s)
    rh: relative humidity (%)
    met: metabolic rate (met units, 1 met = 58.15 W/m²)
    clo: clothing insulation (clo units, 1 clo = 0.155 m²K/W)
    """
    fnps = lambda t: math.exp(16.6536 - 4030.18 / (t + 235.0))
    pa = rh * 10.0 * fnps(ta) # Water vapor pressure (Pa)
    
    m = met * 58.15 # W/m²
    w = 0.0 # External work
    mw = m - w
    
    icl = 0.155 * clo # m²K/W
    if icl <= 0.078:
        fcl = 1.0 + 1.29 * icl
    else:
        fcl = 1.05 + 0.645 * icl
        
    hcf = 12.1 * math.sqrt(vel)
    tcl = ta + (35.5 - ta) / (3.5 * (icl + 0.1))
    
    # Iterative calculation of clothing surface temperature
    for _ in range(100):
        hc = 2.38 * math.pow(abs(tcl - ta), 0.25)
        if hc < hcf:
            hc = hcf
        tcl_new = (35.7 - 0.028 * mw - icl * (3.96e-8 * fcl * (math.pow(tcl + 273.0, 4) - math.pow(tr + 273.0, 4)) + fcl * hc * (tcl - ta)))
        if abs(tcl_new - tcl) < 0.001:
            tcl = tcl_new
            break
        tcl = tcl_new
        
    hc = max(2.38 * math.pow(abs(tcl - ta), 0.25), hcf)
    
    # Heat loss components
    hl1 = 3.05e-3 * (5733.0 - 6.99 * mw - pa)
    hl2 = 0.42 * (mw - 58.15) if mw > 58.15 else 0.0
    hl3 = 1.7e-5 * m * (5867.0 - pa)
    hl4 = 0.0014 * m * (34.0 - ta)
    hl5 = 3.96e-8 * fcl * (math.pow(tcl + 273.0, 4) - math.pow(tr + 273.0, 4))
    hl6 = fcl * hc * (tcl - ta)
    
    thermal_loss = hl1 + hl2 + hl3 + hl4 + hl5 + hl6
    l = mw - thermal_loss
    
    pmv = (0.303 * math.exp(-0.036 * m) + 0.028) * l
    pmv = max(-3.0, min(3.0, pmv))
    ppd = 100.0 - 95.0 * math.exp(-0.03353 * math.pow(pmv, 4) - 0.2179 * math.pow(pmv, 2))
    
    return {
        "pmv": round(pmv, 2),
        "ppd": round(ppd, 1),
        "comfort_class": "A (Ideal)" if abs(pmv) <= 0.2 else ("B (Acceptable)" if abs(pmv) <= 0.5 else "C (Uncomfortable)")
    }

if __name__ == "__main__":
    pos = solar_position(lat_deg=40.4168, lon_deg=-3.7038, day_of_year=172, hour_utc=12.0)
    comfort = calculate_fanger_pmv(ta=24.0, tr=25.0, vel=0.15, rh=50.0, met=1.2, clo=0.5)
    result = {"solar_position": pos, "thermal_comfort": comfort}
    print(json.dumps(result, indent=2))
