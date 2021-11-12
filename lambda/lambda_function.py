# -*- coding: utf-8 -*-

# Class on Demand(COD)
# The skill serves as a simple sample on how to use the
# persistence attributes and persistence adapter features in the SDK.
import random
import logging
import os
import boto3

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

from launch import *
from session_ended import *
from default import help_intent, cancelled_intent, fallback_intent, no_intent, yes_intent

from etc import unhandled_intent
from custom import number_intent, math_intent
SKILL_NAME = 'Class on demand'
ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')
ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)
sb = CustomSkillBuilder(persistence_adapter=dynamodb_adapter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch.

    Get the persistence attributes, to figure out the game state.
    """
    # type: (HandlerInput) -> Response
    return launch_request(handler_input)

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    return help_intent.help_intent(handler_input)

@sb.request_handler(
    can_handle_func=lambda input:
        is_intent_name("AMAZON.CancelIntent")(input) or
        is_intent_name("AMAZON.StopIntent")(input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    return cancelled_intent.cancel_and_stop_intent(handler_input)

@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    logger.info(
        "Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
    return handler_input.response_builder.response

def currently_playing(handler_input):
    """Function that acts as can handle for game state."""
    # type: (HandlerInput) -> bool
    is_currently_playing = False
    session_attr = handler_input.attributes_manager.session_attributes

    if ("game_state" in session_attr
            and session_attr['game_state'] == "STARTED"):
        is_currently_playing = True

    return is_currently_playing

@sb.request_handler(can_handle_func=lambda input:
                    not currently_playing(input) and
                    is_intent_name("AMAZON.YesIntent")(input))
def yes_handler(handler_input):
    """Handler for Yes Intent
    """
    # type: (HandlerInput) -> Response
    return yes_intent.yes_intent(handler_input)

@sb.request_handler(can_handle_func=lambda input:
                    not currently_playing(input) and
                    is_intent_name("MathIntent")(input))
def math_handler(handler_input):
    """Handler for Math Intent
    """
    # type: (HandlerInput) -> Response
    return math_intent.math_intent(handler_input)

@sb.request_handler(can_handle_func=lambda input:
                    not currently_playing(input) and
                    is_intent_name("AMAZON.NoIntent")(input))
def no_handler(handler_input):
    """Handler for No Intent
    """
    # type: (HandlerInput) -> Response
    return no_intent.no_intent(handler_input)

@sb.request_handler(can_handle_func=lambda input:
                    currently_playing(input) and
                    is_intent_name("NumberGuessIntent")(input))
def number_handler(handler_input):
    """Handler for processing answer."""
    # type: (HandlerInput) -> Response
    return number_intent.number_intent(handler_input)

@sb.request_handler(can_handle_func=lambda input:
                    is_intent_name("AMAZON.FallbackIntent")(input) or
                    is_intent_name("AMAZON.YesIntent")(input) or
                    is_intent_name("AMAZON.NoIntent")(input))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent only available in en-US locale.
    """
    # type: (HandlerInput) -> Response
    return fallback_intent.fallback_intent(handler_input)

@sb.request_handler(can_handle_func=lambda input: True)
def unhandled_intent_handler(handler_input):
    """Handler for all other unhandled requests."""
    # type: (HandlerInput) -> Response
    unhandled_intent.unhandled_intent(handler_input)

@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)
    speech = "Sorry, I can't understand that. Please say again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response

@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Response logger."""
    # type: (HandlerInput, Response) -> None
    logger.info("Response: {}".format(response))

lambda_handler = sb.lambda_handler()
