## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import logging
import typing

## custom modules 
from .protocols.openai_service_protocol import OpenAIServiceProtocol

from .util.classes import openai_service

from .monkeystrapper import monkeystrap

## monkeystrapping new functions to EasyTL
monkeystrap()

## finally importing EasyTL with modified classes
from easytl import EasyTL

from .util.classes import ModelTranslationMessage, SystemTranslationMessage, ChatCompletion, NOT_GIVEN, NotGiven
from .util.attributes import _validate_easytl_llm_translation_settings, _return_curated_openai_settings, _validate_stop_sequences, _validate_text_length

from .exceptions import InvalidResponseFormatException

class Elucidate:

    """
    
    Elucidate global client.

    """

##-------------------start-of-openai_evaluate()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def openai_evaluate(text:typing.Union[str, typing.Iterable[str], ModelTranslationMessage, typing.Iterable[ModelTranslationMessage]],
                        override_previous_settings:bool = True,
                        decorator:typing.Callable | None = None,
                        logging_directory:str | None = None,
                        response_type:typing.Literal["text", "raw", "json", "raw_json"] | None = "text",
                        evaluation_delay:float | None = None,
                        evaluation_instructions:str | SystemTranslationMessage | None = None,
                        model:str="gpt-4",
                        temperature:float | None | NotGiven = NOT_GIVEN,
                        top_p:float | None | NotGiven = NOT_GIVEN,
                        stop:typing.List[str] | None | NotGiven = NOT_GIVEN,
                        max_tokens:int | None | NotGiven = NOT_GIVEN,
                        presence_penalty:float | None | NotGiven = NOT_GIVEN,
                        frequency_penalty:float | None | NotGiven = NOT_GIVEN,
                        service:OpenAIServiceProtocol = typing.cast(OpenAIServiceProtocol, openai_service.OpenAIService)
                        ) -> typing.Union[typing.List[str], str, typing.List[ChatCompletion], ChatCompletion]:
        
        """

        Performs an evaluation on already translated text using the original untranslated text with OpenAI. Your text attribute should contain both.

        This function assumes that the API key has already been set.

        Evaluation instructions default to 'Please suggest a revised of the given text given it's original text and it's translation.' if not specified.

        Due to how OpenAI's API works, NOT_GIVEN is treated differently than None. If a parameter is set to NOT_GIVEN, it is not passed to the API. If it is set to None, it is passed to the API as None.
        
        This function is not for use for real-time evaluation, nor for generating multiple response candidates. Another function may be implemented for this given demand.

        Parameters:
        text (string or iterable) : The text to evaluate.  This should be the original untranslated text along with the translated text.
        override_previous_settings (bool) : Whether to override the previous settings that were used during the last call to an OpenAI evaluation function.
        decorator (callable or None) : The decorator to use when evaluating. Typically for exponential backoff retrying. If this is None, OpenAI will retry the request twice if it fails.
        logging_directory (string or None) : The directory to log to. If None, no logging is done. This'll append the text result and some function information to a file in the specified directory. File is created if it doesn't exist. Currently broken.
        response_type (literal["text", "raw", "json", "raw_json"]) : The type of response to return. 'text' returns the evaluated text, 'raw' returns the raw response, a ChatCompletion object, 'json' returns a json-parseable string. 'raw_json' returns the raw response, a ChatCompletion object, but with the content as a json-parseable string.
        evaluation_delay (float or None) : If text is an iterable, the delay between each evaluation. Default is none. This is more important for asynchronous evaluations where a semaphore alone may not be sufficient.
        evaluation_instructions (string or SystemTranslationMessage or None) : The evaluation instructions to use. If None, the default system message is used. If you plan on using the json response type, you must specify that you want a json output and it's format in the instructions. The default system message will ask for a generic json if the response type is json.
        model (string) : The model to use. (E.g. 'gpt-4', 'gpt-3.5-turbo-0125', 'gpt-4o', etc.)
        temperature (float) : The temperature to use. The higher the temperature, the more creative the output. Lower temperatures are typically better for translation and evaluation.
        top_p (float) : The nucleus sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        stop (list or None) : String sequences that will cause the model to stop evaluation if encountered, generally useless.
        max_tokens (int or None) : The maximum number of tokens to output.
        presence_penalty (float) : The presence penalty to use. This penalizes the model from repeating the same content in the output.
        frequency_penalty (float) : The frequency penalty to use. This penalizes the model from using the same words too frequently in the output.

        Returns:
        result (string or list - string or ChatCompletion or list - ChatCompletion) : The evaluation result. A list of strings if the input was an iterable, a string otherwise. A list of ChatCompletion objects if the response type is 'raw' and input was an iterable, a ChatCompletion object otherwise.

        """
        
        if(logging_directory is not None):
            logging.warning("Logging is currently broken. No logs will be written.")
        
        assert response_type in ["text", "raw", "json", "raw_json"], InvalidResponseFormatException("Invalid response type specified. Must be 'text', 'raw', 'json' or 'raw_json'.")
        
        _settings = _return_curated_openai_settings(locals())

        _validate_easytl_llm_translation_settings(_settings, "openai")

        _validate_stop_sequences(stop)

        _validate_text_length(text, model, service="openai")

        ## Should be done after validating the settings to reduce cost to the user
        EasyTL.test_credentials("openai")

        json_mode = True if response_type in ["json", "raw_json"] else False
        
        if(override_previous_settings == True):
            service._set_attributes(model=model,
                                        temperature=temperature,
                                        logit_bias=None,
                                        top_p=top_p,
                                        n=1,
                                        stop=stop,
                                        max_tokens=max_tokens,
                                        presence_penalty=presence_penalty,
                                        frequency_penalty=frequency_penalty,
                                        decorator=decorator,
                                        logging_directory=logging_directory,
                                        semaphore=None,
                                        rate_limit_delay=evaluation_delay,
                                        json_mode=json_mode)

            ## Done afterwards, cause default evaluation instructions can change based on set_attributes()
            evaluation_instructions = evaluation_instructions or service._default_evaluation_instructions
        
        else:
            evaluation_instructions = service._system_message

        translation_batches = service._build_evaluation_batches(text, evaluation_instructions)
        
        evaluations = []
        
        for _text, _translation_instructions in translation_batches:

            _result = service._evaluate_translation(_translation_instructions, _text)

            translation = _result if response_type in ["raw", "raw_json"] else _result.choices[0].message.content
            
            evaluations.append(translation)
        
        ## If originally a single text was provided, return a single translation instead of a list
        result = evaluations if isinstance(text, typing.Iterable) and not isinstance(text, str) else evaluations[0]
        
        return result

