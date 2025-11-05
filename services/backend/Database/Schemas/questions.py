from pydantic import BaseModel
from typing import List
from .choices import ChoiceBase

QUESTION_BASE_EXAMPLE = {
    "question_text": "How long should the dry hop rest for a hazy IPA?",
    "choices": [
        {"choice_text": "24 hours at 10°C", "is_correct": False},
        {"choice_text": "4 days at 18°C", "is_correct": True},
        {"choice_text": "10 days at 5°C", "is_correct": False},
    ],
}


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

    class Config:
        orm_mode = True
        schema_extra = {"example": QUESTION_BASE_EXAMPLE}


class QuestionWithID(QuestionBase):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {**QUESTION_BASE_EXAMPLE, "id": 3},
        }
