
from app.llm import (
    analyze_conversation,
    explain_recommendations
)

from app.recommender import RecommendationEngine
from app.memory import ConversationMemory
from app.validator import is_ready
from app.comparison import AssessmentComparator


class SHLAgent:

    def __init__(self):

        self.memory = ConversationMemory()

        self.recommender = RecommendationEngine()

        self.comparator = AssessmentComparator()

    # --------------------------------------------------

    def reset(self):

        self.memory.reset()

    # --------------------------------------------------

    def _format_recommendations(self, recommendations):

        formatted = []

        for item in recommendations:

            formatted.append({

                "name": item.get("name"),

                "url": item.get("link"),

                "description": item.get(
                    "description", ""
                ),

                "duration": item.get(
                    "duration", ""
                ),

                "remote": item.get(
                    "remote", ""
                ),

                "adaptive": item.get(
                    "adaptive", ""
                ),

                "job_levels": item.get(
                    "job_levels", []
                ),

                "languages": item.get(
                    "languages", []
                ),

                "score": round(
                    item.get("score", 0),
                    4
                )

            })

        return formatted

    # --------------------------------------------------

    def chat(self, messages):

        try:
            analysis = analyze_conversation(messages)
        except Exception as e:

            return {

                "reply": str(e),

                "recommendations": None,

                "comparison": None,

                "end_of_conversation": False

            }

        print("\n========== ANALYSIS ==========")
        print(analysis)
        print("==============================")

        action = analysis["action"]

        # --------------------------------------------------
        # REFUSE
        # --------------------------------------------------

        if action == "refuse":

            return {

                "reply":
                "I can help with SHL assessment recommendations and comparisons.",

                "recommendations": None,

                "comparison": None,

                "end_of_conversation": False

            }

        # --------------------------------------------------
        # COMPARE
        # --------------------------------------------------

        if action == "compare":

            result = self.comparator.compare(

                analysis.get("assessment_1"),

                analysis.get("assessment_2")

            )

            return {

                "reply": result["reply"],

                "recommendations": None,

                "comparison": result["comparison"],

                "end_of_conversation": True

            }
            # --------------------------------------------------
        # REFINE
        # --------------------------------------------------

        if action == "refine":

            state = self.memory.get_state()

            recommendations = self.recommender.recommend(state)

            explanation = explain_recommendations(
                messages,
                recommendations
            )

            return {

                "reply": explanation,

                "recommendations": self._format_recommendations(
                    recommendations
                ),

                "comparison": None,

                "end_of_conversation": True

            }

        # --------------------------------------------------
        # UPDATE MEMORY
        # --------------------------------------------------

        self.memory.update(

            analysis["state"]

        )

        self.memory.print_state()

        state = self.memory.get_state()

        # --------------------------------------------------
        # VALIDATE
        # --------------------------------------------------

        ready, question = is_ready(state)

        if not ready:

            return {

                "reply": question,

                "recommendations": None,

                "comparison": None,

                "end_of_conversation": False

            }

        # --------------------------------------------------
        # RECOMMEND
        # --------------------------------------------------

        recommendations = self.recommender.recommend(
            state
        )

        try:

            explanation = explain_recommendations(

                messages,

                recommendations

            )

        except Exception:

            explanation = (
                "Based on the provided role and requirements, "
                "these are the most relevant SHL assessments."
            )

        response = self._format_recommendations(

            recommendations

        )

        return {

            "reply": explanation,

            "recommendations": response,

            "comparison": None,

            "end_of_conversation": True

        }


# ======================================================
# LOCAL TERMINAL TEST
# ======================================================

if __name__ == "__main__":

    agent = SHLAgent()

    history = []

    print("\n=======================================")
    print(" SHL Assessment Recommendation Agent ")
    print("=======================================\n")

    while True:

        user = input("You: ")

        if user.lower() == "exit":
            break

        if user.lower() == "reset":

            history = []

            agent.reset()

            print("\nConversation Reset.\n")

            continue

        history.append({

            "role": "user",

            "content": user

        })

        result = agent.chat(history)

        print("\nAssistant:\n")

        print(result["reply"])

        if result["comparison"]:

            print("\nComparison\n")

            print(result["comparison"])

        if result["recommendations"]:

            print("\nRecommended Assessments\n")

            for i, item in enumerate(

                result["recommendations"],

                start=1

            ):

                print("=" * 70)

                print(f"{i}. {item['name']}")

                print(item["url"])

                print(f"Duration : {item['duration']}")

                print(f"Remote   : {item['remote']}")

                print(f"Adaptive : {item['adaptive']}")

                print()

        history.append({

            "role": "assistant",

            "content": result["reply"]

        })