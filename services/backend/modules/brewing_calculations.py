"""
Brewing calculation utilities.

This module implements a minimal set of formulas that are useful when
estimating beer characteristics during recipe design.  Each function
performs light validation and raises ValueError when the provided inputs
are outside of reasonable brewing ranges.
"""

from __future__ import annotations

import math
from typing import Union


Number = Union[int, float]

__all__ = [
    "calculate_abv",
    "calculate_attenuation",
    "calculate_ibu_tinseth",
    "calculate_srm_morey",
    "calculate_strike_water",
    "calculate_priming_sugar",
    "calculate_yeast_starter",
    "calculate_dilution",
    "calculate_carbonation",
    "calculate_water_chemistry",
    "calculate_mineral_additions",
    "calculate_salt_ion_contribution",
    "calculate_water_adjustment",
]


def _coerce_positive(value: Number, name: str, allow_zero: bool = False) -> float:
    """Convert a numeric input to float and validate positivity."""
    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric.") from exc

    if allow_zero:
        if numeric_value < 0:
            raise ValueError(f"{name} cannot be negative.")
    else:
        if numeric_value <= 0:
            raise ValueError(f"{name} must be greater than zero.")

    return numeric_value


def calculate_abv(original_gravity: Number, final_gravity: Number) -> float:
    """
    Calculate Alcohol by Volume (ABV) from original and final gravity readings.

    Formula: ABV = (OG - FG) * 131.25
    """
    og = _coerce_positive(original_gravity, "original_gravity")
    fg = _coerce_positive(final_gravity, "final_gravity")

    if og <= fg:
        raise ValueError("original_gravity must be greater than final_gravity.")

    return (og - fg) * 131.25


def calculate_attenuation(original_gravity: Number, final_gravity: Number) -> float:
    """
    Calculate apparent attenuation percentage from original and final gravity readings.

    Formula: Attenuation = ((OG - FG) / (OG - 1.0)) * 100

    Args:
        original_gravity: Original gravity reading (e.g., 1.050)
        final_gravity: Final gravity reading (e.g., 1.010)

    Returns:
        Attenuation percentage (e.g., 80.0 for 80% attenuation)
    """
    og = _coerce_positive(original_gravity, "original_gravity")
    fg = _coerce_positive(final_gravity, "final_gravity")

    if og <= fg:
        raise ValueError("original_gravity must be greater than final_gravity.")

    if og <= 1.0:
        raise ValueError("original_gravity must be greater than 1.0")

    attenuation = ((og - fg) / (og - 1.0)) * 100.0
    return max(attenuation, 0.0)


def calculate_ibu_tinseth(
    alpha_acid: Number,
    weight_oz: Number,
    boil_time_min: Number,
    batch_size_gal: Number,
    gravity: Number,
) -> float:
    """
    Estimate International Bitterness Units (IBU) using the Tinseth model.

    Args:
        alpha_acid: Hop alpha acid percentage (e.g., 12.0 for 12% AA).
        weight_oz: Hop weight in ounces.
        boil_time_min: Boil time for the hop addition in minutes.
        batch_size_gal: Batch size in gallons.
        gravity: Specific gravity of the wort during the boil.
    """
    aa_percent = _coerce_positive(alpha_acid, "alpha_acid", allow_zero=True)
    hop_weight = _coerce_positive(weight_oz, "weight_oz", allow_zero=True)
    boil_minutes = _coerce_positive(boil_time_min, "boil_time_min", allow_zero=True)
    batch_volume = _coerce_positive(batch_size_gal, "batch_size_gal")
    wort_gravity = _coerce_positive(gravity, "gravity")

    if aa_percent == 0 or hop_weight == 0 or boil_minutes == 0:
        return 0.0

    gravity_factor = 1.65 * math.pow(0.000125, wort_gravity - 1.0)
    time_factor = (1 - math.exp(-0.04 * boil_minutes)) / 4.15
    utilization = gravity_factor * time_factor
    alpha_fraction = aa_percent / 100.0

    # 7490 converts from ounces and gallons to milligrams per liter.
    ibu = (alpha_fraction * hop_weight * 7490 * utilization) / batch_volume
    return max(ibu, 0.0)


