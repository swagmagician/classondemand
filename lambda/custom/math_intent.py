import random

def math_intent(handler_input):
    """Handler for Yes Intent, only if the player said yes for
    a new game.
    """
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    session_attr['game_state'] = "STARTED"
    session_attr['guess_number'] = random.randint(0, 100)
    session_attr['no_of_guesses'] = 0
    session_attr['number_1'] = random.randint(0, 100)
    session_attr['number_2'] = random.randint(0, 100)
    session_attr['game_score'] = 0
    session_attr['counter'] = 0

    speech_text = (
        "You have selected math! Let the games begin! What is {} + {}?".format(
            session_attr["number_1"], session_attr["number_2"]))
    reprompt = ("What is {} + {}?".format(
        session_attr["number_1"], session_attr["number_2"]))
    
    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response