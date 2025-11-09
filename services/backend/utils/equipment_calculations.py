"""
Equipment profile calculation utilities.

This module provides helper functions for calculating volumes and losses
related to brewing equipment profiles.
"""


def calculate_pre_boil_volume(
    batch_size: float,
    boil_time: int,
    evap_rate: float,
    trub_chiller_loss: float = 0,
    top_up_kettle: float = 0,
) -> float:
    """
    Calculate the pre-boil volume needed for a given batch size.
    
    Args:
        batch_size: Target batch size in liters
        boil_time: Boil time in minutes
        evap_rate: Evaporation rate in liters per hour
        trub_chiller_loss: Volume lost to trub and chiller in liters
        top_up_kettle: Volume of top-up water added to kettle in liters
    
    Returns:
        Pre-boil volume in liters
    """
    if not batch_size or not boil_time or not evap_rate:
        return 0.0
    
    # Calculate evaporation loss during boil
    evap_loss = (evap_rate * boil_time) / 60.0
    
    # Pre-boil volume = batch size + evaporation loss + trub/chiller loss - top-up kettle
    pre_boil_volume = batch_size + evap_loss + (trub_chiller_loss or 0) - (top_up_kettle or 0)
    
    return round(pre_boil_volume, 2)


def calculate_strike_water_volume(
    grain_weight: float,
    mash_thickness: float = 3.0,
    grain_absorption_rate: float = 1.0,
) -> float:
    """
    Calculate the strike water volume needed for mashing.
    
    Args:
        grain_weight: Total weight of grain in kg
        mash_thickness: Ratio of water to grain (liters per kg), default 3.0
        grain_absorption_rate: Volume absorbed by grain (liters per kg), default 1.0
    
    Returns:
        Strike water volume in liters
    """
    if not grain_weight:
        return 0.0
    
    strike_water = grain_weight * mash_thickness
    
    return round(strike_water, 2)


def calculate_total_water_needed(
    batch_size: float,
    boil_time: int,
    evap_rate: float,
    grain_weight: float = 0,
    grain_absorption_rate: float = 1.0,
    trub_chiller_loss: float = 0,
    lauter_deadspace: float = 0,
    mash_thickness: float = 3.0,
) -> dict:
    """
    Calculate total water needed for a brew session.
    
    Args:
        batch_size: Target batch size in liters
        boil_time: Boil time in minutes
        evap_rate: Evaporation rate in liters per hour
        grain_weight: Total weight of grain in kg
        grain_absorption_rate: Volume absorbed by grain (liters per kg), default 1.0
        trub_chiller_loss: Volume lost to trub and chiller in liters
        lauter_deadspace: Volume lost in lauter tun in liters
        mash_thickness: Ratio of water to grain (liters per kg), default 3.0
    
    Returns:
        Dictionary with strike water, sparge water, and total water volumes
    """
    if not batch_size or not boil_time or not evap_rate:
        return {"strike_water": 0.0, "sparge_water": 0.0, "total_water": 0.0}
    
    # Calculate pre-boil volume needed
    pre_boil = calculate_pre_boil_volume(
        batch_size, boil_time, evap_rate, trub_chiller_loss
    )
    
    # Calculate strike water
    strike_water = calculate_strike_water_volume(grain_weight, mash_thickness)
    
    # Calculate volume absorbed by grain
    grain_absorption = grain_weight * grain_absorption_rate if grain_weight else 0
    
    # Calculate sparge water needed
    # sparge = pre-boil volume - (strike water - grain absorption - deadspace)
    sparge_water = pre_boil - (strike_water - grain_absorption - (lauter_deadspace or 0))
    sparge_water = max(0, sparge_water)  # Cannot be negative
    
    total_water = strike_water + sparge_water
    
    return {
        "strike_water": round(strike_water, 2),
        "sparge_water": round(sparge_water, 2),
        "total_water": round(total_water, 2),
        "pre_boil_volume": round(pre_boil, 2),
        "grain_absorption": round(grain_absorption, 2),
    }


def calculate_efficiency(
    actual_og: float,
    target_og: float,
) -> float:
    """
    Calculate brewing efficiency based on actual vs target original gravity.
    
    Args:
        actual_og: Actual original gravity measured (e.g., 1.050)
        target_og: Target original gravity (e.g., 1.050)
    
    Returns:
        Efficiency as a percentage
    """
    if not actual_og or not target_og or target_og == 1.0:
        return 0.0
    
    # Calculate efficiency as (actual - 1) / (target - 1) * 100
    efficiency = ((actual_og - 1.0) / (target_og - 1.0)) * 100
    
    return round(efficiency, 2)


def calculate_volume_loss(
    trub_chiller_loss: float = 0,
    lauter_deadspace: float = 0,
    boil_time: int = 60,
    evap_rate: float = 0,
) -> dict:
    """
    Calculate total volume losses during brewing.
    
    Args:
        trub_chiller_loss: Volume lost to trub and chiller in liters
        lauter_deadspace: Volume lost in lauter tun in liters
        boil_time: Boil time in minutes
        evap_rate: Evaporation rate in liters per hour
    
    Returns:
        Dictionary with individual losses and total loss
    """
    evap_loss = (evap_rate * boil_time) / 60.0 if evap_rate and boil_time else 0
    
    total_loss = (trub_chiller_loss or 0) + (lauter_deadspace or 0) + evap_loss
    
    return {
        "trub_chiller_loss": round(trub_chiller_loss or 0, 2),
        "lauter_deadspace": round(lauter_deadspace or 0, 2),
        "evaporation_loss": round(evap_loss, 2),
        "total_loss": round(total_loss, 2),
    }