def calculate_srm_morey(
    grain_color: Number,
    grain_weight_lbs: Number,
    batch_size_gal: Number,
) -> float:
    """
    Estimate beer color using the Morey equation.

    Args:
        grain_color: Lovibond rating of the grain (or average for the grist).
        grain_weight_lbs: Total grain weight contributing to the color, in pounds.
        batch_size_gal: Batch size in gallons.
    """
    color = _coerce_positive(grain_color, "grain_color", allow_zero=True)
    grain_weight = _coerce_positive(
        grain_weight_lbs, "grain_weight_lbs", allow_zero=True
    )
    batch_volume = _coerce_positive(batch_size_gal, "batch_size_gal")

    if color == 0 or grain_weight == 0:
        return 0.0

    mcu = (grain_weight * color) / batch_volume
    return 1.4922 * math.pow(mcu, 0.6859)


def calculate_strike_water(
    grain_weight_lbs: Number,
    mash_temp_f: Number,
    grain_temp_f: Number,
    water_to_grain_ratio: Number = 1.25,
) -> dict:
    """
    Calculate strike water temperature and volume for mashing.

    Args:
        grain_weight_lbs: Weight of grain in pounds.
        mash_temp_f: Target mash temperature in Fahrenheit.
        grain_temp_f: Current grain temperature in Fahrenheit.
        water_to_grain_ratio: Water to grain ratio in quarts per pound (default 1.25).

    Returns:
        Dictionary with 'volume_quarts' and 'temperature_f' keys.
    """
    grain_weight = _coerce_positive(grain_weight_lbs, "grain_weight_lbs")
    target_temp = _coerce_positive(mash_temp_f, "mash_temp_f")
    grain_temp = _coerce_positive(grain_temp_f, "grain_temp_f", allow_zero=True)
    ratio = _coerce_positive(water_to_grain_ratio, "water_to_grain_ratio")

    # Calculate water volume in quarts
    water_volume = grain_weight * ratio

    # Calculate strike water temperature using simplified infusion equation
    # Strike temp = (0.41/ratio) * (target - grain) + target
    temp_diff = target_temp - grain_temp
    strike_temp = target_temp + (0.41 / ratio) * temp_diff

    return {
        "volume_quarts": water_volume,
        "temperature_f": strike_temp,
    }


def calculate_priming_sugar(
    volume_gal: Number,
    carbonation_level: Number,
    sugar_type: str = "table",
) -> dict:
    """
    Calculate priming sugar needed for bottle carbonation.

    Args:
        volume_gal: Beer volume in gallons.
        carbonation_level: Target CO2 volumes (typically 2.0-2.8).
        sugar_type: Type of sugar ("table", "corn", "dme", "honey").

    Returns:
        Dictionary with 'grams' and 'oz' keys.
    """
    volume = _coerce_positive(volume_gal, "volume_gal")
    co2_volumes = _coerce_positive(carbonation_level, "carbonation_level")

    # Convert to liters
    volume_liters = volume * 3.78541

    # Sugar conversion factors (grams per liter per CO2 volume)
    sugar_factors = {
        "table": 4.0,  # Table sugar (sucrose)
        "corn": 3.6,  # Corn sugar (dextrose)
        "dme": 4.6,  # Dry malt extract
        "honey": 4.7,  # Honey
    }

    if sugar_type not in sugar_factors:
        raise ValueError(f"sugar_type must be one of {list(sugar_factors.keys())}")

    factor = sugar_factors[sugar_type]
    total_grams = co2_volumes * factor * volume_liters

    return {
        "grams": total_grams,
        "oz": total_grams / 28.3495,
    }


