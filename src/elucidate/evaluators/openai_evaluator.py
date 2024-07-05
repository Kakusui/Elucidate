## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing

## third-party imports
from easytl.services import openai_service

from easytl.decorators import _sync_logging_decorator
from easytl.classes import SystemTranslationMessage, ModelTranslationMessage, ChatCompletion, NOT_GIVEN
from easytl.util.constants import VALID_JSON_OPENAI_MODELS

## custom modules
from .protocols import OpenAIServiceProtocol

@staticmethod
def test(test:str | None = None) -> None:

    print("OpenAI Evaluator Test")


##-------------------start-of-attributes---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    _default_evaluation_instructions = SystemTranslationMessage("Please suggest a revised of the given text given it's translation.")

##-------------------start-of-_evaluate_translation()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    @_sync_logging_decorator
    def _evaluate_translation(evaluation_instructions:typing.Optional[SystemTranslationMessage],
                              evaluation_prompt:ModelTranslationMessage,
                              service:OpenAIServiceProtocol = typing.cast(OpenAIServiceProtocol, openai_service.OpenAIService)
                              ) -> ChatCompletion:
        
        """
        
        Synchronously translates the text using the OpenAI API.

        Parameters:
        translation_instructions (SystemTranslationMessage) : The instructions to use for the translation.
        translation_prompt (ModelTranslationMessage) : The text to translate.

        Returns:
        response (ChatCompletion) : The response from the API.

        """
        
        if(evaluation_instructions is None):
            evaluation_instructions = service._default_evaluation_instructions

        if(service._decorator_to_use is None):
            return service.__evaluate_translation(evaluation_instructions, evaluation_prompt)

        decorated_function = service._decorator_to_use(service.__evaluate_translation)
        return decorated_function(evaluation_instructions, evaluation_prompt)

##-------------------start-of-_translate_message()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __evaluate_translation(instructions:SystemTranslationMessage, 
                               prompt:ModelTranslationMessage,
                               service:OpenAIServiceProtocol = typing.cast(OpenAIServiceProtocol, openai_service.OpenAIService)
                               ) -> ChatCompletion:

        """

        Synchronously translates the text using the OpenAI API.

        Parameters:
        instructions (SystemTranslationMessage) : The instructions to use for the translation.
        prompt (ModelTranslationMessage) : The text to translate.

        Returns:
        response (ChatCompletion) : The response from the API.

        """

        response_format = "json_object" if service._json_mode and service._model in VALID_JSON_OPENAI_MODELS else "text"

        attributes = ["temperature", "logit_bias", "top_p", "n", "stream", "stop", "presence_penalty", "frequency_penalty", "max_tokens"]
        message_args = {
            "response_format": { "type": response_format },
            "model": service._model,
            "messages": [instructions.to_dict(), prompt.to_dict()],
            ## scary looking dict comprehension to get the attributes that are not NOT_GIVEN
            **{attr: getattr(service, f"_{attr}") for attr in attributes if getattr(service, f"_{attr}") != NOT_GIVEN}
        }

        response = service._sync_client.chat.completions.create(**message_args)
        
        return response