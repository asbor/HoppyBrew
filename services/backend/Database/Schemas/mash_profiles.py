from pydantic import BaseModel
from typing import Optional, List

MASH_PROFILE_EXAMPLE = {
    "name": "Single Infusion, Medium Body",
    "version": 1,
    "grain_temp": 22,
    "tun_temp": 21,
    "sparge_temp": 76,
    "ph": 5,
    "tun_weight": 15,
    "tun_specific_heat": 3,
    "notes": "Standard single infusion mash aimed at medium body ales.",
    "display_grain_temp": "22 °C",
    "display_tun_temp": "21 °C",
    "display_sparge_temp": "76 °C",
    "display_tun_weight": "15 lb",
}

MASH_STEP_EXAMPLE = {
    "name": "Single Infusion",
    "type": "Infusion",
    "step_temp": 66,
    "step_time": 60,
    "ramp_time": 2,
    "description": "Main conversion step",
    "display_step_temp": "66 °C",
}


class MashStepBase(BaseModel):
    """
    Schema for mash step data.
    """

    name: Optional[str] = None
    version: Optional[int] = None
    type: Optional[str] = None
    infuse_amount: Optional[int] = None
    step_time: Optional[int] = None
    step_temp: Optional[int] = None
    ramp_time: Optional[int] = None
    end_temp: Optional[int] = None
    description: Optional[str] = None
    water_grain_ratio: Optional[str] = None
    decoction_amt: Optional[str] = None
    infuse_temp: Optional[int] = None
    display_step_temp: Optional[str] = None
    display_infuse_amt: Optional[str] = None
    mash_id: Optional[int] = None

    class Config:
        schema_extra = {"example": MASH_STEP_EXAMPLE}


class MashProfileBase(BaseModel):
    """
    Description:

    This class represents the MashProfile table in the database.

    Use cases:

    - Validate the data of a new MashProfile object

    - Validate the data of a MashProfile object to be updated

    Notes:

    - The id field is not included in the base model because it is generated
    by the database

    """

    name: Optional[str] = None
    version: Optional[int] = None
    grain_temp: Optional[int] = None
    tun_temp: Optional[int] = None
    sparge_temp: Optional[int] = None
    ph: Optional[int] = None
    tun_weight: Optional[int] = None
    tun_specific_heat: Optional[int] = None
    # equip_adjust: bool

    notes: Optional[str] = None
    display_grain_temp: Optional[str] = None
    display_tun_temp: Optional[str] = None
    display_sparge_temp: Optional[str] = None
    display_tun_weight: Optional[str] = None

    class Config:
        schema_extra = {"example": MASH_PROFILE_EXAMPLE}
