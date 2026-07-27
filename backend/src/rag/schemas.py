from pydantic import BaseModel, Field

class Source(BaseModel):
    title: str
    location: str | None = None
    score: float | None = None


class LLMResponse(BaseModel):
    answer: str = Field(description="Respuesta")
    sources: list[Source] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)