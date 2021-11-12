def help_intent(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Please choose a subject"
    reprompt = "Please choose a subject"

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response