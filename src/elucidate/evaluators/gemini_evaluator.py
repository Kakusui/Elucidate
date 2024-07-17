## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing
import asyncio

## third-party imports
import google.generativeai as genai

## custom modules
from ..protocols.gemini_service_protocol import GeminiServiceProtocol

from ..util.classes import SystemTranslationMessage, ModelTranslationMessage, ChatCompletion, NOT_GIVEN, gemini_service, GenerationConfig, GenerateContentResponse
from ..util.attributes import VALID_JSON_GEMINI_MODELS as VALID_SYSTEM_MESSAGE_MODELS, _sync_logging_decorator

##-------------------start-of-attributes---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_gemini_default_evaluation_instructions = "Please suggest a revised of the given text given it's original text and it's translation."

##-------------------start-of-_gemini_redefine_client()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
def _gemini_redefine_client(service:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                        ) -> None:

    """

    Redefines the Gemini client and generation config. This should be called before making any requests to the Gemini service, or after changing any of the service's settings.

    """

    response_mime_type = "application/json" if service._json_mode else "text/plain"
    
    gen_model_params = {
        "model_name": service._model,
        "safety_settings": service._safety_settings,
        "system_instruction": service._system_message if service._model in VALID_SYSTEM_MESSAGE_MODELS else None
    }
    
    service._client = genai.GenerativeModel(**gen_model_params)
    
    generation_config_params = {
        "candidate_count": service._candidate_count,
        "stop_sequences": service._stop_sequences,
        "max_output_tokens": service._max_output_tokens,
        "temperature": service._temperature,
        "top_p": service._top_p,
        "top_k": service._top_k,
        "response_mime_type": response_mime_type,
        "response_schema": service._response_schema if service._response_schema and service._json_mode else None
    }
    
    service._generation_config = GenerationConfig(**generation_config_params)
    
    service._semaphore = asyncio.Semaphore(service._semaphore_value)

##-------------------start-of-_gemini_redefine_client_decorator()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
def _gemini_redefine_client_decorator(func:typing.Callable,
                                service:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                                ) -> typing.Callable:

    """

    Wraps a function to redefine the Gemini client before doing anything that requires the client.

    Parameters:
    func (callable) : The function to wrap.

    Returns:
    wrapper (callable) : The wrapped function.

    """

    def wrapper(*args, **kwargs):
        service._redefine_client() 
        return func(*args, **kwargs)
    
    return wrapper

##-------------------start-of-_gemini_evaluate_translation()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
@_gemini_redefine_client_decorator
@_sync_logging_decorator
def _gemini_evaluate_translation(text_to_translate:str,
                    service:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                    ) -> GenerateContentResponse:

    """

    Synchronously translates text.
    Instructions default to translating whatever text is input into English.

    Parameters:
    text_to_translate (string) : The text to translate.

    Returns:
    GenerateContentResponse : The translation.

    """

    if(service._decorator_to_use is None):
        return service.__evaluate_translation(text_to_translate)

    _decorated_function = service._decorator_to_use(service.__evaluate_translation)
    return _decorated_function(text_to_translate)

##-------------------start-of-_gemini_internal_evaluate_translation()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
def _gemini_internal_evaluate_translation(text_to_translate:str,
                                    service:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                                    ) -> GenerateContentResponse:

    """

    Synchronously translates text.

    Parameters:
    text_to_translate (string) : The text to translate.

    Returns:
    _response (GenerateContentResponse) : The translation.

    """

    text_request = f"{text_to_translate}" if service._model in VALID_SYSTEM_MESSAGE_MODELS else f"{service._system_message}\n{text_to_translate}"

    _response = service._client.generate_content(
        contents=text_request,
        generation_config=service._generation_config,
        safety_settings=service._safety_settings,
        stream=service._stream
    )
    
    return _response