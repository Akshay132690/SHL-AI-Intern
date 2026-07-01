from app import state
from app.retriever import search


class RecommendationEngine:

    def __init__(self):
        pass

    # ----------------------------------------------------

    def _build_query(self, state):

        parts = []

        if state.role:
            parts.append(state.role)

        if state.seniority:
            parts.append(state.seniority)

        if state.experience:
            parts.append(state.experience)

        if state.industry:
            parts.append(state.industry)

        if state.skills:
            parts.extend(state.skills)

        return " ".join(parts)

    # ----------------------------------------------------

    def _remove_duplicates(self, results):

        unique = []
        seen = set()

        for item in results:

            name = item["name"].lower()

            if name not in seen:
                seen.add(name)
                unique.append(item)

        return unique

    # ----------------------------------------------------

    def _apply_constraints(self, results, state):

        filtered = results

        for constraint in state.constraints:

            c = constraint.lower()

            if "remote" in c:

                temp = [
                    r for r in filtered
                    if r.get("remote", "").lower() == "yes"
                ]

                if temp:
                    filtered = temp

            elif "adaptive" in c:

                temp = [
                    r for r in filtered
                    if r.get("adaptive", "").lower() == "yes"
                ]

                if temp:
                    filtered = temp

            elif "english" in c:

                temp = []

                for r in filtered:

                    langs = " ".join(
                        r.get("languages", [])
                    ).lower()

                    if "english" in langs:
                        temp.append(r)

                if temp:
                    filtered = temp

        return filtered

    # ----------------------------------------------------

    def _boost_score(self, item, state):

        score = item.get("score", 0)

        text = (
            item.get("name", "") + " " +
            item.get("description", "")
        ).lower()

        keys = " ".join(
            item.get("keys", [])
        ).lower()

        job_levels = " ".join(
            item.get("job_levels", [])
        ).lower()

        # -----------------------------
        # Skill Matching
        # -----------------------------

        for skill in state.skills:

            if skill.lower() in text:
                score += 0.35

        # -----------------------------
        # Role Matching
        # -----------------------------

        if state.role:

            for word in state.role.lower().split():

                if len(word) > 2 and word in text:
                    score += 0.20
        # Prefer Java assessments for Java roles

        if "java" in state.role.lower() or "java" in [s.lower() for s in state.skills]:

            if "java" in text:
                score += 0.50

            if "javascript" in text:
                score -= 0.30
        # -----------------------------
        # Prefer Knowledge Tests
        # -----------------------------

        if "knowledge" in keys:
            score += 0.30

        # -----------------------------
        # Ability Tests
        # -----------------------------

        if "ability" in keys:
            score += 0.10

        # -----------------------------
        # Personality
        # -----------------------------

        if "personality" in keys:
            score += 0.05

        # -----------------------------
        # Seniority Match
        # -----------------------------

        if state.seniority:

            seniority = state.seniority.lower()

            if seniority in job_levels:
                score += 0.15

            # Boost senior-level assessments
            if seniority == "senior":

                if "manager" in job_levels:
                    score += 0.40

                if "director" in job_levels:
                    score += 0.40

                if "executive" in job_levels:
                    score += 0.40

                # Penalize entry-level assessments
                if "entry-level" in job_levels:
                    score -= 0.60

                if "graduate" in job_levels:
                    score -= 0.60
        

        # -----------------------------
        # Penalize generic reports
        # -----------------------------

        generic = [

            "report",

            "development report",

            "hipo",

            "readiness",

            "candidate report",

            "manager report"

        ]

        technical = False

        for s in state.skills:

            if s.lower() in [

                "java",

                "python",

                "sql",

                "aws",

                "docker",

                "spring",

                "react",

                "javascript",

                "c++",

                "node",

                "backend",

                "frontend"

            ]:

                technical = True

        if technical:

            for g in generic:

                if g in text:
                    score -= 0.40

        return score

    # ----------------------------------------------------

    def recommend(self, state):

        query = self._build_query(state)

        print(f"\nSearching for: {query}")

        results = search(query, k=25)

        results = self._remove_duplicates(results)

        results = self._apply_constraints(results, state)

        for item in results:

            item["score"] = self._boost_score(
                item,
                state
            )

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:8]