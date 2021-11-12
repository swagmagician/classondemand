def session_ended(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    logger.info(
        "Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
    return handler_input.response_builder.response