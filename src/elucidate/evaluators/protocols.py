## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing

## third-party imports
from easytl.classes import SystemTranslationMessage

from easytl.decorators import _sync_logging_decorator
from easytl.classes import SystemTranslationMessage, ModelTranslationMessage, ChatCompletion, NOT_GIVEN
from easytl.util.constants import VALID_JSON_OPENAI_MODELS

from openai import AsyncOpenAI, OpenAI

class OpenAIServiceProtocol(typing.Protocol):
    @staticmethod
    def test(test:str | None = None) -> None: ...
    @staticmethod
    def __evaluate_translation(instructions: SystemTranslationMessage, 
                               prompt: ModelTranslationMessage) -> ChatCompletion: ...

    _default_evaluation_instructions: typing.ClassVar[SystemTranslationMessage]
    _decorator_to_use: typing.Union[typing.Callable, None]
    _json_mode:bool

    _model:str

    _sync_client:OpenAI
    _async_client:AsyncOpenAI