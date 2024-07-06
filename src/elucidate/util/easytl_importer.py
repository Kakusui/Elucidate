## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## third-party imports
from easytl.services import openai_service

from easytl.decorators import _sync_logging_decorator
from easytl.classes import SystemTranslationMessage, ModelTranslationMessage, ChatCompletion, NOT_GIVEN, NotGiven
from easytl.util.constants import VALID_JSON_OPENAI_MODELS

from openai import AsyncOpenAI, OpenAI