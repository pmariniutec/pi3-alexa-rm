import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import db_utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

other_request_output = "\n ¿Alguna otra consulta?"
help_text = "estado de un equipo específico. equipos inactivos por x días. equipos asignados a una persona. personas con múltiples equipos asignados. información sobre equipo"


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        speak_output = "Hola, ¿Que desea consultar?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .ask("reprompt")
            .response
        )


class InactiveAssetsIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("InactiveAssetsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slot_key = "number"
        slots = handler_input.request_envelope.request.intent.slots
        num_days = slots[slot_key].value
        inactive_items = db_utils.get_inactive_n_days(num_days)
        days_txt = "día" if num_days == 1 else "días"
        if inactive_items is not None:
            speak_output = "Hay {0} equipos inactivos por {1} {2}.".format(
                inactive_items, num_days, days_txt)
            speak_output += other_request_output
        else:
            speak_output = "No existen equipos inactivos por {0} {1}.".format(
                num_days, days_txt)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class AssetStateIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AssetStateIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        assetBrand = slots["assetBrand"].value
        assetNumber = slots["assetNumber"].value
        state = db_utils.get_asset_state(assetBrand + assetNumber)
        if state is not None:
            speak_output = "El equipo {0} se encuentra {1}.".format(
                assetBrand + assetNumber, state)
            speak_output += other_request_output
        else:
            speak_output = "Al parecer ese equipo no existe, por favor vuelva a pronunciar la marca y número del equipo."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class PersonAssetsIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PersonAssetsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        personName = slots["personName"].value
        personLastName = slots["personLastName"].value
        fullName = "{0} {1}".format(personName, personLastName)
        data = db_utils.get_person_assets(personName, personLastName)
        if data is not None and len(data) > 0:
            assets = ", ".join(d[0] for d in data)
            msg = ("el siguiente equipo:" if len(data) == 1 else "los siguientes equipos:") + \
                " {0} con el siguiente usuario {1}".format(assets, data[0][1])

            speak_output = "La persona {0} tiene asignado {1}.".format(
                fullName, msg)
            speak_output += other_request_output
        else:
            speak_output = "Al parecer esa persona no existe o no tiene ningún equipo asignado."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class UsersMultipleAssetsIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("UsersMultipleAssetsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        user_count = db_utils.get_users_multiple_assets()
        if user_count is not None:
            speak_output = "Claro, las personas con múltiples equipos son: {0}.".format(
                user_count)
            speak_output += other_request_output
        else:
            speak_output = "Ninguna persona en este momento"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class AssetInfoIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AssetInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        assetBrand = slots["assetBrand"].value
        assetNumber = slots["assetNumber"].value
        assignee = db_utils.get_asset_assignee(assetBrand + assetNumber)
        if assignee is not None:
            speak_output = "El equipo {0} se encuentra asignado a {1}.".format(
                assetBrand + assetNumber, assignee)
            speak_output += other_request_output
        else:
            speak_output = "Al parecer ese equipo no existe, por favor vuelve a pronunciar la marca y número del equipo."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class AssetInfoCompleteIntentHandler(AbstractRequestHandler):
    """
        NOTE: unsused, left for show
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AssetInfoCompleteIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        assetBrand = slots["assetBrand"].value
        assetNumber = slots["assetNumber"].value
        state = db_utils.get_asset_info_complete(assetBrand + assetNumber)
        speak_output = "La informacion del activo {0} es {1}".format(
            assetBrand + assetNumber, state)

        return (
            handler_input.response_builder
            .speak(speak_output + other_request_output)
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = help_text

        return (
            handler_input.response_builder
            .speak(speak_output + other_request_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Adios. Gracias por usar Valtx Query"

        return (
            handler_input.response_builder
            .speak(speak_output + other_request_output)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Intent: {0}".format(intent_name)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speak_output = "Error"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(InactiveAssetsIntentHandler())
sb.add_request_handler(AssetStateIntentHandler())
sb.add_request_handler(PersonAssetsIntentHandler())
sb.add_request_handler(UsersMultipleAssetsIntentHandler())
sb.add_request_handler(AssetInfoIntentHandler())
sb.add_request_handler(AssetInfoCompleteIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
