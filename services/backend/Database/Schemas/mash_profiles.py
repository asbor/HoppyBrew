from pydantic import BaseModel
from typing import Optional

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
