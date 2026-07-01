from app.state import ConversationState

def is_ready(state: ConversationState):
    """
    Decide whether we have enough information to recommend assessments.
    """

    # Role is mandatory
    if not state.role:
        return (
            False,
            "Which role are you hiring for?"
        )

    # Seniority or experience
    if not state.seniority and not state.experience:

        return (
            False,
            "What experience level are you hiring for? (Graduate, Junior, Mid, Senior, etc.)"
        )

    # Purpose
    
    # if not state.purpose:

    #     return (
    #         False,
    #         "Is this for hiring, selection, development, promotion, or another purpose?"
    #     )

    return True, None