"""
Yeast viability calculator.

Calculates yeast viability based on various factors including:
- Yeast form (dry, liquid, slant)
- Age since manufacture
- Storage temperature
- Generation number
"""
from datetime import datetime
from typing import Optional
import math


class YeastViabilityCalculator:
    """
    Calculate yeast viability based on age, storage conditions, and form.
    
    Based on common brewing practices:
    - Dry yeast: ~3 years shelf life, very stable
    - Liquid yeast: ~6 months shelf life, degrades faster
    - Slants/cultures: ~2 years shelf life with proper storage
    - Each generation loses ~10-15% viability
    """
    
    # Viability decay rates per month (percentage points lost per month)
    DECAY_RATE_DRY = 0.5  # Very slow decay for dry yeast
    DECAY_RATE_LIQUID = 3.0  # Faster decay for liquid yeast
    DECAY_RATE_SLANT = 1.0  # Moderate decay for slants
    DECAY_RATE_CULTURE = 1.5  # Slightly faster for cultures
    
    # Temperature adjustment factor (multiplier per degree above 4°C)
    TEMP_MULTIPLIER = 0.15
    
    # Generation viability loss
    GENERATION_LOSS_PERCENT = 12.0  # Loss per generation
    
    @classmethod
    def calculate_viability(
        cls,
        yeast_form: str,
        manufacture_date: Optional[datetime] = None,
        expiry_date: Optional[datetime] = None,
        current_date: Optional[datetime] = None,
        initial_viability: float = 100.0,
        storage_temperature: Optional[float] = None,
        generation: int = 0
    ) -> dict:
        """
        Calculate current yeast viability.
        
        Args:
            yeast_form: Form of yeast (Dry, Liquid, Slant, Culture)
            manufacture_date: Date of manufacture/packaging
            expiry_date: Expiry date
            current_date: Date to calculate viability for (default: today)
            initial_viability: Initial viability percentage (default: 100)
            storage_temperature: Storage temperature in Celsius (default: 4°C)
            generation: Generation number (0 for commercial, >0 for harvested)
            
        Returns:
            Dictionary with viability calculation results
        """
        if current_date is None:
            current_date = datetime.now()
            
        if storage_temperature is None:
            storage_temperature = 4.0  # Assume refrigeration
            
        # Calculate age-based viability
        viability = initial_viability
        days_since_manufacture = None
        days_until_expiry = None
        
        if manufacture_date:
            days_since_manufacture = (current_date - manufacture_date).days
            months_old = days_since_manufacture / 30.0
            
            # Get base decay rate for yeast form
            decay_rate = cls._get_decay_rate(yeast_form)
            
            # Adjust for storage temperature
            temp_adjustment = cls._calculate_temp_adjustment(storage_temperature)
            adjusted_decay_rate = decay_rate * temp_adjustment
            
            # Calculate viability loss from age
            viability_loss = months_old * adjusted_decay_rate
            viability -= viability_loss
            
        if expiry_date:
            days_until_expiry = (expiry_date - current_date).days
            
        # Apply generation loss
        if generation > 0:
            generation_loss = generation * cls.GENERATION_LOSS_PERCENT
            viability -= generation_loss
            
        # Ensure viability stays within bounds
        viability = max(0.0, min(100.0, viability))
        
        # Calculate cell loss
        cell_loss_percent = initial_viability - viability
        
        # Determine status and recommendation
        status = cls._determine_status(viability)
        recommendation = cls._get_recommendation(viability, generation)
        
        return {
            "current_viability": round(viability, 1),
            "days_since_manufacture": days_since_manufacture,
            "days_until_expiry": days_until_expiry,
            "viability_status": status,
            "recommendation": recommendation,
            "estimated_cell_loss_percent": round(cell_loss_percent, 1)
        }
    
    @classmethod
    def _get_decay_rate(cls, yeast_form: str) -> float:
        """Get base decay rate for yeast form"""
        form_upper = yeast_form.upper()
        
        if "DRY" in form_upper:
            return cls.DECAY_RATE_DRY
        elif "LIQUID" in form_upper:
            return cls.DECAY_RATE_LIQUID
        elif "SLANT" in form_upper:
            return cls.DECAY_RATE_SLANT
        elif "CULTURE" in form_upper:
            return cls.DECAY_RATE_CULTURE
        else:
            return cls.DECAY_RATE_LIQUID  # Default to liquid
    
    @classmethod
    def _calculate_temp_adjustment(cls, temp_celsius: float) -> float:
        """
        Calculate temperature adjustment multiplier.
        
        Ideal storage is 4°C. Higher temperatures increase decay rate.
        """
        if temp_celsius <= 4.0:
            return 1.0
        
        # Each degree above 4°C increases decay by TEMP_MULTIPLIER
        temp_diff = temp_celsius - 4.0
        multiplier = 1.0 + (temp_diff * cls.TEMP_MULTIPLIER)
        return multiplier
    
    @classmethod
    def _determine_status(cls, viability: float) -> str:
        """Determine viability status category"""
        if viability >= 95:
            return "excellent"
        elif viability >= 85:
            return "good"
        elif viability >= 70:
            return "fair"
        elif viability >= 50:
            return "poor"
        else:
            return "expired"
    
    @classmethod
    def _get_recommendation(cls, viability: float, generation: int) -> str:
        """Get usage recommendation based on viability"""
        if viability >= 95:
            return "Excellent for direct pitching"
        elif viability >= 85:
            return "Good for direct pitching, starter recommended for high gravity"
        elif viability >= 70:
            return "Starter strongly recommended"
        elif viability >= 50:
            return "Large starter required, consider using fresh yeast"
        else:
            return "Not recommended for use, viability too low"
            
        if generation >= 10:
            return "Maximum generations exceeded, use fresh yeast"
        elif generation >= 5:
            return "High generation count, monitor performance closely"
            
        return recommendation
    
    @classmethod
    def calculate_starter_size(cls, viability: float, target_cells: float) -> dict:
        """
        Calculate required starter size to reach target cell count.
        
        Args:
            viability: Current yeast viability percentage
            target_cells: Target cell count in billions
            
        Returns:
            Dictionary with starter recommendations
        """
        if viability <= 0:
            return {
                "starter_recommended": True,
                "starter_size_liters": None,
                "message": "Viability too low, use fresh yeast"
            }
        
        # Adjust target based on viability
        viability_factor = viability / 100.0
        
        if viability >= 85:
            return {
                "starter_recommended": False,
                "starter_size_liters": 0,
                "message": "No starter needed for most batches"
            }
        
        # Simplified starter calculation
        # This is a rough estimate; proper calculation would consider growth rates
        cells_needed = target_cells / viability_factor
        additional_cells = cells_needed - (target_cells * viability_factor)
        
        # Assume ~1.5 liters starter produces ~100B cells
        starter_size = (additional_cells / 100.0) * 1.5
        starter_size = max(0.5, min(5.0, starter_size))  # Between 0.5-5L
        
        return {
            "starter_recommended": True,
            "starter_size_liters": round(starter_size, 1),
            "message": f"Make a {round(starter_size, 1)}L starter to restore cell count"
        }