##-------------------start-of-set_credentials()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def set_credentials(api_type:typing.Literal["gemini", "openai", "anthropic"], credentials:typing.Union[str, None] = None) -> None:
        
        """

        Sets the credentials for the specified API type.

        Parameters:
        api_type (literal["gemini", "openai", "anthropic"]) : The API type to set the credentials for.
        credentials (string) : The credentials to set. This is an api key for the specified API type.

        """

        EasyTL.set_credentials(api_type, credentials)

##-------------------start-of-test_credentials()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def test_credentials(api_type:typing.Literal["gemini", "openai", "anthropic"]) -> typing.Tuple[bool, typing.Optional[Exception]]:
        
        """

        Tests the credentials for the specified API type.

        Parameters:
        api_type (literal["gemini", "openai", "anthropic"]) : The API type to test the credentials for.

        Returns:
        (bool) : Whether the credentials are valid.
        (Exception) : The exception that was raised, if any. None otherwise.

        """

        return EasyTL.test_credentials(api_type)
    
##-------------------start-of-calculate_cost()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def calculate_cost(text:str | typing.Iterable[str],
                       service:typing.Literal["gemini", "openai", "anthropic"],
                       model:typing.Optional[str] = None,
                       evaluation_instructions:typing.Optional[str] = None
                        ) -> typing.Tuple[int, float, str]:
        
        """

        Calculates the cost of evaluating the given text using the specified service.

        Parameters:
        text (string or iterable[string]) : The text to evaluate.
        service (literal["gemini", "openai", "anthropic"]) : The service to use for evaluation.
        model (string or None) : The model to use for evaluation. If None, the default model will be used.
        evaluation_instructions (string or None) : The instructions to use for evaluation. If None, the default instructions will be used.

        Returns:
        (int) : The number of tokens in the text.
        (float) : The cost of evaluating the text.
        (string) : The model used for evaluation.

        """

        return EasyTL.calculate_cost(text, service, model, evaluation_instructions)