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

from ..util.classes import SystemTranslationMessage, ModelTranslationMessage, ChatCompletion, NOT_GIVEN, gemini_service, GenerationConfig, GenerateContentResponse, AsyncGenerateContentResponse
from ..util.attributes import VALID_JSON_GEMINI_MODELS as VALID_SYSTEM_MESSAGE_MODELS, _sync_logging_decorator, _async_logging_decorator

##-------------------start-of-attributes---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_gemini_default_evaluation_instructions = "Please suggest a revised of the given text given it's original text and it's translation."

##-------------------start-of-_gemini_redefine_client()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
def _gemini_redefine_client(_protocol:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                        ) -> None:

    """

    Redefines the Gemini client and generation config. This should be called before making any requests to the Gemini service, or after changing any of the services's settings.

    """

    response_mime_type = "application/json" if _protocol._json_mode else "text/plain"
    
    gen_model_params = {
        "model_name": _protocol._model,
        "safety_settings": _protocol._safety_settings,
        "system_instruction": _protocol._system_message if _protocol._model in VALID_SYSTEM_MESSAGE_MODELS else None
    }
    
    _protocol._client = genai.GenerativeModel(**gen_model_params)
    
    generation_config_params = {
        "candidate_count": _protocol._candidate_count,
        "stop_sequences": _protocol._stop_sequences,
        "max_output_tokens": _protocol._max_output_tokens,
        "temperature": _protocol._temperature,
        "top_p": _protocol._top_p,
        "top_k": _protocol._top_k,
        "response_mime_type": response_mime_type,
        "response_schema": _protocol._response_schema if _protocol._response_schema and _protocol._json_mode else None
    }
    
    _protocol._generation_config = GenerationConfig(**generation_config_params)
    
    _protocol._semaphore = asyncio.Semaphore(_protocol._semaphore_value)

##-------------------start-of-_gemini_redefine_client_decorator()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
def _gemini_redefine_client_decorator(func:typing.Callable,
                                _protocol:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                                ) -> typing.Callable:

    """

    Wraps a function to redefine the Gemini client before doing anything that requires the client.

    Parameters:
    func (callable) : The function to wrap.

    Returns:
    wrapper (callable) : The wrapped function.

    """

    def wrapper(*args, **kwargs):
        _protocol._redefine_client() 
        return func(*args, **kwargs)
    
    return wrapper

##-------------------start-of-_gemini_evaluate_translation()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
@_gemini_redefine_client_decorator
@_sync_logging_decorator
def _gemini_evaluate_translation(text_to_evaluate:str,
                    _protocol:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                    ) -> GenerateContentResponse:

    """

    Synchronously evaluates the text using the Gemini API.
    Instructions default to evaluating the text in the context of the system message.

    Parameters:
    text_to_evaluate (string) : The text to evaluate.

    Returns:
    GenerateContentResponse : The response from the API.

    """

    if(_protocol._decorator_to_use is None):
        return _protocol.__evaluate_translation(text_to_evaluate)

    _decorated_function = _protocol._decorator_to_use(_protocol.__evaluate_translation)
    return _decorated_function(text_to_evaluate)

##-------------------start-of-_gemini_internal_evaluate_translation()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
def _gemini_internal_evaluate_translation(text_to_evaluate:str,
                                    _protocol:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                                    ) -> GenerateContentResponse:

    """

    Synchronously evaluates the text using the Gemini API.

    Parameters:
    text_to_evaluate (string) : The text to evaluate.

    Returns:
    _response (GenerateContentResponse) : The response from the API.

    """

    text_request = f"{text_to_evaluate}" if _protocol._model in VALID_SYSTEM_MESSAGE_MODELS else f"{_protocol._system_message}\n{text_to_evaluate}"

    _response = _protocol._client.generate_content(
        contents=text_request,
        generation_config=_protocol._generation_config,
        safety_settings=_protocol._safety_settings,
        stream=_protocol._stream
    )
    
    return _response

##-------------------start-of-_evaluate_text_async()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
@_gemini_redefine_client_decorator
@_async_logging_decorator
async def _gemini_evaluate_translation_async(text_to_evaluate:str,
                               _protocol:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                               ) -> AsyncGenerateContentResponse:

    """

    Asynchronously evaluates the text using the Gemini API.
    Instructions default to translating whatever text is input into English.

    Parameters:
    text_to_evaluate (string) : The text to evaluate.

    Returns:
    AsyncGenerateContentResponse : The evaluation.

    """

    if(_protocol._decorator_to_use is None):
        return await _protocol.__evaluate_translation_async(text_to_evaluate)

    _decorated_function = _protocol._decorator_to_use(_protocol.__evaluate_translation_async)
    return await _decorated_function(text_to_evaluate)

##-------------------start-of-__translate_message_async()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
async def _gemini_internal_evaluate_translation_async(text_to_evaluate:str,
                                _protocol:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                                 ) -> AsyncGenerateContentResponse:

    """

    Asynchronously evaluates the text using the Gemini API.

    Parameters:
    text_to_evaluate (string) : The text to evaluate.

    Returns:
    AsyncGenerateContentResponse : The evaluation.

    """

    async with _protocol._semaphore:

        if(_protocol._rate_limit_delay is not None):
            await asyncio.sleep(_protocol._rate_limit_delay)

        text_request = f"{text_to_evaluate}" if _protocol._model in VALID_SYSTEM_MESSAGE_MODELS else f"{_protocol._system_message}\n{text_to_evaluate}"

        _response = await _protocol._client.generate_content_async(
            contents=text_request,
            generation_config=_protocol._generation_config,
            safety_settings=_protocol._safety_settings,
            stream=_protocol._stream
        )
        
        return _response