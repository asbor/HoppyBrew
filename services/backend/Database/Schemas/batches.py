from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum
from .batch_logs import BatchLog
from .hops import InventoryHop
from .fermentables import InventoryFermentable
from .miscs import InventoryMisc
from .yeasts import InventoryYeast


class BatchStatus(str, Enum):
    """Batch workflow status enum"""
    PLANNING = "planning"
    BREW_DAY = "brew_day"
    PRIMARY_FERMENTATION = "primary_fermentation"
    SECONDARY_FERMENTATION = "secondary_fermentation"
    CONDITIONING = "conditioning"
    PACKAGED = "packaged"
    COMPLETED = "completed"
    ARCHIVED = "archived"


BATCH_BASE_EXAMPLE = {
    "batch_name": "Citrus IPA - March Run",
    "batch_number": 1,
    "batch_size": 20.0,
    "brewer": "Alex Brewer",
    "brew_date": "2024-03-21T08:00:00Z",
    "status": "planning",
}

BATCH_FULL_EXAMPLE = {
    **BATCH_BASE_EXAMPLE,
    "id": 11,
    "recipe_id": 42,
    "created_at": "2024-03-21T08:00:00Z",
    "updated_at": "2024-03-22T10:30:00Z",
    "status": "primary_fermentation",
    "batch_log": {
        "id": 5,
        "log_entry": "Transferred to secondary fermenter.",
        "created_at": "2024-03-22T09:00:00Z",
    },
    "inventory_hops": [
        {
            "id": 7,
            "name": "Cascade",
            "origin": "USA",
            "alpha": 5.5,
            "type": "Aroma",
            "form": "Pellet",
            "beta": 6.0,
            "hsi": 15.0,
            "amount": 28.0,
            "use": "Dry Hop",
            "time": 3,
            "notes": "Added for burst of citrus aroma.",
            "display_amount": "28 g",
            "inventory": "4.5 kg",
            "display_time": "3 days",
            "batch_id": 11,
        }
    ],
    "inventory_fermentables": [
        {
            "id": 34,
            "name": "Pilsner Malt",
            "type": "Grain",
            "amount": 4.5,
            "yield_": 80.0,
            "color": 2,
            "origin": "Germany",
            "supplier": "Weyermann",
            "notes": "Provides crisp malt backbone.",
            "potential": 1.037,
            "inventory": 18.0,
            "display_amount": "4.5 kg",
            "batch_id": 11,
        }
    ],
    "inventory_miscs": [
        {
            "id": 15,
            "name": "Irish Moss",
            "type": "Fining",
            "use": "Boil",
            "amount": 14,
            "time": 10,
            "display_amount": "14 g",
            "display_time": "10 min",
            "batch_id": 11,
        }
    ],
    "inventory_yeasts": [
        {
            "id": 22,
            "name": "SafAle US-05",
            "type": "Ale",
            "form": "Dry",
            "attenuation": 78.0,
            "notes": "Clean American ale yeast.",
            "batch_id": 11,
        }
    ],
}


class BatchBase(BaseModel):
    batch_name: str
    batch_number: int
    batch_size: float
    brewer: str
    brew_date: datetime
    status: Optional[BatchStatus] = BatchStatus.PLANNING

    model_config = ConfigDict(
        json_schema_extra={"example": BATCH_BASE_EXAMPLE}
    )
class BatchCreate(BatchBase):
    recipe_id: int

    model_config = ConfigDict(
        json_schema_extra={"example": {**BATCH_BASE_EXAMPLE, "recipe_id": 42}}
    )
class BatchUpdate(BaseModel):
    batch_name: Optional[str] = None
    batch_number: Optional[int] = None
    batch_size: Optional[float] = None
    brewer: Optional[str] = None
    brew_date: Optional[datetime] = None
    status: Optional[BatchStatus] = None

    model_config = ConfigDict(
        json_schema_extra={            "example": {                "batch_name": "Citrus IPA - March Run",                "batch_number": 2,                "batch_size": 21.0,                "brewer": "Alex Brewer",                "brew_date": "2024-03-28T08:00:00Z",                "status": "brew_day",            }        }
    )
class Batch(BatchBase):
    id: int
    recipe_id: int
    created_at: datetime
    updated_at: datetime
    status: BatchStatus
    batch_log: Optional[BatchLog] = None
    inventory_hops: List[InventoryHop]
    inventory_fermentables: List[InventoryFermentable]
    inventory_miscs: List[InventoryMisc]
    inventory_yeasts: List[InventoryYeast]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": BATCH_FULL_EXAMPLE}
    )