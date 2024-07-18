## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing
import asyncio

## custom modules
from ..protocols.anthropic_service_protocol import AnthropicServiceProtocol

from ..util.attributes import VALID_JSON_ANTHROPIC_MODELS, _sync_logging_decorator, _async_logging_decorator

from ..util.classes import ModelTranslationMessage, AnthropicMessage, anthropic_service, NOT_GIVEN

##-------------------start-of-Attributes---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_openai_default_evaluation_instructions:str = "Please suggest a revised of the given text given it's original text and it's evaluation."

##-------------------start-of-_anthropic_build_evaluation_batches()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
def _anthropic_build_evaluation_batches(text:typing.Union[str, typing.Iterable[str], ModelTranslationMessage, typing.Iterable[ModelTranslationMessage]]) -> typing.List[ModelTranslationMessage]:
    
    """
    
    Builds the evaluation batches for the Anthropic service.

    Parameters:
    text (string | iterable[string] | ModelTranslationMessage | iterable[ModelTranslationMessage]) : The text to evaluate.

    Returns:
    translation_batches (list[ModelTranslationMessage]) : The evaluation batches to send to the Anthropic service.

    """

    
    if(isinstance(text, str)):
        
        text = [ModelTranslationMessage(content=text)]

    elif(isinstance(text, ModelTranslationMessage)):
        text = [text]
    
    elif(isinstance(text, typing.Iterable)):
        text = [ModelTranslationMessage(content=item) if isinstance(item, str) else item for item in text]
    else:
        raise ValueError("Invalid type for text. Must either be a string, ModelTranslationMessage, or an iterable of strings/ModelTranslationMessage.")
    
    if(any(not isinstance(item, ModelTranslationMessage) for item in text)):
        raise ValueError("Invalid type in iterable. Must be either strings or ModelTranslationMessage objects.")
    
    return text

##-------------------start-of-_anthropic_evaluate_text()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
@_sync_logging_decorator
def _anthropic_evaluate_translation(evaluation_instructions:typing.Optional[str],
                            evaluation_prompt: ModelTranslationMessage,
                            _protocol:AnthropicServiceProtocol = typing.cast(AnthropicServiceProtocol, anthropic_service.AnthropicService)
                            ) -> AnthropicMessage:
    
    """
    
    Synchronously evaluates the translation using the Anthropic API.

    Parameters:
    evaluation_instructions (str) : The instructions to use for the evaluation.
    evaluation_prompt (ModelTranslationMessage) : The text to evaluate.

    Returns:
    response (AnthropicMessage) : The response from the API.

    """
    
    if(evaluation_instructions is None):
        evaluation_instructions = _protocol._default_translation_instructions

    if(_protocol._decorator_to_use is None):
        return _protocol.__evaluate_translation(evaluation_instructions, evaluation_prompt)

    decorated_function = _protocol._decorator_to_use(_protocol.__evaluate_translation)
    return decorated_function(evaluation_instructions, evaluation_prompt)

##-------------------start-of-_anthropic_evaluate_translation_async()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
@_async_logging_decorator
async def _anthropic_evaluate_translation_async(evaluation_instructions: typing.Optional[str],
                            evaluation_prompt: ModelTranslationMessage,
                            _protocol:AnthropicServiceProtocol = typing.cast(AnthropicServiceProtocol, anthropic_service.AnthropicService)
                            ) -> AnthropicMessage:
    
    """

    Asynchronously evaluates the translation using the Anthropic API.

    Parameters:
    evaluation_instructions (str) : The instructions to use for the evaluation.
    evaluation_prompt (ModelTranslationMessage) : The text to evaluate.

    Returns:
    response (AnthropicMessage) : The response from the API.

    """
    
    if(evaluation_instructions is None):
        evaluation_instructions = _protocol._default_translation_instructions

    if(_protocol._decorator_to_use is None):
        return await _protocol.__evaluate_translation_async(evaluation_instructions, evaluation_prompt)
    
    decorated_function = _protocol._decorator_to_use(_protocol.__evaluate_translation_async)
    return await decorated_function(evaluation_instructions, evaluation_prompt)

##-------------------start-of-_internal_anthropic_evaluate_translation()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
def _internal_anthropic_evaluate_translation(instructions:str, prompt:ModelTranslationMessage,
                     _protocol:AnthropicServiceProtocol = typing.cast(AnthropicServiceProtocol, anthropic_service.AnthropicService)) -> AnthropicMessage:

    """

    Synchronously evaluates the translation using the Anthropic API.

    Parameters:
    instructions (str) : The instructions to use for the evaluation.
    prompt (ModelTranslationMessage) : The text to evaluate.

    Returns:
    response (AnthropicMessage) : The response from the API.

    """
    
    attributes = ["temperature", "top_p", "top_k", "stream", "stop_sequences", "max_tokens"]
    message_args = {
        "model": _protocol._model,
        "system": instructions,
        "messages": [prompt.to_dict()],
        ## scary looking dict comprehension to get the attributes that are not NOT_GIVEN
        **{attr: getattr(_protocol, f"_{attr}") for attr in attributes if getattr(_protocol, f"_{attr}") != NOT_GIVEN}
    }
    
    ## Special case for max_tokens
    message_args["max_tokens"] = message_args.get("max_tokens", 4096)
    
    if(_protocol._json_mode and _protocol._model in VALID_JSON_ANTHROPIC_MODELS):
        message_args.update({
            "tools": [_protocol._json_tool],
            "tool_choice": {"type": "tool", "name": "format_to_json"}
        })
    
    response = _protocol._sync_client.messages.create(**message_args)
    
    return response

##-------------------start-of-_internal_anthropic_evaluate_translation_async()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@staticmethod
async def _internal_anthropic_evaluate_translation_async(instructions:str, prompt:ModelTranslationMessage,
                                                         _protocol:AnthropicServiceProtocol = typing.cast(AnthropicServiceProtocol, anthropic_service.AnthropicService)) -> AnthropicMessage:

    """

    Asynchronously evaluates the translation using the Anthropic API.

    Parameters:
    instruction (str) : The instructions to use for the evaluation.
    prompt (ModelTranslationMessage) : The text to evaluate.

    Returns:
    response (AnthropicMessage) : The response from the API.

    """

    async with _protocol._semaphore:

        if(_protocol._rate_limit_delay is not None):
            await asyncio.sleep(_protocol._rate_limit_delay)

        attributes = ["temperature", "top_p", "top_k", "stream", "stop_sequences", "max_tokens"]
        message_args = {
            "model": _protocol._model,
            "system": instructions,
            "messages": [prompt.to_dict()],
            ## scary looking dict comprehension to get the attributes that are not NOT_GIVEN
            **{attr: getattr(_protocol, f"_{attr}") for attr in attributes if getattr(_protocol, f"_{attr}") != NOT_GIVEN}
        }
        
        ## Special case for max_tokens
        message_args["max_tokens"] = message_args.get("max_tokens", 4096)
        
        if(_protocol._json_mode and _protocol._model in VALID_JSON_ANTHROPIC_MODELS):
            message_args.update({
                "tools": [_protocol._json_tool],
                "tool_choice": {"type": "tool", "name": "format_to_json"}
            })

        response = await _protocol._async_client.messages.create(**message_args)

        return response