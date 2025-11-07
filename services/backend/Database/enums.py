"""
Shared enums for the application
"""
from enum import Enum


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
