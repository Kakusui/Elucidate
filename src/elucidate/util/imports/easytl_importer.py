## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## third-party imports
from easytl.services import openai_service, gemini_service

from easytl.decorators import _sync_logging_decorator
from easytl.classes import SystemTranslationMessage, ModelTranslationMessage, ChatCompletion, NOT_GIVEN, NotGiven, GenerationConfig, GenerateContentResponse
from easytl.util.constants import VALID_JSON_OPENAI_MODELS, VALID_JSON_ANTHROPIC_MODELS, VALID_JSON_GEMINI_MODELS
from easytl.exceptions import InvalidResponseFormatException

from easytl.util.util import _is_iterable_of_strings
from easytl.util.llm_util import _validate_easytl_llm_translation_settings, _return_curated_gemini_settings, _return_curated_openai_settings, _validate_stop_sequences, _validate_response_schema,  _return_curated_anthropic_settings, _validate_text_length, _convert_to_correct_type 

from easytl.exceptions import InvalidResponseFormatException, InvalidTextInputException, EasyTLException