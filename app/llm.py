import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------------------------------------------------
# Generic Gemini Call
# ---------------------------------------------------------

def ask_gemini(prompt):

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return text

    except Exception as e:

        print("Gemini Error:", e)

        if "429" in str(e) or "ResourceExhausted" in str(e):
            raise Exception(
                "Gemini API quota exceeded. Please try again later."
            )

        raise Exception(
            "Unable to contact Gemini API."
        )


# ---------------------------------------------------------
# Conversation Understanding
# ---------------------------------------------------------

def analyze_conversation(messages):

    schema = """
{
    "action": "",

    "assessment_1": null,

    "assessment_2": null,

    "clarification_question": null,

    "state": {

        "role": null,

        "seniority": null,

        "experience": null,

        "purpose": null,

        "industry": null,

        "language": null,

        "skills": [],

        "assessment_types": [],

        "constraints": []

    }
}
"""

    prompt = f"""
You are SHL's AI Assessment Recommendation Assistant.

Understand the conversation and return ONLY valid JSON.

--------------------------------------------------

Possible actions

clarify
retrieve
compare
refine
refuse

--------------------------------------------------

CLARIFY

Ask a clarification question ONLY if required.

Normally recommendations can be made once you know

- role
- seniority OR experience

Purpose is optional.

Do NOT ask unnecessary questions.

Do NOT ask about programming languages.

Do NOT ask about obvious skills already implied by the role.

--------------------------------------------------

RETRIEVE

If enough hiring information exists

return

action = retrieve

--------------------------------------------------

COMPARE

If the user asks to compare two SHL assessments

return

action = compare

Extract

assessment_1

assessment_2

Example

Compare OPQ32r and Verify G+

↓

{{
"action":"compare",

"assessment_1":"OPQ32r",

"assessment_2":"Verify G+",

"clarification_question":null,

"state":{{

"role":null,

"seniority":null,

"experience":null,

"purpose":null,

"industry":null,

"language":null,

"skills":[],

"assessment_types":[],

"constraints":[]

}}

}}
--------------------------------------------------

REFINE

If the user wants to modify previously recommended assessments,
return

action = refine

Examples

Add cognitive assessment

Remove personality assessment

Only remote assessments

Only adaptive assessments

English only

Limit duration to 30 minutes
--------------------------------------------------

REFUSE

If unrelated to SHL assessments.

--------------------------------------------------

Rules

language = spoken language

Programming languages belong inside skills.

Examples

Java

Python

SQL

AWS

Docker

Spring

↓

skills

--------------------------------------------------

Schema

{schema}

Conversation

{json.dumps(messages, indent=2)}
"""

    response = ask_gemini(prompt)

    try:

        data = json.loads(response)

    except Exception:

        data = {

            "action": "clarify",

            "assessment_1": None,

            "assessment_2": None,

            "clarification_question":
            "Which role are you hiring for?",

            "state": {

                "role": None,

                "seniority": None,

                "experience": None,

                "purpose": None,

                "industry": None,

                "language": None,

                "skills": [],

                "assessment_types": [],

                "constraints": []

            }

        }

    data.setdefault("assessment_1", None)
    data.setdefault("assessment_2", None)

    return data


# ---------------------------------------------------------
# Recommendation Explanation
# ---------------------------------------------------------

def explain_recommendations(messages, recommendations):

    prompt = f"""
You are an SHL hiring expert.

Conversation

{json.dumps(messages, indent=2)}

Recommended assessments

{json.dumps(recommendations, indent=2)}

Write a concise explanation.

Rules

Explain WHY these assessments fit.

Mention important skills.

Mention knowledge, cognitive or personality
ONLY if they actually appear.

Maximum 150 words.

No bullet points.

No markdown.

Do not mention similarity scores.

Return plain text only.
"""

    return ask_gemini(prompt)


# ---------------------------------------------------------
# Assessment Comparison
# ---------------------------------------------------------

def compare_assessments(first, second):

    prompt = f"""
You are an SHL assessment expert.

Compare these two assessments.

Assessment 1

{json.dumps(first, indent=2)}

Assessment 2

{json.dumps(second, indent=2)}

Compare

- Purpose

- Skills measured

- Job level

- Duration

- Remote testing

- Adaptive

- Best use cases

Write a concise professional comparison.

Maximum 200 words.

Do not use markdown tables.

Return plain text.
"""

    return ask_gemini(prompt)