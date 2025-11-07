# Database/Schemas/choices.py

from pydantic import BaseModel, ConfigDict

CHOICE_BASE_EXAMPLE = {
    "choice_text": "Dry hop for four days at 18°C",
    "is_correct": True,
}


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": CHOICE_BASE_EXAMPLE}
    )