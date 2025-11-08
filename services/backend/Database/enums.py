"""
Shared enums for the application
"""

from enum import Enum


class BatchStatus(str, Enum):
    """Batch workflow status enum"""

    PLANNING = "planning"
    BREWING = "brewing"
    FERMENTING = "fermenting"
    CONDITIONING = "conditioning"
    PACKAGING = "packaging"
    COMPLETE = "complete"
    ARCHIVED = "archived"


# Valid state transitions for batch workflow
BATCH_STATUS_TRANSITIONS = {
    BatchStatus.PLANNING: [BatchStatus.BREWING, BatchStatus.ARCHIVED],
    BatchStatus.BREWING: [BatchStatus.FERMENTING, BatchStatus.ARCHIVED],
    BatchStatus.FERMENTING: [BatchStatus.CONDITIONING, BatchStatus.ARCHIVED],
    BatchStatus.CONDITIONING: [BatchStatus.PACKAGING, BatchStatus.ARCHIVED],
    BatchStatus.PACKAGING: [BatchStatus.COMPLETE, BatchStatus.ARCHIVED],
    BatchStatus.COMPLETE: [BatchStatus.ARCHIVED],
    BatchStatus.ARCHIVED: [],  # Terminal state
}