def calculate_yeast_starter(
    og: Number,
    volume_gal: Number,
    yeast_age_months: Number,
    target_cell_count: Number = None,
) -> dict:
    """
    Calculate yeast starter requirements.

    Args:
        og: Target original gravity.
        volume_gal: Batch volume in gallons.
        yeast_age_months: Age of yeast in months (0 = fresh).
        target_cell_count: Target cell count in billions (optional, calculated if not provided).

    Returns:
        Dictionary with 'cells_needed_billions', 'packages', and 'starter_size_ml' keys.
    """
    gravity = _coerce_positive(og, "og")
    volume = _coerce_positive(volume_gal, "volume_gal")
    age_months = _coerce_positive(yeast_age_months, "yeast_age_months", allow_zero=True)

    # Convert to liters
    volume_liters = volume * 3.78541

    # Calculate gravity in Plato (rough conversion)
    gravity_plato = ((gravity - 1) * 1000) / 4.0

    # Calculate cells needed (default pitch rate: 0.75M cells/mL/°P for ales)
    if target_cell_count is None:
        pitch_rate = 0.75  # million cells per mL per degree Plato
        cells_needed = (
            pitch_rate * (volume_liters * 1000) * gravity_plato / 1000
        )  # in billions
    else:
        cells_needed = _coerce_positive(target_cell_count, "target_cell_count")

    # Estimate viable cells per package (100B fresh, decreases ~20% per month)
    viability = max(0.2, 1.0 - (age_months * 0.2))
    cells_per_package = 100 * viability  # in billions

    # Calculate number of packages needed
    packages_needed = math.ceil(cells_needed / cells_per_package)

    # Estimate starter size needed (rough approximation: 1L starter per 100B cells growth)
    starter_size = max(
        1000, int((cells_needed - (packages_needed * cells_per_package)) * 10)
    )

    return {
        "cells_needed_billions": cells_needed,
        "packages": packages_needed,
        "starter_size_ml": starter_size,
    }


def calculate_dilution(
    current_og: Number,
    current_volume_gal: Number,
    target_og: Number,
) -> dict:
    """
    Calculate water needed to dilute wort to target gravity.

    Args:
        current_og: Current original gravity.
        current_volume_gal: Current volume in gallons.
        target_og: Target original gravity.

    Returns:
        Dictionary with 'water_to_add_gal' and 'final_volume_gal' keys.
    """
    current_gravity = _coerce_positive(current_og, "current_og")
    current_volume = _coerce_positive(current_volume_gal, "current_volume_gal")
    target_gravity = _coerce_positive(target_og, "target_og")

    if target_gravity >= current_gravity:
        return {
            "water_to_add_gal": 0.0,
            "final_volume_gal": current_volume,
        }

    # Calculate gravity points
    current_points = (current_gravity - 1) * 1000
    target_points = (target_gravity - 1) * 1000

    # Calculate final volume using dilution equation: C1*V1 = C2*V2
    final_volume = (current_points * current_volume) / target_points
    water_to_add = final_volume - current_volume

    return {
        "water_to_add_gal": water_to_add,
        "final_volume_gal": final_volume,
    }


def calculate_carbonation(
    temp_f: Number,
    co2_volumes: Number,
) -> dict:
    """
    Calculate carbonation pressure for a given temperature and CO2 volume.

    Args:
        temp_f: Beer temperature in Fahrenheit.
        co2_volumes: Desired CO2 volumes.

    Returns:
        Dictionary with 'psi' and 'bar' keys.
    """
    temperature = _coerce_positive(temp_f, "temp_f", allow_zero=True)
    volumes = _coerce_positive(co2_volumes, "co2_volumes")

    # Convert temperature to Celsius for calculation
    temp_c = (temperature - 32) * 5 / 9

    # Calculate dissolved CO2 at temperature (Henry's Law approximation)
    dissolved_co2 = 3.0378 - (0.050062 * temp_c) + (0.00026555 * temp_c * temp_c)

    # CO2 needed from pressure
    co2_from_pressure = volumes - dissolved_co2

    if co2_from_pressure <= 0:
        return {"psi": 0.0, "bar": 0.0}

    # Simplified pressure calculation (empirical formula)
    # PSI = (-16.6999 - 0.0101059 * T + 0.00116512 * T^2) + (0.173354 * T + 4.24267) * V
    psi = (-16.6999 - 0.0101059 * temp_f + 0.00116512 * temp_f * temp_f) + (
        0.173354 * temp_f + 4.24267
    ) * volumes

    return {
        "psi": max(0.0, psi),
        "bar": max(0.0, psi * 0.0689476),
    }


