def cancel_and_stop_intent(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Thanks for playing!!"

    handler_input.response_builder.speak(
        speech_text).set_should_end_session(True)
    return handler_input.response_builder.response