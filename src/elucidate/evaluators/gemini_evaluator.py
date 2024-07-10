## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing

## custom modules
from ..protocols.gemini_service_protocol import GeminiServiceProtocol

from ..util.classes import SystemTranslationMessage, ModelTranslationMessage, ChatCompletion, NOT_GIVEN, openai_service
from ..util.attributes import VALID_JSON_OPENAI_MODELS, _sync_logging_decorator

##-------------------start-of-attributes---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_default_evaluation_instructions = "Please suggest a revised of the given text given it's original text and it's translation."