def calculate_water_chemistry(
    water_profile: dict,
    grain_bill_lbs: Number,
    target_ph: Number = 5.4,
) -> dict:
    """
    Estimate water adjustments for target mash pH.

    Args:
        water_profile: Dictionary with ion concentrations (calcium, magnesium, sodium,
                      chloride, sulfate, bicarbonate in ppm).
        grain_bill_lbs: Total grain weight in pounds.
        target_ph: Target mash pH (default 5.4).

    Returns:
        Dictionary with residual alkalinity and estimated pH.
    """
    _coerce_positive(grain_bill_lbs, "grain_bill_lbs")  # Validate but not used in calc
    target = _coerce_positive(target_ph, "target_ph")

    # Validate required keys
    required_keys = ["calcium", "magnesium", "bicarbonate"]
    for key in required_keys:
        if key not in water_profile:
            raise ValueError(f"water_profile must contain '{key}' key")

    calcium = _coerce_positive(water_profile["calcium"], "calcium", allow_zero=True)
    magnesium = _coerce_positive(
        water_profile["magnesium"], "magnesium", allow_zero=True
    )
    bicarbonate = _coerce_positive(
        water_profile["bicarbonate"], "bicarbonate", allow_zero=True
    )

    # Calculate alkalinity as CaCO3 equivalent
    alkalinity = bicarbonate * 0.8202

    # Calculate residual alkalinity (Kolbach formula)
    residual_alkalinity = alkalinity - (calcium / 3.5 + magnesium / 7.0)

    # Estimate mash pH (simplified)
    # Base pH from grain (typically around 5.8)
    base_ph = 5.8

    # Adjust for residual alkalinity (rough approximation: 1 mEq/L RA raises pH ~0.1)
    ph_adjustment = residual_alkalinity / 50.0
    estimated_ph = base_ph + ph_adjustment

    # Clamp pH to reasonable brewing range
    estimated_ph = max(5.0, min(6.0, estimated_ph))

    return {
        "residual_alkalinity": residual_alkalinity,
        "estimated_ph": estimated_ph,
        "ph_target": target,
        "ph_difference": estimated_ph - target,
    }


def calculate_salt_ion_contribution(
    salt_type: str,
    amount_grams: Number,
    water_volume_gal: Number,
) -> dict:
    """
    Calculate ion contribution from brewing salt additions.

    Args:
        salt_type: Type of salt (CaCl2, CaSO4, MgSO4, NaCl, NaHCO3, CaCO3, etc.)
        amount_grams: Amount of salt in grams
        water_volume_gal: Water volume in gallons

    Returns:
        Dictionary with ion contributions in ppm
    """
    amount = _coerce_positive(amount_grams, "amount_grams", allow_zero=True)
    volume = _coerce_positive(water_volume_gal, "water_volume_gal")

    if amount == 0:
        return {
            "calcium": 0.0,
            "magnesium": 0.0,
            "sodium": 0.0,
            "chloride": 0.0,
            "sulfate": 0.0,
            "bicarbonate": 0.0,
        }

    # Convert gallons to liters
    volume_liters = volume * 3.78541

    # Ion contribution factors (mg of ion per gram of salt)
    salt_factors = {
        "CaCl2": {"calcium": 272.6, "chloride": 482.6},  # Calcium Chloride (anhydrous)
        "CaCl2.2H2O": {"calcium": 272.6, "chloride": 482.6},  # Calcium Chloride dihydrate
        "CaSO4": {"calcium": 232.8, "sulfate": 557.7},  # Gypsum (Calcium Sulfate)
        "MgSO4": {"magnesium": 98.6, "sulfate": 389.6},  # Epsom Salt (Magnesium Sulfate)
        "MgSO4.7H2O": {"magnesium": 98.6, "sulfate": 389.6},  # Epsom Salt heptahydrate
        "NaCl": {"sodium": 393.4, "chloride": 606.6},  # Table Salt (Sodium Chloride)
        "NaHCO3": {"sodium": 274.2, "bicarbonate": 726.3},  # Baking Soda (Sodium Bicarbonate)
        "CaCO3": {"calcium": 400.4, "bicarbonate": 609.6},  # Chalk (Calcium Carbonate)
    }

    # Normalize salt type
    salt_type_normalized = salt_type.replace(" ", "").replace(".", "")
    
    # Try to find matching salt type
    salt_data = None
    for key in salt_factors:
        if key.replace(".", "").upper() == salt_type_normalized.upper():
            salt_data = salt_factors[key]
            break
    
    if not salt_data:
        raise ValueError(
            f"Unknown salt type '{salt_type}'. "
            f"Supported types: {', '.join(salt_factors.keys())}"
        )

    # Calculate ion contributions in ppm (mg/L)
    contributions = {
        "calcium": 0.0,
        "magnesium": 0.0,
        "sodium": 0.0,
        "chloride": 0.0,
        "sulfate": 0.0,
        "bicarbonate": 0.0,
    }

    for ion, factor in salt_data.items():
        # ppm = (grams of salt * mg of ion per gram) / liters
        contributions[ion] = (amount * factor / 1000.0) / volume_liters

    return contributions


