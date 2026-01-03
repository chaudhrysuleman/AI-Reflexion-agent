from pydantic import BaseModel, Field
from typing import List

class Reflection(BaseModel):
	missing: str = Field(description="What information is missing")
	superfluous: str = Field(description="What information is unnecessary")

class AnswerQuestion(BaseModel):
    answer: str = Field(description="Detailed response to the question. Must incorporate search findings.")
    reflection: Reflection = Field(description="Self-critique identifying missing info or inaccuracies.")
    search_queries: List[str] = Field(description="List 1-3 specific queries to verify or expand your answer.")

class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question."""
    references: List[str] = Field(description="MANDATORY: Provide full URLs for every claim made. List as a flat list of strings.")