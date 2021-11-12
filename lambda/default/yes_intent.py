import random

def yes_intent(handler_input):
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
    
    speech_text = (
        "Great! What is {} + {}?".format(
            session_attr["number_1"], session_attr["number_2"]))
    reprompt = "Try saying a number."
    
    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response