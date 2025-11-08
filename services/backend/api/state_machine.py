"""
State machine logic for batch status workflow
"""

from Database.enums import BatchStatus, BATCH_STATUS_TRANSITIONS
from fastapi import HTTPException


def validate_status_transition(
    current_status: BatchStatus, new_status: BatchStatus
) -> bool:
    """
    Validate if a status transition is allowed

    Args:
        current_status: Current batch status
        new_status: New batch status to transition to

    Returns:
        True if transition is valid

    Raises:
        HTTPException: If transition is invalid
    """
    if current_status == new_status:
        raise HTTPException(
            status_code=400, detail=f"Batch is already in {current_status.value} status"
        )

    valid_transitions = BATCH_STATUS_TRANSITIONS.get(current_status, [])

    if new_status not in valid_transitions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {current_status.value} to {new_status.value}. "
            f"Valid transitions: {', '.join([s.value for s in valid_transitions])}",
        )

    return True


def get_valid_transitions(current_status: BatchStatus) -> list[BatchStatus]:
    """
    Get list of valid status transitions from current status

    Args:
        current_status: Current batch status

    Returns:
        List of valid next statuses
    """
    return BATCH_STATUS_TRANSITIONS.get(current_status, [])
