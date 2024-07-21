## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

from .version import VERSION as __version__  # noqa

__author__ = "Kaden Bilyeu (Bikatr7) <Bikatr7@proton.me>"

## EasyTL things
from easytl import Message

from easytl import MODEL_COSTS, ALLOWED_GEMINI_MODELS, ALLOWED_OPENAI_MODELS, ALLOWED_ANTHROPIC_MODELS, VALID_JSON_OPENAI_MODELS, VALID_JSON_GEMINI_MODELS, VALID_JSON_ANTHROPIC_MODELS, MODEL_MAX_TOKENS

## google generic exception
from easytl import GoogleAPIError

## openai generic exception
from easytl import OpenAIError

## anthropic generic exception
from easytl import AnthropicError

## service specific exceptions
from easytl import OpenAIAPIError, OpenAIConflictError, OpenAINotFoundError, OpenAIAPIStatusError, OpenAIRateLimitError, OpenAIAPITimeoutError, OpenAIBadRequestError, OpenAIAPIConnectionError, OpenAIAuthenticationError, OpenAIInternalServerError, OpenAIPermissionDeniedError, OpenAIUnprocessableEntityError, OpenAIAPIResponseValidationError
from easytl import AnthropicAPIError, AnthropicConflictError, AnthropicNotFoundError, AnthropicAPIStatusError, AnthropicRateLimitError, AnthropicAPITimeoutError, AnthropicBadRequestError, AnthropicAPIConnectionError, AnthropicAuthenticationError, AnthropicInternalServerError, AnthropicPermissionDeniedError, AnthropicUnprocessableEntityError, AnthropicAPIResponseValidationError

## Elucidate things
from .elucidate import Elucidate

from .util.classes import SystemTranslationMessage, ModelTranslationMessage
from .util.classes import ChatCompletion
from .util.classes import GenerateContentResponse, AsyncGenerateContentResponse, GenerationConfig
from .util.classes import AnthropicMessage, AnthropicTextBlock, AnthropicToolUseBlock
from .util.classes import NOT_GIVEN, NotGiven

from .exceptions import ElucidateException, InvalidElucidateSettingsException

__all__ = [
    "Elucidate",
    "Message", "SystemTranslationMessage", "ModelTranslationMessage",
    "ChatCompletion",
    "GenerateContentResponse", "AsyncGenerateContentResponse", "GenerationConfig",
    "AnthropicMessage","AnthropicTextBlock", "AnthropicToolUseBlock",
    "NOT_GIVEN","NotGiven",
    "MODEL_COSTS", "ALLOWED_GEMINI_MODELS", "ALLOWED_OPENAI_MODELS", "ALLOWED_ANTHROPIC_MODELS", "VALID_JSON_OPENAI_MODELS", "VALID_JSON_GEMINI_MODELS", "VALID_JSON_ANTHROPIC_MODELS", "MODEL_MAX_TOKENS",
    "GoogleAPIError",
    "OpenAIError",
    "AnthropicError",
    "OpenAIAPIError", "OpenAIConflictError", "OpenAINotFoundError", "OpenAIAPIStatusError", "OpenAIRateLimitError", "OpenAIAPITimeoutError", "OpenAIBadRequestError", "OpenAIAPIConnectionError", "OpenAIAuthenticationError", "OpenAIInternalServerError", "OpenAIPermissionDeniedError", "OpenAIUnprocessableEntityError", "OpenAIAPIResponseValidationError",
    "AnthropicAPIError", "AnthropicConflictError", "AnthropicNotFoundError", "AnthropicAPIStatusError", "AnthropicRateLimitError", "AnthropicAPITimeoutError", "AnthropicBadRequestError", "AnthropicAPIConnectionError", "AnthropicAuthenticationError", "AnthropicInternalServerError", "AnthropicPermissionDeniedError", "AnthropicUnprocessableEntityError", "AnthropicAPIResponseValidationError",
    "ElucidateException", "InvalidElucidateSettingsException"
]