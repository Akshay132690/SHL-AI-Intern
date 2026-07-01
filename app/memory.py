from copy import deepcopy
from app.state import ConversationState


class ConversationMemory:

    def __init__(self):
        self.state = ConversationState()

    def get_state(self):
        return self.state

    def reset(self):
        self.state = ConversationState()

    def update(self, extracted):

        if extracted.get("role"):
            self.state.role = extracted["role"]

        if extracted.get("seniority"):
            self.state.seniority = extracted["seniority"]

        if extracted.get("experience"):
            self.state.experience = extracted["experience"]

        if extracted.get("purpose"):
            self.state.purpose = extracted["purpose"]

        if extracted.get("industry"):
            self.state.industry = extracted["industry"]

        if extracted.get("language"):
            self.state.language = extracted["language"]

        # ---------- Skills ----------

        skills = extracted.get("skills", [])

        for skill in skills:

            if skill not in self.state.skills:
                self.state.skills.append(skill)

        # ---------- Assessment Types ----------

        assessment_types = extracted.get(
            "assessment_types",
            []
        )

        for item in assessment_types:

            if item not in self.state.assessment_types:
                self.state.assessment_types.append(item)

        # ---------- Constraints ----------

        constraints = extracted.get(
            "constraints",
            []
        )

        for item in constraints:

            if item not in self.state.constraints:
                self.state.constraints.append(item)

    def to_dict(self):

        return {

            "role": self.state.role,

            "seniority": self.state.seniority,

            "experience": self.state.experience,

            "purpose": self.state.purpose,

            "industry": self.state.industry,

            "language": self.state.language,

            "skills": deepcopy(self.state.skills),

            "assessment_types": deepcopy(
                self.state.assessment_types
            ),

            "constraints": deepcopy(
                self.state.constraints
            )

        }

    def print_state(self):

        print("\n========== MEMORY ==========")

        print(f"Role          : {self.state.role}")
        print(f"Seniority     : {self.state.seniority}")
        print(f"Experience    : {self.state.experience}")
        print(f"Purpose       : {self.state.purpose}")
        print(f"Industry      : {self.state.industry}")
        print(f"Language      : {self.state.language}")
        print(f"Skills        : {self.state.skills}")
        print(f"Assessments   : {self.state.assessment_types}")
        print(f"Constraints   : {self.state.constraints}")

        print("============================\n")