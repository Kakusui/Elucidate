## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing
import asyncio

## custom modules
from ..util.classes import SystemTranslationMessage, ModelTranslationMessage, ChatCompletion, NOT_GIVEN, NotGiven, OpenAI, AsyncOpenAI
from ..util.attributes import  _sync_logging_decorator, _async_logging_decorator

class OpenAIServiceProtocol(typing.Protocol):

    _default_translation_instructions:typing.ClassVar[SystemTranslationMessage]

    _default_evaluation_instructions:typing.ClassVar[SystemTranslationMessage] = SystemTranslationMessage("Please suggest a revised of the given text given it's original text and it's translation.")
    _system_message:typing.Optional[typing.Union[SystemTranslationMessage, str]] = _default_evaluation_instructions

    _log_directory:str | None = None

    _decorator_to_use: typing.Union[typing.Callable, None]

    _json_mode:bool

    _rate_limit_delay:float | None = None

    _default_model:str = "gpt-4"
    _model:str

    _sync_client:OpenAI
    _async_client:AsyncOpenAI

    _semaphore_value:int = 5
    _semaphore:asyncio.Semaphore = asyncio.Semaphore(_semaphore_value)


    @staticmethod
    def _build_evaluation_batches(text: typing.Union[str, typing.Iterable[str], ModelTranslationMessage, typing.Iterable[ModelTranslationMessage]],
                                instructions: typing.Optional[typing.Union[str, SystemTranslationMessage]] = None) -> typing.List[typing.Tuple[ModelTranslationMessage, SystemTranslationMessage]]: ...

    @staticmethod
    @_sync_logging_decorator
    def _evaluate_translation(evaluation_instructions:typing.Optional[SystemTranslationMessage],
                                evaluation_prompt:ModelTranslationMessage,
                                ) -> ChatCompletion: ...
    @staticmethod
    @_async_logging_decorator
    async def _evaluate_translation_async(evaluation_instructions:typing.Optional[SystemTranslationMessage],
                            evaluation_prompt:ModelTranslationMessage
                            ) -> ChatCompletion: ...

    @staticmethod
    def __evaluate_translation(instructions: SystemTranslationMessage, 
                               prompt: ModelTranslationMessage) -> ChatCompletion: ...
    
    @staticmethod
    async def __evaluate_translation_async(instructions: SystemTranslationMessage,
                                    prompt: ModelTranslationMessage) -> ChatCompletion: ...
    
    @staticmethod
    def _set_attributes(model:str = _default_model,
                        temperature:float | None | NotGiven = NOT_GIVEN,
                        logit_bias:typing.Dict[str, int] | None | NotGiven = NOT_GIVEN,
                        top_p:float | None | NotGiven = NOT_GIVEN,
                        n:int | None | NotGiven = 1,
                        stream:bool = False,
                        stop:typing.List[str] | None | NotGiven = NOT_GIVEN,
                        max_tokens:int | None | NotGiven = NOT_GIVEN,
                        presence_penalty:float | None | NotGiven = NOT_GIVEN,
                        frequency_penalty:float | None | NotGiven = NOT_GIVEN,
                        decorator:typing.Union[typing.Callable, None]=None,
                        logging_directory:str | None=None,
                        semaphore:int | None=None,
                        rate_limit_delay:float | None=None,
                        json_mode:bool=False
                        ) -> None: ...
