from pydantic import BaseModel, Field, field_validator

class AskRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=2000)

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Question cannot be blank.")
        return value.strip()

class AskResponse(BaseModel):
    status: str
    question: str
    answer: str
    sources: list[str]
    disclaimer: str
