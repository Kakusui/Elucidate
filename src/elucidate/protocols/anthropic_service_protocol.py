## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing
import asyncio

## custom modules
from ..util.classes import NOT_GIVEN, NotGiven, Anthropic, AsyncAnthropic, ModelTranslationMessage, AnthropicMessage

class AnthropicServiceProtocol(typing.Protocol):

    _default_model:str = "claude-3-haiku-20240307"
    _default_evaluation_instructions:str = "Please suggest a revised of the given text given it's original text and it's translation."

    _system:str | None

    _model:str
    _temperature:float | NotGiven
    _top_p:float | NotGiven
    _top_k:int | NotGiven
    _stream:typing.Literal[False] | NotGiven
    _stop_sequences:typing.List[str] | NotGiven
    _max_tokens:int | NotGiven

    _semaphore_value:int
    _semaphore:asyncio.Semaphore

    _sync_client:Anthropic
    _async_client:AsyncAnthropic

    _rate_limit_delay:float | None

    _decorator_to_use:typing.Union[typing.Callable, None]

    _log_directory:str | None

    _json_mode:bool
    _response_schema:typing.Mapping[str, typing.Any] | None
    
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

    @staticmethod
    def _build_evaluation_batches(text: typing.Union[str, typing.Iterable[str], ModelTranslationMessage, typing.Iterable[ModelTranslationMessage]]) -> typing.List[ModelTranslationMessage]: ...
        
    @staticmethod
    def _evaluate_translation(evaluation_instructions:typing.Optional[str],
                                evaluation_prompt:ModelTranslationMessage,
                                ) -> AnthropicMessage: ...
    @staticmethod
    async def _evaluate_translation_async(evaluation_instructions:typing.Optional[str],
                            evaluation_prompt:ModelTranslationMessage
                            ) -> AnthropicMessage: ...

    @staticmethod
    def __evaluate_translation(instructions: str, 
                               prompt: ModelTranslationMessage) -> AnthropicMessage: ...
    
    @staticmethod
    async def __evaluate_translation_async(instructions:str,
                                    prompt:ModelTranslationMessage) -> AnthropicMessage: ...

    @staticmethod
    def _set_attributes(model:str = _default_model,
                        system:str | None = _default_evaluation_instructions,
                        temperature:float | NotGiven = NOT_GIVEN,
                        top_p:float | NotGiven = NOT_GIVEN,
                        top_k:int | NotGiven = NOT_GIVEN,
                        stream:typing.Literal[False] | NotGiven = False,
                        stop_sequences:typing.List[str] | NotGiven = NOT_GIVEN,
                        max_tokens:int | NotGiven = NOT_GIVEN,
                        decorator:typing.Union[typing.Callable, None]=None,
                        logging_directory:str | None=None,
                        semaphore:int | None=None,
                        rate_limit_delay:float | None=None,
                        json_mode:bool=False,
                        response_schema:typing.Mapping[str, typing.Any] | None = None
                        ) -> None: ...