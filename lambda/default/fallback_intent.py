SKILL_NAME = 'Class on demand'
def fallback_intent(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes

    if ("game_state" in session_attr and
            session_attr["game_state"]=="STARTED"):
        speech_text = (
            "The {} skill can't help you with that.  "
            "Please answer the question".format(SKILL_NAME))
        reprompt = "Answer"
    else:
        speech_text = (
            "The {} skill can't help you with that.  "
            "Would you like to play?".format(SKILL_NAME))
        reprompt = "Say yes to start the game or no to quit."

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response