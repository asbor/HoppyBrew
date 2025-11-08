"""
API endpoints for brewing calculators.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

from modules.brewing_calculations import (
    calculate_abv,
    calculate_ibu_tinseth,
    calculate_srm_morey,
    calculate_strike_water,
    calculate_priming_sugar,
    calculate_yeast_starter,
    calculate_dilution,
    calculate_carbonation,
    calculate_water_chemistry,
)

router = APIRouter()


# Request/Response Models


class ABVRequest(BaseModel):
    original_gravity: float = Field(
        ..., gt=0, description="Original gravity (e.g., 1.050)"
    )
    final_gravity: float = Field(..., gt=0, description="Final gravity (e.g., 1.010)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"original_gravity": 1.050, "final_gravity": 1.010}
        }
    )


class ABVResponse(BaseModel):
    abv: float = Field(..., description="Alcohol by volume percentage")

    model_config = ConfigDict(json_schema_extra={"example": {"abv": 5.25}})


class IBURequest(BaseModel):
    alpha_acid: float = Field(
        ..., ge=0, description="Alpha acid percentage (e.g., 12.0)"
    )
    weight_oz: float = Field(..., ge=0, description="Hop weight in ounces")
    boil_time_min: float = Field(..., ge=0, description="Boil time in minutes")
    batch_size_gal: float = Field(..., gt=0, description="Batch size in gallons")
    gravity: float = Field(..., gt=0, description="Wort gravity during boil")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "alpha_acid": 12.0,
                "weight_oz": 2.0,
                "boil_time_min": 60.0,
                "batch_size_gal": 5.0,
                "gravity": 1.050,
            }
        }
    )


class IBUResponse(BaseModel):
    ibu: float = Field(..., description="International Bitterness Units")

    model_config = ConfigDict(json_schema_extra={"example": {"ibu": 35.2}})


class SRMRequest(BaseModel):
    grain_color: float = Field(..., ge=0, description="Grain color in Lovibond")
    grain_weight_lbs: float = Field(..., ge=0, description="Grain weight in pounds")
    batch_size_gal: float = Field(..., gt=0, description="Batch size in gallons")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "grain_color": 3.0,
                "grain_weight_lbs": 10.0,
                "batch_size_gal": 5.0,
            }
        }
    )


class SRMResponse(BaseModel):
    srm: float = Field(..., description="Standard Reference Method color")

    model_config = ConfigDict(json_schema_extra={"example": {"srm": 4.5}})


class StrikeWaterRequest(BaseModel):
    grain_weight_lbs: float = Field(..., gt=0, description="Grain weight in pounds")
    mash_temp_f: float = Field(
        ..., gt=0, description="Target mash temperature in Fahrenheit"
    )
    grain_temp_f: float = Field(
        ..., ge=0, description="Current grain temperature in Fahrenheit"
    )
    water_to_grain_ratio: float = Field(
        1.25, gt=0, description="Water to grain ratio in quarts per pound"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "grain_weight_lbs": 11.0,
                "mash_temp_f": 152.0,
                "grain_temp_f": 68.0,
                "water_to_grain_ratio": 1.25,
            }
        }
    )


class StrikeWaterResponse(BaseModel):
    volume_quarts: float = Field(..., description="Strike water volume in quarts")
    temperature_f: float = Field(
        ..., description="Strike water temperature in Fahrenheit"
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"volume_quarts": 13.75, "temperature_f": 164.2}}
    )


class PrimingSugarRequest(BaseModel):
    volume_gal: float = Field(..., gt=0, description="Beer volume in gallons")
    carbonation_level: float = Field(
        ..., gt=0, description="Target CO2 volumes (typically 2.0-2.8)"
    )
    sugar_type: str = Field(
        "table", description="Sugar type: table, corn, dme, or honey"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "volume_gal": 5.0,
                "carbonation_level": 2.4,
                "sugar_type": "table",
            }
        }
    )


class PrimingSugarResponse(BaseModel):
    grams: float = Field(..., description="Priming sugar needed in grams")
    oz: float = Field(..., description="Priming sugar needed in ounces")

    model_config = ConfigDict(
        json_schema_extra={"example": {"grams": 106.2, "oz": 3.75}}
    )


class YeastStarterRequest(BaseModel):
    og: float = Field(..., gt=0, description="Target original gravity")
    volume_gal: float = Field(..., gt=0, description="Batch volume in gallons")
    yeast_age_months: float = Field(
        ..., ge=0, description="Yeast age in months (0 = fresh)"
    )
    target_cell_count: Optional[float] = Field(
        None, description="Target cell count in billions (optional)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "og": 1.050,
                "volume_gal": 5.0,
                "yeast_age_months": 2.0,
            }
        }
    )


class YeastStarterResponse(BaseModel):
    cells_needed_billions: float = Field(..., description="Cells needed in billions")
    packages: int = Field(..., description="Number of yeast packages needed")
    starter_size_ml: int = Field(..., description="Recommended starter size in mL")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cells_needed_billions": 188.7,
                "packages": 3,
                "starter_size_ml": 1000,
            }
        }
    )


class DilutionRequest(BaseModel):
    current_og: float = Field(..., gt=0, description="Current original gravity")
    current_volume_gal: float = Field(
        ..., gt=0, description="Current volume in gallons"
    )
    target_og: float = Field(..., gt=0, description="Target original gravity")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_og": 1.060,
                "current_volume_gal": 5.0,
                "target_og": 1.050,
            }
        }
    )


class DilutionResponse(BaseModel):
    water_to_add_gal: float = Field(..., description="Water to add in gallons")
    final_volume_gal: float = Field(..., description="Final volume in gallons")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"water_to_add_gal": 1.0, "final_volume_gal": 6.0}
        }
    )


class CarbonationRequest(BaseModel):
    temp_f: float = Field(..., ge=0, description="Beer temperature in Fahrenheit")
    co2_volumes: float = Field(..., gt=0, description="Desired CO2 volumes")

    model_config = ConfigDict(
        json_schema_extra={"example": {"temp_f": 38.0, "co2_volumes": 2.5}}
    )


class CarbonationResponse(BaseModel):
    psi: float = Field(..., description="Pressure in PSI")
    bar: float = Field(..., description="Pressure in bar")

    model_config = ConfigDict(json_schema_extra={"example": {"psi": 12.5, "bar": 0.86}})


class WaterChemistryRequest(BaseModel):
    water_profile: dict = Field(
        ...,
        description=(
            "Water profile with ion concentrations "
            "(calcium, magnesium, sodium, chloride, sulfate, bicarbonate in ppm)"
        ),
    )
    grain_bill_lbs: float = Field(..., gt=0, description="Total grain weight in pounds")
    target_ph: float = Field(5.4, gt=0, description="Target mash pH")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "water_profile": {
                    "calcium": 50,
                    "magnesium": 10,
                    "sodium": 15,
                    "chloride": 60,
                    "sulfate": 120,
                    "bicarbonate": 80,
                },
                "grain_bill_lbs": 11.0,
                "target_ph": 5.4,
            }
        }
    )


class WaterChemistryResponse(BaseModel):
    residual_alkalinity: float = Field(..., description="Residual alkalinity")
    estimated_ph: float = Field(..., description="Estimated mash pH")
    ph_target: float = Field(..., description="Target pH")
    ph_difference: float = Field(..., description="Difference from target")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "residual_alkalinity": 23.5,
                "estimated_ph": 5.47,
                "ph_target": 5.4,
                "ph_difference": 0.07,
            }
        }
    )


# Endpoints


@router.post(
    "/calculators/abv",
    response_model=ABVResponse,
    summary="Calculate ABV",
    response_description="Alcohol by volume from gravity readings",
)
async def calc_abv(request: ABVRequest) -> ABVResponse:
    """Calculate Alcohol by Volume (ABV) from original and final gravity readings."""
    abv = calculate_abv(request.original_gravity, request.final_gravity)
    return ABVResponse(abv=abv)


@router.post(
    "/calculators/ibu",
    response_model=IBUResponse,
    summary="Calculate IBU",
    response_description="International Bitterness Units using Tinseth formula",
)
async def calc_ibu(request: IBURequest) -> IBUResponse:
    """Calculate International Bitterness Units (IBU) using the Tinseth model."""
    ibu = calculate_ibu_tinseth(
        request.alpha_acid,
        request.weight_oz,
        request.boil_time_min,
        request.batch_size_gal,
        request.gravity,
    )
    return IBUResponse(ibu=ibu)


@router.post(
    "/calculators/srm",
    response_model=SRMResponse,
    summary="Calculate SRM",
    response_description="Standard Reference Method color using Morey equation",
)
async def calc_srm(request: SRMRequest) -> SRMResponse:
    """Calculate beer color using the Morey equation."""
    srm = calculate_srm_morey(
        request.grain_color,
        request.grain_weight_lbs,
        request.batch_size_gal,
    )
    return SRMResponse(srm=srm)


@router.post(
    "/calculators/strike-water",
    response_model=StrikeWaterResponse,
    summary="Calculate strike water",
    response_description="Strike water temperature and volume for mashing",
)
async def calc_strike_water(request: StrikeWaterRequest) -> StrikeWaterResponse:
    """Calculate strike water temperature and volume for mashing."""
    result = calculate_strike_water(
        request.grain_weight_lbs,
        request.mash_temp_f,
        request.grain_temp_f,
        request.water_to_grain_ratio,
    )
    return StrikeWaterResponse(**result)


@router.post(
    "/calculators/priming-sugar",
    response_model=PrimingSugarResponse,
    summary="Calculate priming sugar",
    response_description="Priming sugar needed for bottle carbonation",
)
async def calc_priming_sugar(request: PrimingSugarRequest) -> PrimingSugarResponse:
    """Calculate priming sugar needed for bottle carbonation."""
    result = calculate_priming_sugar(
        request.volume_gal,
        request.carbonation_level,
        request.sugar_type,
    )
    return PrimingSugarResponse(**result)


@router.post(
    "/calculators/yeast-starter",
    response_model=YeastStarterResponse,
    summary="Calculate yeast starter",
    response_description="Yeast starter requirements",
)
async def calc_yeast_starter(request: YeastStarterRequest) -> YeastStarterResponse:
    """Calculate yeast starter requirements."""
    result = calculate_yeast_starter(
        request.og,
        request.volume_gal,
        request.yeast_age_months,
        request.target_cell_count,
    )
    return YeastStarterResponse(**result)


@router.post(
    "/calculators/dilution",
    response_model=DilutionResponse,
    summary="Calculate dilution",
    response_description="Water needed to dilute wort to target gravity",
)
async def calc_dilution(request: DilutionRequest) -> DilutionResponse:
    """Calculate water needed to dilute wort to target gravity."""
    result = calculate_dilution(
        request.current_og,
        request.current_volume_gal,
        request.target_og,
    )
    return DilutionResponse(**result)


@router.post(
    "/calculators/carbonation",
    response_model=CarbonationResponse,
    summary="Calculate carbonation pressure",
    response_description="Carbonation pressure for given temperature and CO2 volumes",
)
async def calc_carbonation(request: CarbonationRequest) -> CarbonationResponse:
    """Calculate carbonation pressure for a given temperature and CO2 volume."""
    result = calculate_carbonation(
        request.temp_f,
        request.co2_volumes,
    )
    return CarbonationResponse(**result)


@router.post(
    "/calculators/water-chemistry",
    response_model=WaterChemistryResponse,
    summary="Calculate water chemistry",
    response_description="Water adjustments for target mash pH",
)
async def calc_water_chemistry(
    request: WaterChemistryRequest,
) -> WaterChemistryResponse:
    """Estimate water adjustments for target mash pH."""
    result = calculate_water_chemistry(
        request.water_profile,
        request.grain_bill_lbs,
        request.target_ph,
    )
    return WaterChemistryResponse(**result)


# Hop Schedule Optimizer Models


class HopAddition(BaseModel):
    name: str = Field(..., description="Hop variety name")
    alpha_acid: float = Field(..., ge=0, description="Alpha acid percentage")
    amount_oz: float = Field(..., ge=0, description="Hop amount in ounces")
    time_min: float = Field(..., ge=0, description="Boil time in minutes")
    type: Optional[str] = Field(None, description="Hop type (Bittering, Aroma, etc.)")
    form: Optional[str] = Field(None, description="Hop form (Pellet, Whole, etc.)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Cascade",
                "alpha_acid": 5.5,
                "amount_oz": 1.0,
                "time_min": 60.0,
                "type": "Aroma",
                "form": "Pellet",
            }
        }
    )


class HopScheduleRequest(BaseModel):
    hops: List[HopAddition] = Field(..., description="List of hop additions")
    batch_size_gal: float = Field(..., gt=0, description="Batch size in gallons")
    boil_gravity: float = Field(..., gt=0, description="Boil gravity (e.g., 1.050)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "hops": [
                    {
                        "name": "Magnum",
                        "alpha_acid": 12.0,
                        "amount_oz": 1.0,
                        "time_min": 60.0,
                        "type": "Bittering",
                        "form": "Pellet",
                    },
                    {
                        "name": "Cascade",
                        "alpha_acid": 5.5,
                        "amount_oz": 1.0,
                        "time_min": 15.0,
                        "type": "Aroma",
                        "form": "Pellet",
                    },
                ],
                "batch_size_gal": 5.0,
                "boil_gravity": 1.050,
            }
        }
    )


class HopContribution(BaseModel):
    name: str = Field(..., description="Hop variety name")
    time_min: float = Field(..., description="Boil time in minutes")
    amount_oz: float = Field(..., description="Amount in ounces")
    ibu: float = Field(..., description="IBU contribution")
    utilization: float = Field(..., description="Hop utilization percentage")
    type: Optional[str] = Field(None, description="Hop type")
    form: Optional[str] = Field(None, description="Hop form")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Cascade",
                "time_min": 60.0,
                "amount_oz": 1.0,
                "ibu": 27.5,
                "utilization": 28.5,
                "type": "Aroma",
                "form": "Pellet",
            }
        }
    )


class HopScheduleResponse(BaseModel):
    total_ibu: float = Field(..., description="Total IBU from all additions")
    hop_contributions: List[HopContribution] = Field(
        ..., description="Individual hop contributions"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_ibu": 45.3,
                "hop_contributions": [
                    {
                        "name": "Magnum",
                        "time_min": 60.0,
                        "amount_oz": 1.0,
                        "ibu": 37.8,
                        "utilization": 30.1,
                        "type": "Bittering",
                        "form": "Pellet",
                    },
                    {
                        "name": "Cascade",
                        "time_min": 15.0,
                        "amount_oz": 1.0,
                        "ibu": 7.5,
                        "utilization": 10.5,
                        "type": "Aroma",
                        "form": "Pellet",
                    },
                ],
            }
        }
    )


class HopSubstitution(BaseModel):
    name: str = Field(..., description="Substitute hop variety name")
    alpha_acid_range: str = Field(
        ..., description="Typical alpha acid range (e.g., '4-6%')"
    )
    similarity_score: float = Field(
        ..., ge=0, le=100, description="Similarity score (0-100)"
    )
    characteristics: str = Field(..., description="Flavor and aroma characteristics")
    origin: Optional[str] = Field(None, description="Primary origin")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Centennial",
                "alpha_acid_range": "9-12%",
                "similarity_score": 85.0,
                "characteristics": "Citrus, floral, pine notes",
                "origin": "USA",
            }
        }
    )


class HopSubstitutionRequest(BaseModel):
    hop_name: str = Field(..., description="Hop variety to find substitutes for")
    alpha_acid: Optional[float] = Field(
        None, description="Alpha acid percentage (optional)"
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"hop_name": "Cascade", "alpha_acid": 5.5}}
    )


class HopSubstitutionResponse(BaseModel):
    original_hop: str = Field(..., description="Original hop variety")
    substitutes: List[HopSubstitution] = Field(
        ..., description="List of substitute hops"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "original_hop": "Cascade",
                "substitutes": [
                    {
                        "name": "Centennial",
                        "alpha_acid_range": "9-12%",
                        "similarity_score": 85.0,
                        "characteristics": "Citrus, floral, pine notes",
                        "origin": "USA",
                    },
                    {
                        "name": "Amarillo",
                        "alpha_acid_range": "8-11%",
                        "similarity_score": 78.0,
                        "characteristics": "Orange, grapefruit, floral",
                        "origin": "USA",
                    },
                ],
            }
        }
    )


# Hop Schedule Optimizer Endpoints


@router.post(
    "/calculators/hop-schedule",
    response_model=HopScheduleResponse,
    summary="Calculate hop schedule",
    response_description="IBU contributions and utilization for hop schedule",
)
async def calculate_hop_schedule(request: HopScheduleRequest) -> HopScheduleResponse:
    """
    Calculate IBU contributions and utilization for each hop addition in a schedule.
    
    This endpoint provides detailed analysis of hop additions including:
    - Individual IBU contribution per hop
    - Hop utilization percentage
    - Total IBU for the recipe
    """
    contributions = []
    total_ibu = 0.0

    for hop in request.hops:
        # Calculate IBU for this addition
        ibu = calculate_ibu_tinseth(
            hop.alpha_acid,
            hop.amount_oz,
            hop.time_min,
            request.batch_size_gal,
            request.boil_gravity,
        )

        # Calculate utilization percentage
        gravity_factor = 1.65 * (0.000125 ** (request.boil_gravity - 1.0))
        time_factor = (1 - (2.71828 ** (-0.04 * hop.time_min))) / 4.15
        utilization = (gravity_factor * time_factor) * 100

        contributions.append(
            HopContribution(
                name=hop.name,
                time_min=hop.time_min,
                amount_oz=hop.amount_oz,
                ibu=round(ibu, 1),
                utilization=round(utilization, 1),
                type=hop.type,
                form=hop.form,
            )
        )
        total_ibu += ibu

    return HopScheduleResponse(
        total_ibu=round(total_ibu, 1), hop_contributions=contributions
    )


@router.post(
    "/calculators/hop-substitutions",
    response_model=HopSubstitutionResponse,
    summary="Get hop substitutions",
    response_description="List of substitute hops with similarity scores",
)
async def get_hop_substitutions(
    request: HopSubstitutionRequest,
) -> HopSubstitutionResponse:
    """
    Suggest hop substitutions based on hop characteristics.
    
    Returns a list of alternative hops that can substitute for the requested variety,
    with similarity scores and detailed characteristics.
    """
    # Hop substitution database with characteristics
    hop_database = {
        "Cascade": {
            "alpha_range": "4.5-7%",
            "characteristics": "Citrus, grapefruit, floral",
            "origin": "USA",
            "substitutes": {
                "Centennial": 85,
                "Amarillo": 78,
                "Citra": 72,
                "Columbus": 65,
            },
        },
        "Centennial": {
            "alpha_range": "9-12%",
            "characteristics": "Citrus, floral, pine",
            "origin": "USA",
            "substitutes": {"Cascade": 85, "Columbus": 80, "Chinook": 75, "Citra": 70},
        },
        "Citra": {
            "alpha_range": "11-13%",
            "characteristics": "Tropical fruit, citrus, passion fruit",
            "origin": "USA",
            "substitutes": {
                "Mosaic": 88,
                "Amarillo": 75,
                "Simcoe": 72,
                "Cascade": 68,
            },
        },
        "Mosaic": {
            "alpha_range": "11.5-13.5%",
            "characteristics": "Tropical fruit, berry, floral",
            "origin": "USA",
            "substitutes": {"Citra": 88, "Simcoe": 80, "Amarillo": 75, "Galaxy": 70},
        },
        "Simcoe": {
            "alpha_range": "12-14%",
            "characteristics": "Pine, citrus, earthy",
            "origin": "USA",
            "substitutes": {
                "Columbus": 82,
                "Amarillo": 78,
                "Mosaic": 75,
                "Chinook": 72,
            },
        },
        "Amarillo": {
            "alpha_range": "8-11%",
            "characteristics": "Orange, grapefruit, floral",
            "origin": "USA",
            "substitutes": {"Cascade": 80, "Citra": 78, "Centennial": 75, "Simcoe": 70},
        },
        "Columbus": {
            "alpha_range": "14-18%",
            "characteristics": "Pungent, earthy, spicy",
            "origin": "USA",
            "substitutes": {
                "Chinook": 85,
                "Magnum": 80,
                "Simcoe": 78,
                "Centennial": 72,
            },
        },
        "Chinook": {
            "alpha_range": "12-14%",
            "characteristics": "Pine, spicy, grapefruit",
            "origin": "USA",
            "substitutes": {
                "Columbus": 85,
                "Nugget": 80,
                "Centennial": 75,
                "Simcoe": 70,
            },
        },
        "Magnum": {
            "alpha_range": "12-17%",
            "characteristics": "Clean bittering, mild aroma",
            "origin": "Germany/USA",
            "substitutes": {
                "Columbus": 82,
                "Warrior": 80,
                "Nugget": 78,
                "Chinook": 75,
            },
        },
        "Saaz": {
            "alpha_range": "3-4.5%",
            "characteristics": "Earthy, herbal, spicy",
            "origin": "Czech Republic",
            "substitutes": {
                "Sterling": 85,
                "Liberty": 82,
                "Tettnanger": 78,
                "Hallertau": 75,
            },
        },
        "Hallertau": {
            "alpha_range": "3.5-5.5%",
            "characteristics": "Mild, pleasant, slightly spicy",
            "origin": "Germany",
            "substitutes": {
                "Tettnanger": 88,
                "Liberty": 85,
                "Crystal": 80,
                "Saaz": 75,
            },
        },
        "Tettnanger": {
            "alpha_range": "3.5-5.5%",
            "characteristics": "Floral, herbal, spicy",
            "origin": "Germany",
            "substitutes": {
                "Hallertau": 88,
                "Saaz": 82,
                "Liberty": 80,
                "Sterling": 78,
            },
        },
        "Galaxy": {
            "alpha_range": "13-15%",
            "characteristics": "Passion fruit, peach, citrus",
            "origin": "Australia",
            "substitutes": {"Citra": 75, "Mosaic": 72, "El Dorado": 70, "Azacca": 68},
        },
        "Nelson Sauvin": {
            "alpha_range": "12-14%",
            "characteristics": "White wine, gooseberry, grape",
            "origin": "New Zealand",
            "substitutes": {
                "Motueka": 78,
                "Galaxy": 72,
                "Citra": 68,
                "Amarillo": 65,
            },
        },
        "Fuggle": {
            "alpha_range": "4-5.5%",
            "characteristics": "Earthy, woody, mild",
            "origin": "UK",
            "substitutes": {
                "Willamette": 88,
                "Styrian Golding": 85,
                "East Kent Golding": 82,
            },
        },
        "East Kent Golding": {
            "alpha_range": "4.5-6.5%",
            "characteristics": "Earthy, floral, honey",
            "origin": "UK",
            "substitutes": {
                "Fuggle": 85,
                "Willamette": 82,
                "Styrian Golding": 80,
                "Progress": 75,
            },
        },
    }

    hop_name_normalized = request.hop_name.strip()

    # Try to find exact match (case-insensitive)
    hop_info = None
    for key, value in hop_database.items():
        if key.lower() == hop_name_normalized.lower():
            hop_info = value
            hop_name_normalized = key
            break

    if not hop_info:
        # Return empty substitutes if hop not found
        return HopSubstitutionResponse(
            original_hop=request.hop_name, substitutes=[]
        )

    # Build substitution list
    substitutes = []
    for sub_name, similarity in hop_info["substitutes"].items():
        if sub_name in hop_database:
            sub_info = hop_database[sub_name]
            substitutes.append(
                HopSubstitution(
                    name=sub_name,
                    alpha_acid_range=sub_info["alpha_range"],
                    similarity_score=float(similarity),
                    characteristics=sub_info["characteristics"],
                    origin=sub_info["origin"],
                )
            )

    # Sort by similarity score (descending)
    substitutes.sort(key=lambda x: x.similarity_score, reverse=True)

    return HopSubstitutionResponse(
        original_hop=hop_name_normalized, substitutes=substitutes
    )