def calculate_mineral_additions(
    source_profile: dict,
    target_profile: dict,
    water_volume_gal: Number,
) -> dict:
    """
    Calculate salt additions needed to adjust source water to target profile.

    Args:
        source_profile: Starting water profile with ion concentrations (ppm)
        target_profile: Target water profile with ion concentrations (ppm)
        water_volume_gal: Volume of water to treat in gallons

    Returns:
        Dictionary with recommended salt additions in grams and resulting profile
    """
    volume = _coerce_positive(water_volume_gal, "water_volume_gal")
    volume_liters = volume * 3.78541

    # Validate required keys
    required_ions = ["calcium", "magnesium", "sodium", "chloride", "sulfate", "bicarbonate"]
    for profile_name, profile in [("source_profile", source_profile), ("target_profile", target_profile)]:
        for ion in required_ions:
            if ion not in profile:
                raise ValueError(f"{profile_name} must contain '{ion}' key")

    # Calculate ion differences (target - source)
    differences = {}
    for ion in required_ions:
        source_val = _coerce_positive(profile[ion] if profile[ion] else 0, f"source_{ion}", allow_zero=True)
        target_val = _coerce_positive(target_profile[ion] if target_profile[ion] else 0, f"target_{ion}", allow_zero=True)
        differences[ion] = target_val - source_val

    # Calculate salt additions using a simplified approach
    # This uses a greedy algorithm to add salts in priority order
    additions = {
        "CaSO4": 0.0,  # Gypsum
        "CaCl2": 0.0,  # Calcium Chloride
        "MgSO4": 0.0,  # Epsom Salt
        "NaCl": 0.0,   # Table Salt
        "NaHCO3": 0.0, # Baking Soda
    }

    current_ions = {ion: float(source_profile[ion]) for ion in required_ions}

    # Add Gypsum (CaSO4) for calcium and sulfate
    if differences["calcium"] > 0 and differences["sulfate"] > 0:
        # Calculate grams needed: (ppm increase * liters) / (mg ion per gram of salt / 1000)
        ca_needed = (differences["calcium"] * volume_liters) / (232.8 / 1000.0)
        so4_needed = (differences["sulfate"] * volume_liters) / (557.7 / 1000.0)
        gypsum_grams = min(ca_needed, so4_needed)
        additions["CaSO4"] = max(0, gypsum_grams)
        
        # Update current ions
        contrib = calculate_salt_ion_contribution("CaSO4", additions["CaSO4"], volume)
        for ion in contrib:
            current_ions[ion] += contrib[ion]

    # Add Calcium Chloride for remaining calcium and chloride
    remaining_ca = target_profile["calcium"] - current_ions["calcium"]
    remaining_cl = target_profile["chloride"] - current_ions["chloride"]
    if remaining_ca > 0 and remaining_cl > 0:
        ca_needed = (remaining_ca * volume_liters) / (272.6 / 1000.0)
        cl_needed = (remaining_cl * volume_liters) / (482.6 / 1000.0)
        cacl2_grams = min(ca_needed, cl_needed)
        additions["CaCl2"] = max(0, cacl2_grams)
        
        contrib = calculate_salt_ion_contribution("CaCl2", additions["CaCl2"], volume)
        for ion in contrib:
            current_ions[ion] += contrib[ion]

    # Add Epsom Salt for magnesium and remaining sulfate
    remaining_mg = target_profile["magnesium"] - current_ions["magnesium"]
    remaining_so4 = target_profile["sulfate"] - current_ions["sulfate"]
    if remaining_mg > 0 and remaining_so4 > 0:
        mg_needed = (remaining_mg * volume_liters) / (98.6 / 1000.0)
        so4_needed = (remaining_so4 * volume_liters) / (389.6 / 1000.0)
        epsom_grams = min(mg_needed, so4_needed)
        additions["MgSO4"] = max(0, epsom_grams)
        
        contrib = calculate_salt_ion_contribution("MgSO4", additions["MgSO4"], volume)
        for ion in contrib:
            current_ions[ion] += contrib[ion]

    # Add Table Salt for remaining sodium and chloride
    remaining_na = target_profile["sodium"] - current_ions["sodium"]
    remaining_cl = target_profile["chloride"] - current_ions["chloride"]
    if remaining_na > 0 and remaining_cl > 0:
        na_needed = (remaining_na * volume_liters) / (393.4 / 1000.0)
        cl_needed = (remaining_cl * volume_liters) / (606.6 / 1000.0)
        nacl_grams = min(na_needed, cl_needed)
        additions["NaCl"] = max(0, nacl_grams)
        
        contrib = calculate_salt_ion_contribution("NaCl", additions["NaCl"], volume)
        for ion in contrib:
            current_ions[ion] += contrib[ion]

    # Add Baking Soda for remaining sodium and bicarbonate
    remaining_na = target_profile["sodium"] - current_ions["sodium"]
    remaining_hco3 = target_profile["bicarbonate"] - current_ions["bicarbonate"]
    if remaining_na > 0 and remaining_hco3 > 0:
        na_needed = (remaining_na * volume_liters) / (274.2 / 1000.0)
        hco3_needed = (remaining_hco3 * volume_liters) / (726.3 / 1000.0)
        nahco3_grams = min(na_needed, hco3_needed)
        additions["NaHCO3"] = max(0, nahco3_grams)
        
        contrib = calculate_salt_ion_contribution("NaHCO3", additions["NaHCO3"], volume)
        for ion in contrib:
            current_ions[ion] += contrib[ion]

    # Round additions to 2 decimal places
    for salt in additions:
        additions[salt] = round(additions[salt], 2)

    # Round resulting ions to 1 decimal place
    for ion in current_ions:
        current_ions[ion] = round(current_ions[ion], 1)

    return {
        "additions": additions,
        "resulting_profile": current_ions,
        "target_profile": {ion: float(target_profile[ion]) for ion in required_ions},
    }


