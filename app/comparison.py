from app.retriever import search
from app.llm import compare_assessments


class AssessmentComparator:

    def __init__(self):
        pass

    def _find_assessment(self, name):

        results = search(name, k=1)

        if not results:
            return None

        return results[0]

    def compare(self, assessment1, assessment2):

        first = self._find_assessment(assessment1)

        second = self._find_assessment(assessment2)

        if first is None or second is None:

            return {
                "success": False,
                "reply": "I couldn't find one or both assessments in the SHL catalog.",
                "comparison": None
            }

        explanation = compare_assessments(
            first,
            second
        )

        return {

            "success": True,

            "reply": explanation,

            "comparison": {

                "assessment_1": {

                    "name": first["name"],
                    "duration": first.get("duration", ""),
                    "remote": first.get("remote", ""),
                    "adaptive": first.get("adaptive", ""),
                    "url": first["link"]

                },

                "assessment_2": {

                    "name": second["name"],
                    "duration": second.get("duration", ""),
                    "remote": second.get("remote", ""),
                    "adaptive": second.get("adaptive", ""),
                    "url": second["link"]

                }

            }

        }


if __name__ == "__main__":

    comparator = AssessmentComparator()

    result = comparator.compare(

        "OPQ32r",

        "Verify G+"

    )

    print(result["reply"])