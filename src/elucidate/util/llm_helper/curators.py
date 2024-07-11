## built-in libraries
import typing

## custom modules
from ..attributes import _convert_to_correct_type

##-------------------start-of-_return_curated_openai_settings()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def _return_curated_openai_settings(local_settings:dict[str, typing.Any]) -> dict:
        
        """
        
        Returns the curated OpenAI settings.

        What this does is it takes local_settings from the calling function, and then returns a dictionary with the settings that are relevant to OpenAI that were converted to the correct type.

        """

        _settings = {
        "openai_model": "",
        "openai_temperature": "",
        "openai_top_p": "",
        "openai_stop": "",
        "openai_max_tokens": "",
        "openai_presence_penalty": "",
        "openai_frequency_penalty": ""
        }

        _non_openai_params = ["text", "override_previous_settings", "decorator", "translation_instructions", "logging_directory", "response_type", "response_schema", "semaphore", "translation_delay", "use_pretranslated_text"]
        _custom_validation_params = ["openai_stop"]

        for _key in _settings.keys():
            param_name = _key.replace("openai_", "")
            if(param_name in local_settings and _key not in _non_openai_params and _key not in _custom_validation_params):
                _settings[_key] = _convert_to_correct_type(_key, local_settings[param_name])

        return _settings