def calculate_water_adjustment(
    water_profile: dict,
    salt_additions: dict,
    water_volume_gal: Number,
) -> dict:
    """
    Calculate resulting water chemistry from salt additions.

    Args:
        water_profile: Starting water profile with ion concentrations (ppm)
        salt_additions: Dictionary of salt additions in grams (e.g., {"CaSO4": 5.0, "CaCl2": 3.0})
        water_volume_gal: Volume of water in gallons

    Returns:
        Dictionary with resulting ion concentrations
    """
    volume = _coerce_positive(water_volume_gal, "water_volume_gal")

    # Validate required keys
    required_ions = ["calcium", "magnesium", "sodium", "chloride", "sulfate", "bicarbonate"]
    for ion in required_ions:
        if ion not in water_profile:
            raise ValueError(f"water_profile must contain '{ion}' key")

    # Start with source water chemistry
    resulting_profile = {ion: float(water_profile[ion]) for ion in required_ions}

    # Add contributions from each salt
    for salt_type, amount in salt_additions.items():
        if amount > 0:
            contributions = calculate_salt_ion_contribution(salt_type, amount, volume)
            for ion in required_ions:
                resulting_profile[ion] += contributions[ion]

    # Round to 1 decimal place
    for ion in resulting_profile:
        resulting_profile[ion] = round(resulting_profile[ion], 1)

    return resulting_profile
