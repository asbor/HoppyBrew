from pydantic import BaseModel, ConfigDict
from typing import Optional

EQUIPMENT_PROFILE_EXAMPLE = {
    "name": "10 Gallon Electric Brewery",
    "version": 1,
    "boil_size": 38,
    "batch_size": 23,
    "tun_volume": 45,
    "tun_weight": 15,
    "tun_specific_heat": 3,
    "top_up_water": 0,
    "trub_chiller_loss": 2,
    "evap_rate": 12,
    "boil_time": 60,
    "calc_boil_volume": True,
    "lauter_deadspace": 1,
    "top_up_kettle": 0,
    "hop_utilization": 100,
    "notes": "Configured for single-vessel electric brewing.",
    "display_boil_size": "10 gal",
    "display_batch_size": "6 gal",
    "display_tun_volume": "12 gal",
    "display_tun_weight": "15 lb",
    "display_top_up_water": "0 gal",
    "display_trub_chiller_loss": "0.5 gal",
    "display_lauter_deadspace": "0.25 gal",
    "display_top_up_kettle": "0 gal",
}


class EquipmentProfileBase(BaseModel):
    """
    Description:

    This class represents the EquipmentProfile table in the database.

    Use cases:

    - Validate the data of a new EquipmentProfile object

    - Validate the data of a EquipmentProfile object to be updated

    Notes:

    - The id field is not included in the base model because it is generated
    by the database

    """

    name: Optional[str] = None
    version: Optional[int] = None
    boil_size: Optional[int] = None
    batch_size: Optional[int] = None
    tun_volume: Optional[int] = None
    tun_weight: Optional[int] = None
    tun_specific_heat: Optional[int] = None
    top_up_water: Optional[int] = None
    trub_chiller_loss: Optional[int] = None
    evap_rate: Optional[int] = None
    boil_time: Optional[int] = None
    calc_boil_volume: bool = False
    lauter_deadspace: Optional[int] = None
    top_up_kettle: Optional[int] = None
    hop_utilization: Optional[int] = None
    notes: Optional[str] = None
    display_boil_size: Optional[str] = None
    display_batch_size: Optional[str] = None
    display_tun_volume: Optional[str] = None
    display_tun_weight: Optional[str] = None
    display_top_up_water: Optional[str] = None
    display_trub_chiller_loss: Optional[str] = None
    display_lauter_deadspace: Optional[str] = None
    display_top_up_kettle: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={"example": EQUIPMENT_PROFILE_EXAMPLE}
    )