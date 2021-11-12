def launch_request(handler_input):
    """Handler for Skill Launch.

    Get the persistence attributes, to figure out the game state.
    """
    # type: (HandlerInput) -> Response
    attr = handler_input.attributes_manager.persistent_attributes
    if not attr:
        attr['ended_session_count'] = 0
        attr['games_played'] = 0
        attr['game_state'] = 'ENDED'

    handler_input.attributes_manager.session_attributes = attr

    speech_text = "Welcome to class on demand! What game would you like to play: Math, Spelling, or Colors"
    reprompt = "What game would you like to play: Math, Spelling, or Colors"

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response