## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing
import asyncio

## custom modules
from ..util.classes import SystemTranslationMessage, ModelTranslationMessage, ChatCompletion, NOT_GIVEN, NotGiven, Anthropic, AsyncAnthropic
from ..util.attributes import  _sync_logging_decorator, _async_logging_decorator

class OpenAIServiceProtocol(typing.Protocol):

    _default_model:str = "claude-3-haiku-20240307"
    _default_translation_instructions:str = "Please translate the following text into English."

    _system:str | None   = _default_translation_instructions 

    _model:str = _default_model
    _temperature:float | NotGiven = NOT_GIVEN
    _top_p:float | NotGiven = NOT_GIVEN
    _top_k:int | NotGiven = NOT_GIVEN
    _stream:typing.Literal[False] | NotGiven = False
    _stop_sequences:typing.List[str] | NotGiven = NOT_GIVEN
    _max_tokens:int | NotGiven = NOT_GIVEN

    _semaphore_value:int = 5
    _semaphore:asyncio.Semaphore = asyncio.Semaphore(_semaphore_value)

    _sync_client = Anthropic(api_key="DummyKey")
    _async_client = AsyncAnthropic(api_key="DummyKey")

    _rate_limit_delay:float | None = None

    _decorator_to_use:typing.Union[typing.Callable, None] = None

    _log_directory:str | None = None

    _json_mode:bool = False
    _response_schema:typing.Mapping[str, typing.Any] | None = None
    
    _json_tool = {
        "name": "format_to_json",
        "description": "Formats text into json. This is required.",
        "input_schema": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "The text you were given to translate"
                },
                "output": {
                    "type": "string",
                    "description": "The translated text"
                }
            },
            "required": ["input", "output"]
        }
    }