## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing

## custom modules
from classes import NOT_GIVEN
from attributes import VALID_JSON_OPENAI_MODELS as ALLOWED_OPENAI_MODELS, VALID_JSON_GEMINI_MODELS as ALLOWED_GEMINI_MODELS, VALID_JSON_ANTHROPIC_MODELS as ALLOWED_ANTHROPIC_MODELS
from exceptions import InvalidEasyTLSettingsException

##-------------------start-of-_validate_elucidate_llm_translation_settings()--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def _validate_elucidate_llm_translation_settings(settings:dict, type:typing.Literal["gemini","openai", "anthropic"]) -> None:

    """

    Validates the incoming settings for Elucidate.

    Parameters:
    settings (dict) : The settings to validate.
    type (typing.Literal["gemini","openai"]) : The type of settings to validate.

    """

    ## Commented out keys are not used in the current version of Elucidate, but are kept.
    ## Stuff like stop, logit_bias, and n/candidate_count are not in use because there is simply no need for them in Elucidate.
    ## Stream may be used in the future, but is not used in the current version of Elucidate.
    ## They are typically hardcoded by Elucidate.

    ## The exception is openai_stop, and gemini_stop_sequences, which aren't validated here, rather in elucidate.py, but still used and given to the model.

    _openai_keys = [
        "openai_model",
        "openai_temperature",
        "openai_top_p",
      #  "openai_n",
    #    "openai_stream",
     #   "openai_stop",
      ##  "openai_logit_bias",
        "openai_max_tokens",
        "openai_presence_penalty",
        "openai_frequency_penalty"
    ]

    _gemini_keys = [
        "gemini_model",
        "gemini_temperature",
        "gemini_top_p",
        "gemini_top_k",
    ##    "gemini_candidate_count",
    ##    "gemini_stream",
  ##      "gemini_stop_sequences",
        "gemini_max_output_tokens"
    ]

    _anthropic_keys = [
        "anthropic_model",
        "anthropic_temperature",
        "anthropic_top_p",
        "anthropic_top_k",
    ##    "anthropic_stream",
    ##    "anthropic_stop_sequences",
        "anthropic_max_output_tokens"
    ]

    _validation_rules = {
        "openai_model": lambda x: isinstance(x, str) and x in ALLOWED_OPENAI_MODELS or x is None or x is NOT_GIVEN,
        "openai_temperature": lambda x: isinstance(x, (int, float)) and 0 <= x <= 2 or x is None or x is NOT_GIVEN,
        "openai_top_p": lambda x: isinstance(x, (int, float)) and 0 <= x <= 1 or x is None or x is NOT_GIVEN,
        "openai_max_tokens": lambda x: x is None or x is NOT_GIVEN or (isinstance(x, int) and x > 0),
        "openai_presence_penalty": lambda x: isinstance(x, (int, float)) and -2 <= x <= 2 or x is None or x is NOT_GIVEN,
        "openai_frequency_penalty": lambda x: isinstance(x, (int, float)) and -2 <= x <= 2 or x is None or x is NOT_GIVEN,
        "gemini_model": lambda x: isinstance(x, str) and x in ALLOWED_GEMINI_MODELS or x is None or x is NOT_GIVEN,
        "gemini_prompt": lambda x: x not in ["", "None", None, NOT_GIVEN],
        "gemini_temperature": lambda x: isinstance(x, (int, float)) and 0 <= x <= 2 or x is None or x is NOT_GIVEN,
        "gemini_top_p": lambda x: x is None or x is NOT_GIVEN or (isinstance(x, (int, float)) and 0 <= x <= 2),
        "gemini_top_k": lambda x: x is None or x is NOT_GIVEN or (isinstance(x, int) and x >= 0),
        "gemini_max_output_tokens": lambda x: x is None or x is NOT_GIVEN or isinstance(x, int),
        "anthropic_model": lambda x: isinstance(x, str) and x in ALLOWED_ANTHROPIC_MODELS or x is None or x is NOT_GIVEN,
        "anthropic_temperature": lambda x: isinstance(x, (int, float)) and 0 <= x <= 1 or x is None or x is NOT_GIVEN,
        "anthropic_top_p": lambda x: isinstance(x, (int, float)) and 0 <= x <= 1 or x is None or x is NOT_GIVEN,
        "anthropic_top_k": lambda x: isinstance(x, int) and x > 0 or x is None or x is NOT_GIVEN,
        "anthropic_max_output_tokens": lambda x: x is None or x is NOT_GIVEN or (isinstance(x, int) and x > 0)
    }
    
    try:

        ## assign to variables to reduce repetitive access    
        if(type == "openai"):

            ## ensure all keys are present
            assert all(_key in settings for _key in _openai_keys)

            ## validate each _key using the validation rules
            for _key, _validate in _validation_rules.items():
                if(_key in settings and not _validate(settings[_key])):
                    raise ValueError(f"Invalid _value for {_key}")
                
      ##      settings["openai_logit_bias"] = None
       ##     settings["openai_stream"] = False
   ##         settings["openai_n"] = 1

        elif(type == "gemini"):

            ## ensure all keys are present
            assert all(_key in settings for _key in _gemini_keys)

            ## _validate each _key using the validation rules
            for _key, _validate in _validation_rules.items():
                if (_key in settings and not _validate(settings[_key])):
                    raise ValueError(f"Invalid _value for {_key}")
                
        ##    settings["gemini_stream"] = False
      ##      settings["gemini_candidate_count"] = 1

        elif(type == "anthropic"):

            ## ensure all keys are present
            assert all(_key in settings for _key in _anthropic_keys)

            ## _validate each _key using the validation rules
            for _key, _validate in _validation_rules.items():
                if (_key in settings and not _validate(settings[_key])):
                    raise ValueError(f"Invalid _value for {_key}")
        
    except Exception as e:
        raise InvalidEasyTLSettingsException(f"Invalid settings, Due to: {str(e)}")