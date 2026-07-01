from dataclasses import dataclass, field


@dataclass
class ConversationState:

    role: str | None = None
    seniority: str | None = None
    experience: str | None = None
    purpose: str | None = None

    industry: str | None = None
    language: str | None = None

    skills: list[str] = field(default_factory=list)

    assessment_types: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)

    recommendations: list = field(default_factory=list)

    clarification_count: int = 0

    completed: bool = False