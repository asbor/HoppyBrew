"""
API endpoints for brewing calculators.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

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
    calculate_salt_ion_contribution,
    calculate_mineral_additions,
    calculate_water_adjustment,
    calculate_mash_ph,
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


# New mineral adjustment calculator models and endpoints


class SaltIonContributionRequest(BaseModel):
    salt_type: str = Field(
        ...,
        description="Type of brewing salt (CaCl2, CaSO4, MgSO4, NaCl, NaHCO3, CaCO3)",
    )
    amount_grams: float = Field(..., ge=0, description="Amount of salt in grams")
    water_volume_gal: float = Field(..., gt=0, description="Water volume in gallons")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "salt_type": "CaSO4",
                "amount_grams": 5.0,
                "water_volume_gal": 5.0,
            }
        }
    )


class SaltIonContributionResponse(BaseModel):
    calcium: float = Field(..., description="Calcium contribution in ppm")
    magnesium: float = Field(..., description="Magnesium contribution in ppm")
    sodium: float = Field(..., description="Sodium contribution in ppm")
    chloride: float = Field(..., description="Chloride contribution in ppm")
    sulfate: float = Field(..., description="Sulfate contribution in ppm")
    bicarbonate: float = Field(..., description="Bicarbonate contribution in ppm")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "calcium": 54.0,
                "magnesium": 0.0,
                "sodium": 0.0,
                "chloride": 0.0,
                "sulfate": 129.3,
                "bicarbonate": 0.0,
            }
        }
    )


class MineralAdditionsRequest(BaseModel):
    source_profile: dict = Field(
        ...,
        description="Source water profile with ion concentrations in ppm",
    )
    target_profile: dict = Field(
        ...,
        description="Target water profile with ion concentrations in ppm",
    )
    water_volume_gal: float = Field(..., gt=0, description="Water volume in gallons")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "source_profile": {
                    "calcium": 10,
                    "magnesium": 2,
                    "sodium": 5,
                    "chloride": 8,
                    "sulfate": 5,
                    "bicarbonate": 20,
                },
                "target_profile": {
                    "calcium": 100,
                    "magnesium": 10,
                    "sodium": 15,
                    "chloride": 60,
                    "sulfate": 150,
                    "bicarbonate": 40,
                },
                "water_volume_gal": 5.0,
            }
        }
    )


class MineralAdditionsResponse(BaseModel):
    additions: dict = Field(..., description="Recommended salt additions in grams")
    resulting_profile: dict = Field(
        ..., description="Resulting water profile after additions"
    )
    target_profile: dict = Field(..., description="Target water profile")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "additions": {
                    "CaSO4": 15.2,
                    "CaCl2": 8.5,
                    "MgSO4": 3.1,
                    "NaCl": 0.5,
                    "NaHCO3": 1.2,
                },
                "resulting_profile": {
                    "calcium": 98.5,
                    "magnesium": 9.8,
                    "sodium": 14.7,
                    "chloride": 58.3,
                    "sulfate": 148.9,
                    "bicarbonate": 39.5,
                },
                "target_profile": {
                    "calcium": 100,
                    "magnesium": 10,
                    "sodium": 15,
                    "chloride": 60,
                    "sulfate": 150,
                    "bicarbonate": 40,
                },
            }
        }
    )


class WaterAdjustmentRequest(BaseModel):
    water_profile: dict = Field(
        ...,
        description="Starting water profile with ion concentrations in ppm",
    )
    salt_additions: dict = Field(
        ...,
        description="Salt additions in grams (e.g., {'CaSO4': 5.0, 'CaCl2': 3.0})",
    )
    water_volume_gal: float = Field(..., gt=0, description="Water volume in gallons")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "water_profile": {
                    "calcium": 10,
                    "magnesium": 2,
                    "sodium": 5,
                    "chloride": 8,
                    "sulfate": 5,
                    "bicarbonate": 20,
                },
                "salt_additions": {
                    "CaSO4": 5.0,
                    "CaCl2": 3.0,
                },
                "water_volume_gal": 5.0,
            }
        }
    )


class WaterAdjustmentResponse(BaseModel):
    calcium: float = Field(..., description="Resulting calcium in ppm")
    magnesium: float = Field(..., description="Resulting magnesium in ppm")
    sodium: float = Field(..., description="Resulting sodium in ppm")
    chloride: float = Field(..., description="Resulting chloride in ppm")
    sulfate: float = Field(..., description="Resulting sulfate in ppm")
    bicarbonate: float = Field(..., description="Resulting bicarbonate in ppm")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "calcium": 71.8,
                "magnesium": 2.0,
                "sodium": 5.0,
                "chloride": 45.6,
                "sulfate": 134.3,
                "bicarbonate": 20.0,
            }
        }
    )


@router.post(
    "/calculators/salt-ion-contribution",
    response_model=SaltIonContributionResponse,
    summary="Calculate salt ion contribution",
    response_description="Ion contribution from brewing salt addition",
)
async def calc_salt_ion_contribution(
    request: SaltIonContributionRequest,
) -> SaltIonContributionResponse:
    """Calculate the ion contribution from adding a brewing salt to water."""
    try:
        result = calculate_salt_ion_contribution(
            request.salt_type,
            request.amount_grams,
            request.water_volume_gal,
        )
        return SaltIonContributionResponse(**result)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=str(e))


@router.post(
    "/calculators/mineral-additions",
    response_model=MineralAdditionsResponse,
    summary="Calculate mineral additions",
    response_description="Recommended salt additions to reach target water profile",
)
async def calc_mineral_additions(
    request: MineralAdditionsRequest,
) -> MineralAdditionsResponse:
    """Calculate salt additions needed to adjust source water to target profile."""
    result = calculate_mineral_additions(
        request.source_profile,
        request.target_profile,
        request.water_volume_gal,
    )
    return MineralAdditionsResponse(**result)


@router.post(
    "/calculators/water-adjustment",
    response_model=WaterAdjustmentResponse,
    summary="Calculate water adjustment",
    response_description="Resulting water chemistry from salt additions",
)
async def calc_water_adjustment(
    request: WaterAdjustmentRequest,
) -> WaterAdjustmentResponse:
    """Calculate resulting water chemistry from salt additions."""
    result = calculate_water_adjustment(
        request.water_profile,
        request.salt_additions,
        request.water_volume_gal,
    )
    return WaterAdjustmentResponse(**result)


# Enhanced mash pH calculator


class MashPhRequest(BaseModel):
    water_profile: dict = Field(
        ...,
        description="Water profile with ion concentrations in ppm",
    )
    grain_bill_lbs: float = Field(..., gt=0, description="Total grain weight in pounds")
    water_volume_gal: float = Field(..., gt=0, description="Mash water volume in gallons")
    grain_color_lovibond: float = Field(
        3.0, ge=0, description="Average grain color in Lovibond (default 3.0)"
    )
    target_ph: float = Field(5.4, gt=0, le=14, description="Target mash pH (default 5.4)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "water_profile": {
                    "calcium": 75,
                    "magnesium": 10,
                    "sodium": 15,
                    "chloride": 60,
                    "sulfate": 120,
                    "bicarbonate": 50,
                },
                "grain_bill_lbs": 11.0,
                "water_volume_gal": 4.5,
                "grain_color_lovibond": 5.0,
                "target_ph": 5.4,
            }
        }
    )


class MashPhResponse(BaseModel):
    estimated_ph: float = Field(..., description="Estimated mash pH")
    target_ph: float = Field(..., description="Target mash pH")
    ph_difference: float = Field(..., description="Difference from target")
    residual_alkalinity: float = Field(..., description="Residual alkalinity")
    base_grain_ph: float = Field(..., description="Base pH from grain")
    water_to_grist_ratio: float = Field(..., description="Water to grist ratio (L/kg)")
    acid_addition_ml: float = Field(..., description="Recommended acid addition in mL")
    acid_type: str = Field(..., description="Type of acid recommended")
    alkalinity_reduction_needed: float = Field(
        ..., description="Alkalinity reduction needed (ppm as CaCO3)"
    )
    notes: str = Field(..., description="Recommendation notes")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "estimated_ph": 5.45,
                "target_ph": 5.4,
                "ph_difference": 0.05,
                "residual_alkalinity": 23.5,
                "base_grain_ph": 5.78,
                "water_to_grist_ratio": 3.2,
                "acid_addition_ml": 0.0,
                "acid_type": "lactic acid (88%)",
                "alkalinity_reduction_needed": 0.0,
                "notes": "Predicted pH is acceptable",
            }
        }
    )


@router.post(
    "/calculators/mash-ph",
    response_model=MashPhResponse,
    summary="Calculate mash pH with grain consideration",
    response_description="Predicted mash pH with acid addition recommendations",
)
async def calc_mash_ph(
    request: MashPhRequest,
) -> MashPhResponse:
    """
    Calculate predicted mash pH with grain bill consideration.
    
    This enhanced pH calculator considers:
    - Water chemistry (residual alkalinity)
    - Grain bill size and color
    - Water to grist ratio
    - Provides acid addition recommendations to reach target pH
    """
    result = calculate_mash_ph(
        request.water_profile,
        request.grain_bill_lbs,
        request.water_volume_gal,
        request.grain_color_lovibond,
        request.target_ph,
    )
    return MashPhResponse(**result)
