from pydantic import BaseModel
from typing import Optional


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
