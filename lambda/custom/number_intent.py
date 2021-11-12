import random

def number_intent(handler_input):
    """Handler for processing guess with target."""
    # type: (HandlerInput) -> Response
    session_attr = handler_input.attributes_manager.session_attributes
    target_num = session_attr["guess_number"]
    guess_num = int(handler_input.request_envelope.request.intent.slots[
        "number"].value)
        
    number_1 = session_attr['number_1']
    number_2 = session_attr['number_2']
    session_attr["no_of_guesses"] += 1
    session_attr["counter"] += 1
    
    ans = number_1 + number_2
    if guess_num == number_1 + number_2:
        session_attr['number_1'] = random.randint(0, 100)
        session_attr['number_2'] = random.randint(0, 100)
        session_attr["game_score"] += 1
        if session_attr["counter"] == 3:
            speech_text = (
                "Correct. Congratulations! You scored a {} out of 3 points! Thank you for playing!".format(session_attr["game_score"]))
            reprompt = "Say yes to start a new game or no to end the game"
            session_attr["game_state"] = "ENDED"
            handler_input.attributes_manager.persistent_attributes = session_attr
            handler_input.attributes_manager.save_persistent_attributes()
        else:
            speech_text = (
                "Correct. Your next question is what is {} + {}".format(
                    session_attr['number_1'], session_attr["number_2"]))
            reprompt = "Say yes to start a new game or no to end the game"
        
    elif guess_num != number_1 + number_2:
        session_attr['number_1'] = random.randint(0, 100)
        session_attr['number_2'] = random.randint(0, 100)
        if session_attr["counter"] == 3:
            speech_text = (
                "Incorrect. The correct answer is: {}. Congratulations, you finished the game! You scored a {} out of 3 points! Thank you for playing!".format(
                    ans, session_attr["game_score"]))
            reprompt = "Say yes to start a new game or no to end the game"
            session_attr["game_state"] = "ENDED"
            handler_input.attributes_manager.persistent_attributes = session_attr
            handler_input.attributes_manager.save_persistent_attributes()
        else:
            speech_text = (
                "Incorrect. The correct answer is: {}. Your next question is what is {} + {}".format(
                    ans, session_attr['number_1'], session_attr["number_2"]))
            reprompt = "Say yes to start a new game or no to end the game"
    else:
        speech_text = "Sorry, I didn't get that. Try saying a number."
        reprompt = "Try saying a number."

    handler_input.response_builder.speak(speech_text).ask(reprompt)
    return handler_input.response_builder.response