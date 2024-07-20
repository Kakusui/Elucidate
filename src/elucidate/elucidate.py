## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import typing
import asyncio

## custom modules 
from .protocols.openai_service_protocol import OpenAIServiceProtocol
from .protocols.gemini_service_protocol import GeminiServiceProtocol
from .protocols.anthropic_service_protocol import AnthropicServiceProtocol

from .util.classes import openai_service, gemini_service, anthropic_service

from .monkeystrapper import monkeystrap

## monkeystrapping new functions to EasyTL
monkeystrap()

## finally importing EasyTL with modified classes
from easytl import EasyTL

from .util.classes import ModelTranslationMessage, SystemTranslationMessage, ChatCompletion, NOT_GIVEN, NotGiven, GenerateContentResponse, AsyncGenerateContentResponse, AnthropicMessage, AnthropicTextBlock, AnthropicToolUseBlock
from .util.attributes import _return_curated_openai_settings, _validate_stop_sequences, _validate_text_length, _is_iterable_of_strings, _validate_response_schema, _return_curated_gemini_settings, _return_curated_anthropic_settings
from .util.llm_helper.validators import _validate_elucidate_llm_translation_settings

from .exceptions import InvalidResponseFormatException, InvalidTextInputException, ElucidateException, InvalidAPITypeException

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
                        _protocol:OpenAIServiceProtocol = typing.cast(OpenAIServiceProtocol, openai_service.OpenAIService)
                        ) -> typing.Union[typing.List[str], str, typing.List[ChatCompletion], ChatCompletion]:
        
        """

        Performs an evaluation on already translated text using the original untranslated text with OpenAI. Your text attribute should contain both.

        This function assumes that the API key has already been set.

        Evaluation instructions default to 'Please suggest a revised of the given text given it's original text and it's evaluation.' if not specified.

        Due to how OpenAI's API works, NOT_GIVEN is treated differently than None. If a parameter is set to NOT_GIVEN, it is not passed to the API. If it is set to None, it is passed to the API as None.
        
        This function is not for use for real-time evaluation, nor for generating multiple response candidates. Another function may be implemented for this given demand.

        Parameters:
        text (string | ModelTranslationMessage | iterable[str] | iterable[ModelTranslationMessage]) : The text to evaluate.  This should be the original untranslated text along with the translated text.
        override_previous_settings (bool) : Whether to override the previous settings that were used during the last call to an OpenAI evaluation function.
        decorator (callable or None) : The decorator to use when evaluating. Typically for exponential backoff retrying. If this is None, OpenAI will retry the request twice if it fails.
        logging_directory (string or None) : The directory to log to. If None, no logging is done. This'll append the text result and some function information to a file in the specified directory. File is created if it doesn't exist.
        response_type (literal["text", "raw", "json", "raw_json"]) : The type of response to return. 'text' returns the evaluated text, 'raw' returns the raw response, a ChatCompletion object, 'json' returns a json-parseable string. 'raw_json' returns the raw response, a ChatCompletion object, but with the content as a json-parseable string.
        evaluation_delay (float or None) : If text is an iterable, the delay between each evaluation. Default is none. This is more important for asynchronous evaluations where a semaphore alone may not be sufficient.
        evaluation_instructions (string or SystemTranslationMessage or None) : The evaluation instructions to use. If None, the default system message is used. If you plan on using the json response type, you must specify that you want a json output and it's format in the instructions. The default system message will ask for a generic json if the response type is json.
        model (string) : The model to use. (E.g. 'gpt-4', 'gpt-3.5-turbo-0125', 'gpt-4o', etc.)
        temperature (float) : The temperature to use. The higher the temperature, the more creative the output. Lower temperatures are typically better for evaluation and evaluation.
        top_p (float) : The nucleus sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        stop (list or None) : String sequences that will cause the model to stop evaluation if encountered, generally useless.
        max_tokens (int or None) : The maximum number of tokens to output.
        presence_penalty (float) : The presence penalty to use. This penalizes the model from repeating the same content in the output.
        frequency_penalty (float) : The frequency penalty to use. This penalizes the model from using the same words too frequently in the output.

        Returns:
        result (string or list - string or ChatCompletion or list - ChatCompletion) : The evaluation result. A list of strings if the input was an iterable, a string otherwise. A list of ChatCompletion objects if the response type is 'raw' and input was an iterable, a ChatCompletion object otherwise.

        """
        
        assert response_type in ["text", "raw", "json", "raw_json"], InvalidResponseFormatException("Invalid response type specified. Must be 'text', 'raw', 'json' or 'raw_json'.")
        
        _settings = _return_curated_openai_settings(locals())

        _validate_elucidate_llm_translation_settings(_settings, "openai")

        _validate_stop_sequences(stop)

        _validate_text_length(text, model, service="openai")

        ## Should be done after validating the settings to reduce cost to the user
        EasyTL.test_credentials("openai")

        json_mode = True if response_type in ["json", "raw_json"] else False
        
        if(override_previous_settings == True):
            _protocol._set_attributes(model=model,
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
            evaluation_instructions = evaluation_instructions or _protocol._default_evaluation_instructions
        
        else:
            evaluation_instructions = _protocol._system_message

        assert isinstance(text, str) or _is_iterable_of_strings(text) or isinstance(text, ModelTranslationMessage) or _is_iterable_of_strings(text), InvalidTextInputException("text must be a string, an iterable of strings, a ModelTranslationMessage or an iterable of ModelTranslationMessages.")

        evaluation_batches = _protocol._build_evaluation_batches(text, evaluation_instructions)
        
        evaluations = []
        
        for _text, _evaluation_instructions in evaluation_batches:

            _result = _protocol._evaluate_translation(_evaluation_instructions, _text)

            evaluation = _result if response_type in ["raw", "raw_json"] else _result.choices[0].message.content
            
            evaluations.append(evaluation)
        
        ## If originally a single text was provided, return a single evaluation instead of a list
        result = evaluations if isinstance(text, typing.Iterable) and not isinstance(text, str) else evaluations[0]
        
        return result
    
##-------------------start-of-openai_evaluate_async()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    async def openai_evaluate_async(text:typing.Union[str, typing.Iterable[str], ModelTranslationMessage, typing.Iterable[ModelTranslationMessage]],
                        override_previous_settings:bool = True,
                        decorator:typing.Callable | None = None,
                        logging_directory:str | None = None,
                        response_type:typing.Literal["text", "raw", "json", "raw_json"] | None = "text",
                        semaphore:int | None = 5,
                        evaluation_delay:float | None = None,
                        evaluation_instructions:str | SystemTranslationMessage | None = None,
                        model:str="gpt-4",
                        temperature:float | None | NotGiven = NOT_GIVEN,
                        top_p:float | None | NotGiven = NOT_GIVEN,
                        stop:typing.List[str] | None | NotGiven = NOT_GIVEN,
                        max_tokens:int | None | NotGiven = NOT_GIVEN,
                        presence_penalty:float | None | NotGiven = NOT_GIVEN,
                        frequency_penalty:float | None | NotGiven = NOT_GIVEN,
                        _protocol:OpenAIServiceProtocol = typing.cast(OpenAIServiceProtocol, openai_service.OpenAIService)
                        ) -> typing.Union[typing.List[str], str, typing.List[ChatCompletion], ChatCompletion]:
        
        """

        Asynchronous version of openai_evaluate(). 
        Will generally be faster for iterables. Order is preserved.

        Performs an evaluation on already translated text using the original untranslated text with OpenAI. Your text attribute should contain both.

        This function assumes that the API key has already been set.

        Evaluation instructions default to 'Please suggest a revised of the given text given it's original text and it's evaluation.' if not specified.

        Due to how OpenAI's API works, NOT_GIVEN is treated differently than None. If a parameter is set to NOT_GIVEN, it is not passed to the API. If it is set to None, it is passed to the API as None.
        
        This function is not for use for real-time evaluation, nor for generating multiple response candidates. Another function may be implemented for this given demand.

        Parameters:
        text (string | ModelTranslationMessage | iterable[str] | iterable[ModelTranslationMessage]) : The text to evaluate.  This should be the original untranslated text along with the translated text.        override_previous_settings (bool) : Whether to override the previous settings that were used during the last call to an OpenAI evaluation function.
        override_previous_settings (bool) : Whether to override the previous settings that were used during the last call to an OpenAI evaluation function.
        decorator (callable or None) : The decorator to use when evaluating. Typically for exponential backoff retrying. If this is None, OpenAI will retry the request twice if it fails.
        logging_directory (string or None) : The directory to log to. If None, no logging is done. This'll append the text result and some function information to a file in the specified directory. File is created if it doesn't exist.
        response_type (literal["text", "raw", "json", "raw_json"]) : The type of response to return. 'text' returns the evaluated text, 'raw' returns the raw response, a ChatCompletion object, 'json' returns a json-parseable string. 'raw_json' returns the raw response, a ChatCompletion object, but with the content as a json-parseable string.
        semaphore (int) : The number of concurrent requests to make. Default is 5.
        evaluation_delay (float or None) : If text is an iterable, the delay between each evaluation. Default is none. This is more important for asynchronous evaluations where a semaphore alone may not be sufficient.
        evaluation_instructions (string or SystemTranslationMessage or None) : The evaluation instructions to use. If None, the default system message is used. If you plan on using the json response type, you must specify that you want a json output and it's format in the instructions. The default system message will ask for a generic json if the response type is json.
        model (string) : The model to use. (E.g. 'gpt-4', 'gpt-3.5-turbo-0125', 'gpt-4o', etc.)
        temperature (float) : The temperature to use. The higher the temperature, the more creative the output. Lower temperatures are typically better for evaluation and evaluation.
        top_p (float) : The nucleus sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        stop (list or None) : String sequences that will cause the model to stop evaluation if encountered, generally useless.
        max_tokens (int or None) : The maximum number of tokens to output.
        presence_penalty (float) : The presence penalty to use. This penalizes the model from repeating the same content in the output.
        frequency_penalty (float) : The frequency penalty to use. This penalizes the model from using the same words too frequently in the output.

        Returns:
        result (string or list - string or ChatCompletion or list - ChatCompletion) : The evaluation result. A list of strings if the input was an iterable, a string otherwise. A list of ChatCompletion objects if the response type is 'raw' and input was an iterable, a ChatCompletion object otherwise.

        """
                
        assert response_type in ["text", "raw", "json", "raw_json"], InvalidResponseFormatException("Invalid response type specified. Must be 'text', 'raw', 'json' or 'raw_json'.")
        
        _settings = _return_curated_openai_settings(locals())

        _validate_elucidate_llm_translation_settings(_settings, "openai")

        _validate_stop_sequences(stop)

        _validate_text_length(text, model, service="openai")

        ## Should be done after validating the settings to reduce cost to the user
        EasyTL.test_credentials("openai")

        json_mode = True if response_type in ["json", "raw_json"] else False
        
        if(override_previous_settings == True):
            _protocol._set_attributes(model=model,
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
                                        semaphore=semaphore,
                                        rate_limit_delay=evaluation_delay,
                                        json_mode=json_mode)

            ## Done afterwards, cause default evaluation instructions can change based on set_attributes()
            evaluation_instructions = evaluation_instructions or _protocol._default_evaluation_instructions
        
        else:
            evaluation_instructions = _protocol._system_message

        assert isinstance(text, str) or _is_iterable_of_strings(text) or isinstance(text, ModelTranslationMessage) or _is_iterable_of_strings(text), InvalidTextInputException("text must be a string, an iterable of strings, a ModelTranslationMessage or an iterable of ModelTranslationMessages.")

        _evaluation_batches = _protocol._build_evaluation_batches(text, evaluation_instructions)

        _evaluation_tasks = []

        for _text, _evaluation_instructions in _evaluation_batches:
            _task = _protocol._evaluate_translation_async(_evaluation_instructions, _text)
            _evaluation_tasks.append(_task)

        _results = await asyncio.gather(*_evaluation_tasks)

        _results:typing.List[ChatCompletion] = _results

        assert all([hasattr(_r, "choices") for _r in _results]), ElucidateException("Malformed response received. Please try again.")

        evaluation = _results if response_type in ["raw","raw_json"] else [result.choices[0].message.content for result in _results if result.choices[0].message.content is not None]

        result = evaluation if isinstance(text, typing.Iterable) and not isinstance(text, str) else evaluation[0]

        return result
    
##-------------------start-of-gemini_evaluate()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def gemini_evaluate(text:typing.Union[str, typing.Iterable[str]],
                        override_previous_settings:bool = True,
                        decorator:typing.Callable | None = None,
                        logging_directory:str | None = None,
                        response_type:typing.Literal["text", "raw", "json", "raw_json"] | None = "text",
                        response_schema:str | typing.Mapping[str, typing.Any] | None = None,
                        evaluation_delay:float | None = None,
                        evaluation_instructions:str | None = None,
                        model:str="gemini-pro",
                        temperature:float=0.5,
                        top_p:float=0.9,
                        top_k:int=40,
                        stop_sequences:typing.List[str] | None=None,
                        max_output_tokens:int | None=None,
                        _protocol:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                        ) -> typing.Union[typing.List[str], str, GenerateContentResponse, typing.List[GenerateContentResponse]]:
        
        """

        Performs an evaluation on already translated text using the original untranslated text with Gemini. Your text attribute should contain both.

        This function assumes that the API key has already been set.

        Evaluation instructions default to 'Please suggest a revised of the given text given it's original text and it's evaluation.' if not specified.
        
        This function is not for use for real-time evaluation, nor for generating multiple response candidates. Another function may be implemented for this given demand.

        Parameters:
        text (string | iterable[str]) : The text to evaluate.  This should be the original untranslated text along with the translated text.
        override_previous_settings (bool) : Whether to override the previous settings that were used during the last call to a Gemini evaluation function.
        decorator (callable or None) : The decorator to use when evaluating. Typically for exponential backoff retrying. If this is None, Gemini will retry the request twice if it fails.
        logging_directory (string or None) : The directory to log to. If None, no logging is done. This'll append the text result and some function information to a file in the specified directory. File is created if it doesn't exist.
        response_type (literal["text", "raw", "json", "raw_json"]) : The type of response to return. 'text' returns the evaluated text, 'raw' returns the raw response, a GenerateContentResponse object, 'json' returns a json-parseable string. 'raw_json' returns the raw response, a GenerateContentResponse object, but with the content as a json-parseable string.
        response_schema (string or mapping or None) : The schema to use for the response. If None, no schema is used. This is only used if the response type is 'json' or 'json_raw'. Elucidate only validates the schema to the extend that it is None or a valid json. It does not validate the contents of the json.4
        evaluation_delay (float or None) : If text is an iterable, the delay between each evaluation. Default is none. This is more important for asynchronous evaluations where a semaphore alone may not be sufficient.
        evaluation_instructions (string or None) : The evaluation instructions to use. If None, the default system message is used. If you plan on using the json response type, you must specify that you want a json output and it's format in the instructions. The default system message will ask for a generic json if the response type is json.
        model (string) : The model to use. (E.g. 'gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash', etc.)
        temperature (float) : The temperature to use. The higher the temperature, the more creative the output. Lower temperatures are typically better for evaluation and evaluation.
        top_p (float) : The nucleus sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        top_k (int) : The top k sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        stop_sequences (list or None) : String sequences that will cause the model to stop evaluation if encountered, generally useless.
        max_output_tokens (int or None) : The maximum number of tokens to output.

        Returns:
        result (string or list - string or GenerateContentResponse or list - GenerateContentResponse) : The evaluation result. A list of strings if the input was an iterable, a string otherwise. A list of GenerateContentResponse objects if the response type is 'raw' and input was an iterable, a GenerateContentResponse object otherwise.

        """

        assert response_type in ["text", "raw", "json", "raw_json"], InvalidResponseFormatException("Invalid response type specified. Must be 'text', 'raw', 'json' or 'raw_json'.")

        _settings = _return_curated_gemini_settings(locals())

        _validate_elucidate_llm_translation_settings(_settings, "gemini")

        _validate_stop_sequences(stop_sequences)

        _validate_text_length(text, model, service="gemini")

        response_schema = _validate_response_schema(response_schema)

        ## Should be done after validating the settings to reduce cost to the user
        EasyTL.test_credentials("gemini")

        json_mode = True if response_type in ["json", "raw_json"] else False

        if(override_previous_settings == True):
            _protocol._set_attributes(model=model,
                                          system_message=evaluation_instructions,
                                          temperature=temperature,
                                          top_p=top_p,
                                          top_k=top_k,
                                          candidate_count=1,
                                          stream=False,
                                          stop_sequences=stop_sequences,
                                          max_output_tokens=max_output_tokens,
                                          decorator=decorator,
                                          logging_directory=logging_directory,
                                          semaphore=None,
                                          rate_limit_delay=evaluation_delay,
                                          json_mode=json_mode,
                                          response_schema=response_schema)
            
            ## Done afterwards, cause default evaluation instructions can change based on set_attributes()       
            _protocol._system_message = evaluation_instructions or _protocol._default_evaluation_instructions
        
        if(isinstance(text, str)):
            _result = _protocol._evaluate_translation(text)
            
            assert not isinstance(_result, list) and hasattr(_result, "text"), ElucidateException("Malformed response received. Please try again.")
            
            result = _result if response_type in ["raw", "raw_json"] else _result.text

        elif(_is_iterable_of_strings(text)):
            
            _results = [_protocol._evaluate_translation(_text) for _text in text]

            assert isinstance(_results, list) and all([hasattr(_r, "text") for _r in _results]), ElucidateException("Malformed response received. Please try again.")

            result = [_r.text for _r in _results] if response_type in ["text","json"] else _results # type: ignore
            
        else:
            raise InvalidTextInputException("text must be a string or an iterable of strings.")
        
        return result
    
##-------------------start-of-gemini_evaluate_async()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    async def gemini_evaluate_async(text:typing.Union[str, typing.Iterable[str]],
                                    override_previous_settings:bool = True,
                                    decorator:typing.Callable | None = None,
                                    logging_directory:str | None = None,
                                    response_type:typing.Literal["text", "raw", "json", "raw_json"] | None = "text",
                                    response_schema:str | typing.Mapping[str, typing.Any] | None = None,
                                    semaphore:int | None = 5,
                                    evaluation_delay:float | None = None,
                                    evaluation_instructions:str | None = None,
                                    model:str="gemini-pro",
                                    temperature:float=0.5,
                                    top_p:float=0.9,
                                    top_k:int=40,
                                    stop_sequences:typing.List[str] | None=None,
                                    max_output_tokens:int | None=None,
                                    _protocol:GeminiServiceProtocol = typing.cast(GeminiServiceProtocol, gemini_service.GeminiService)
                                    ) -> typing.Union[typing.List[str], str, AsyncGenerateContentResponse, typing.List[AsyncGenerateContentResponse]]:
        
        """

        Asynchronous version of gemini_evaluate().
        Will generally be faster for iterables. Order is preserved.

        Performs an evaluation on already translated text using the original untranslated text with Gemini. Your text attribute should contain both.

        This function assumes that the API key has already been set.

        Evaluation instructions default to 'Please suggest a revised of the given text given it's original text and it's evaluation.' if not specified.

        This function is not for use for real-time evaluation, nor for generating multiple response candidates. Another function may be implemented for this given demand.

        Parameters:
        text (string | iterable[str]) : The text to evaluate.  This should be the original untranslated text along with the translated text.
        override_previous_settings (bool) : Whether to override the previous settings that were used during the last call to a Gemini evaluation function.
        decorator (callable or None) : The decorator to use when evaluating. Typically for exponential backoff retrying. If this is None, Gemini will retry the request twice if it fails.
        logging_directory (string or None) : The directory to log to. If None, no logging is done. This'll append the text result and some function information to a file in the specified directory. File is created if it doesn't exist.
        response_type (literal["text", "raw", "json", "raw_json"]) : The type of response to return. 'text' returns the evaluated text, 'raw' returns the raw response, a GenerateContentResponse object, 'json' returns a json-parseable string. 'raw_json' returns the raw response, a GenerateContentResponse object, but with the content as a json-parseable string.
        response_schema (string or mapping or None) : The schema to use for the response. If None, no schema is used. This is only used if the response type is 'json' or 'json_raw'. Elucidate only validates the schema to the extend that it is None or a valid json.4
        semaphore (int) : The number of concurrent requests to make. Default is 5.
        evaluation_delay (float or None) : If text is an iterable, the delay between each evaluation. Default is none. This is more important for asynchronous evaluations where a semaphore alone may not be sufficient.
        evaluation_instructions (string or None) : The evaluation instructions to use. If None, the default system message is used. If you plan on using the json response type, you must specify that you want a json output and it's format in the instructions. The default system message will ask for a generic json if the response type is json.
        model (string) : The model to use. (E.g. 'gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash', etc.)
        temperature (float) : The temperature to use. The higher the temperature, the more creative the output. Lower temperatures are typically better for evaluation and evaluation.
        top_p (float) : The nucleus sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        top_k (int) : The top k sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        stop_sequences (list or None) : String sequences that will cause the model to stop evaluation if encountered, generally useless.
        max_output_tokens (int or None) : The maximum number of tokens to output.

        Returns:
        result (string or list - string or GenerateContentResponse or list - GenerateContentResponse) : The evaluation result. A list of strings if the input was an iterable, a string otherwise. A list of GenerateContentResponse objects if the response type is 'raw' and input was an iterable, a GenerateContentResponse object otherwise.

        """

        assert response_type in ["text", "raw", "json", "raw_json"], InvalidResponseFormatException("Invalid response type specified. Must be 'text', 'raw', 'json' or 'raw_json'.")

        _settings = _return_curated_gemini_settings(locals())

        _validate_elucidate_llm_translation_settings(_settings, "gemini")

        _validate_stop_sequences(stop_sequences)

        _validate_text_length(text, model, service="gemini")

        response_schema = _validate_response_schema(response_schema)

        ## Should be done after validating the settings to reduce cost to the user
        EasyTL.test_credentials("gemini")

        json_mode = True if response_type in ["json", "raw_json"] else False

        if(override_previous_settings == True):
            _protocol._set_attributes(model=model,
                                          system_message=evaluation_instructions,
                                          temperature=temperature,
                                          top_p=top_p,
                                          top_k=top_k,
                                          candidate_count=1,
                                          stream=False,
                                          stop_sequences=stop_sequences,
                                          max_output_tokens=max_output_tokens,
                                          decorator=decorator,
                                          logging_directory=logging_directory,
                                          semaphore=semaphore,
                                          rate_limit_delay=evaluation_delay,
                                          json_mode=json_mode,
                                          response_schema=response_schema)
            
            ## Done afterwards, cause default evaluation instructions can change based on set_attributes()
            _protocol._system_message = evaluation_instructions or _protocol._default_evaluation_instructions
            
        if(isinstance(text, str)):
            _result = await _protocol._evaluate_translation_async(text)

            result = _result if response_type in ["raw", "raw_json"] else _result.text
            
        elif(_is_iterable_of_strings(text)):
            _tasks = [_protocol._evaluate_translation_async(_text) for _text in text]
            _results = await asyncio.gather(*_tasks)

            result = [_r.text for _r in _results] if response_type in ["text","json"] else _results # type: ignore

        else:
            raise InvalidTextInputException("text must be a string or an iterable of strings.")
        
        return result

##-------------------start-of-anthropic_evaluate()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------    

    @staticmethod
    def anthropic_evaluate(text:typing.Union[str, typing.Iterable[str], ModelTranslationMessage, typing.Iterable[ModelTranslationMessage]],
                            override_previous_settings:bool = True,
                            decorator:typing.Callable | None = None,
                            logging_directory:str | None = None,
                            response_type:typing.Literal["text", "raw", "json", "raw_json"] | None = "text",
                            response_schema:str | typing.Mapping[str, typing.Any] | None = None,
                            evaluation_delay:float | None = None,
                            evaluation_instructions:str | None = None,
                            model:str="claude-3-haiku-20240307",
                            temperature:float | NotGiven = NOT_GIVEN,
                            top_p:float | NotGiven = NOT_GIVEN,
                            top_k:int | NotGiven = NOT_GIVEN,
                            stop_sequences:typing.List[str] | NotGiven = NOT_GIVEN,
                            max_output_tokens:int | NotGiven = NOT_GIVEN,
                            _protocol:AnthropicServiceProtocol = typing.cast(AnthropicServiceProtocol, anthropic_service.AnthropicService)
                            ) -> typing.Union[typing.List[str], str, AnthropicMessage, typing.List[AnthropicMessage]]:
        
        """
        
        Performs an evaluation on already translated text using the original untranslated text with Anthropic. Your text attribute should contain both.

        This function assumes that the API key has already been set.

        Evaluation instructions default to 'Please suggest a revised of the given text given it's original text and it's evaluation.' if not specified.

        This function is not for use for real-time evaluation, nor for generating multiple response candidates. Another function may be implemented for this given demand.

        Parameters:
        text (string | ModelTranslationMessage | iterable[str] | iterable[ModelTranslationMessage]) : The text to evaluate.  This should be the original untranslated text along with the translated text.
        override_previous_settings (bool) : Whether to override the previous settings that were used during the last call to an Anthropic evaluation function.
        decorator (callable or None) : The decorator to use when evaluating. Typically for exponential backoff retrying. If this is None, Anthropic will retry the request twice if it fails.
        logging_directory (string or None) : The directory to log to. If None, no logging is done. This'll append the text result and some function information to a file in the specified directory. File is created if it doesn't exist.
        response_type (literal["text", "raw", "json", "raw_json"]) : The type of response to return. 'text' returns the evaluated text, 'raw' returns the raw response, a AnthropicMessage object, 'json' returns a json-parseable string. 'raw_json' returns the raw response, a AnthropicMessage object, but with the content as a json-parseable string.
        response_schema (string or mapping or None) : The schema to use for the response. If None, no schema is used. This is only used if the response type is 'json' or 'json_raw'. Elucidate only validates the schema to the extend that it is None or a valid json.
        evaluation_delay (float or None) : If text is an iterable, the delay between each evaluation. Default is none. This is more important for asynchronous evaluations where a semaphore alone may not be sufficient.
        evaluation_instructions (string or None) : The evaluation instructions to use. If None, the default system message is used. If you plan on using the json response type, you must specify that you want a json output and it's format in the instructions. The default system message will ask for a generic json if the response type is json.
        model (string) : The model to use. (E.g. 'claude-3-haiku-20240307', 'claude-3-haiku-20240307', 'claude-3-haiku-20240307', etc.)
        temperature (float) : The temperature to use. The higher the temperature, the more creative the output. Lower temperatures are typically better for evaluation and evaluation.
        top_p (float) : The nucleus sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        top_k (int) : The top k sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        stop_sequences (list or None) : String sequences that will cause the model to stop evaluation if encountered, generally useless.
        max_output_tokens (int or None) : The maximum number of tokens to output.
        
        Returns:
        result (string or list - string or AnthropicMessage or list - AnthropicMessage) : The evaluation result. A list of strings if the input was an iterable, a string otherwise. A list of AnthropicMessage objects if the response type is 'raw' and input was an iterable, a AnthropicMessage object otherwise.

        """

        assert response_type in ["text", "raw", "json", "raw_json"], InvalidResponseFormatException("Invalid response type specified. Must be 'text', 'raw', 'json' or 'raw_json'.")

        _settings = _return_curated_anthropic_settings(locals())

        _validate_elucidate_llm_translation_settings(_settings, "anthropic")

        _validate_stop_sequences(stop_sequences)

        _validate_text_length(text, model, service="anthropic")

        response_schema = _validate_response_schema(response_schema)

        ## Should be done after validating the settings to reduce cost to the user
        EasyTL.test_credentials("anthropic")

        json_mode = True if response_type in ["json", "raw_json"] else False

        if(override_previous_settings == True):
            _protocol._set_attributes(model=model,
                                            system=evaluation_instructions,
                                            temperature=temperature,
                                            top_p=top_p,
                                            top_k=top_k,
                                            stop_sequences=stop_sequences,
                                            stream=False,
                                            max_tokens=max_output_tokens,
                                            decorator=decorator,
                                            logging_directory=logging_directory,
                                            semaphore=None,
                                            rate_limit_delay=evaluation_delay,
                                            json_mode=json_mode,
                                            response_schema=response_schema)
            
            ## Done afterwards, cause default evaluation instructions can change based on set_attributes()
            _protocol._system = evaluation_instructions or _protocol._default_evaluation_instructions

        assert isinstance(text, str) or _is_iterable_of_strings(text) or isinstance(text, ModelTranslationMessage) or _is_iterable_of_strings(text), InvalidTextInputException("text must be a string, an iterable of strings, a ModelTranslationMessage or an iterable of ModelTranslationMessages.")

        _evaluation_batches = _protocol._build_evaluation_batches(text)

        _evaluation = []

        for _text in _evaluation_batches:

            _result = _protocol._evaluate_translation(_protocol._system, _text)

            assert not isinstance(_result, list) and hasattr(_result, "content"), ElucidateException("Malformed response received. Please try again.")

            if(response_type in ["raw", "raw_json"]):
                evaluation = _result

            ## response structure can vary if tools are used
            else:
                content = _result.content

                if(isinstance(content[0], AnthropicTextBlock)):
                    evaluation = content[0].text

                elif(isinstance(content[0], AnthropicToolUseBlock)):
                    evaluation = content[0].input
                            
            _evaluation.append(evaluation)

        ## If originally a single text was provided, return a single evaluation instead of a list
        result = _evaluation if isinstance(text, typing.Iterable) and not isinstance(text, str) else _evaluation[0]

        return result
    
##-------------------start-of-anthropic_evaluate_async()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    async def anthropic_evaluate_async(text:typing.Union[str, typing.Iterable[str], ModelTranslationMessage, typing.Iterable[ModelTranslationMessage]],
                                        override_previous_settings:bool = True,
                                        decorator:typing.Callable | None = None,
                                        logging_directory:str | None = None,
                                        response_type:typing.Literal["text", "raw", "json", "raw_json"] | None = "text",
                                        response_schema:str | typing.Mapping[str, typing.Any] | None = None,
                                        semaphore:int | None = 5,
                                        evaluation_delay:float | None = None,
                                        evaluation_instructions:str | None = None,
                                        model:str="claude-3-haiku-20240307",
                                        temperature:float | NotGiven = NOT_GIVEN,
                                        top_p:float | NotGiven = NOT_GIVEN,
                                        top_k:int | NotGiven = NOT_GIVEN,
                                        stop_sequences:typing.List[str] | NotGiven = NOT_GIVEN,
                                        max_output_tokens:int | NotGiven = NOT_GIVEN,
                                        _protocol:AnthropicServiceProtocol = typing.cast(AnthropicServiceProtocol, anthropic_service.AnthropicService)
                                        ) -> typing.Union[typing.List[str], str, AnthropicMessage, typing.List[AnthropicMessage]]:
        """

        Asynchronous version of anthropic_evaluate().
        Will generally be faster for iterables. Order is preserved.

        Performs an evaluation on already translated text using the original untranslated text with Anthropic. Your text attribute should contain both.

        This function assumes that the API key has already been set.

        Evaluation instructions default to 'Please suggest a revised of the given text given it's original text and it's evaluation.' if not specified.

        This function is not for use for real-time evaluation, nor for generating multiple response candidates. Another function may be implemented for this given demand.

        Parameters:
        text (string | ModelTranslationMessage | iterable[str] | iterable[ModelTranslationMessage]) : The text to evaluate.  This should be the original untranslated text along with the translated text.
        override_previous_settings (bool) : Whether to override the previous settings that were used during the last call to an Anthropic evaluation function.
        decorator (callable or None) : The decorator to use when evaluating. Typically for exponential backoff retrying. If this is None, Anthropic will retry the request twice if it fails.
        logging_directory (string or None) : The directory to log to. If None, no logging is done. This'll append the text result and some function information to a file in the specified directory. File is created if it doesn't exist.
        response_type (literal["text", "raw", "json", "raw_json"]) : The type of response to return. 'text' returns the evaluated text, 'raw' returns the raw response, a AnthropicMessage object, 'json' returns a json-parseable string. 'raw_json' returns the raw response, a AnthropicMessage object, but with the content as a json-parseable string.
        response_schema (string or mapping or None) : The schema to use for the response. If None, no schema is used. This is only used if the response type is 'json' or 'json_raw'. Elucidate only validates the schema to the extend that it is None or a valid json.
        semaphore (int) : The number of concurrent requests to make. Default is 5.
        evaluation_delay (float or None) : If text is an iterable, the delay between each evaluation. Default is none. This is more important for asynchronous evaluations where a semaphore alone may not be sufficient.
        evaluation_instructions (string or None) : The evaluation instructions to use. If None, the default system message is used. If you plan on using the json response type, you must specify that you want a json output and it's format in the instructions. The default system message will ask for a generic json if the response type is json.
        model (string) : The model to use. (E.g. 'claude-3-haiku-20240307', 'claude-3-haiku-20240307', 'claude-3-haiku-20240307', etc.)
        temperature (float) : The temperature to use. The higher the temperature, the more creative the output. Lower temperatures are typically better for evaluation and evaluation.
        top_p (float) : The nucleus sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        top_k (int) : The top k sampling probability. The higher the value, the more words are considered for the next token. Generally, alter this or temperature, not both.
        stop_sequences (list or None) : String sequences that will cause the model to stop evaluation if encountered, generally useless.
        max_output_tokens (int or None) : The maximum number of tokens to output.
        
        Returns:
        result (string or list - string or AnthropicMessage or list - AnthropicMessage) : The evaluation result. A list of strings if the input was an iterable, a string otherwise. A list of AnthropicMessage objects if the response type is 'raw' and input was an iterable, a AnthropicMessage object otherwise.

        """

        assert response_type in ["text", "raw", "json", "raw_json"], InvalidResponseFormatException("Invalid response type specified. Must be 'text', 'raw', 'json' or 'raw_json'.")

        _settings = _return_curated_anthropic_settings(locals())

        _validate_elucidate_llm_translation_settings(_settings, "anthropic")

        _validate_stop_sequences(stop_sequences)

        _validate_text_length(text, model, service="anthropic")

        response_schema = _validate_response_schema(response_schema)

        ## Should be done after validating the settings to reduce cost to the user
        EasyTL.test_credentials("anthropic")

        json_mode = True if response_type in ["json", "raw_json"] else False

        if(override_previous_settings == True):
            _protocol._set_attributes(model=model,
                                            system=evaluation_instructions,
                                            temperature=temperature,
                                            top_p=top_p,
                                            top_k=top_k,
                                            stop_sequences=stop_sequences,
                                            stream=False,
                                            max_tokens=max_output_tokens,
                                            decorator=decorator,
                                            logging_directory=logging_directory,
                                            semaphore=semaphore,
                                            rate_limit_delay=evaluation_delay,
                                            json_mode=json_mode,
                                            response_schema=response_schema)
            
            ## Done afterwards, cause default evaluation instructions can change based on set_attributes()
            _protocol._system = evaluation_instructions or _protocol._default_evaluation_instructions
        
        assert isinstance(text, str) or _is_iterable_of_strings(text) or isinstance(text, ModelTranslationMessage) or _is_iterable_of_strings(text), InvalidTextInputException("text must be a string, an iterable of strings, a ModelTranslationMessage or an iterable of ModelTranslationMessages.")

        _evaluation_batches = _protocol._build_evaluation_batches(text)

        _evaluation_tasks = []

        for _text in _evaluation_batches:
            _task = _protocol._evaluate_translation_async(_protocol._system, _text)
            _evaluation_tasks.append(_task)

        _results = await asyncio.gather(*_evaluation_tasks)

        _results:typing.List[AnthropicMessage] = _results

        assert all([hasattr(_r, "content") for _r in _results]), ElucidateException("Malformed response received. Please try again.")

        if(response_type in ["raw", "raw_json"]):
            evaluation = _results

        else:
            evaluation = [result.content[0].input if isinstance(result.content[0], AnthropicToolUseBlock) else result.content[0].text for result in _results]
        
        result = evaluation if isinstance(text, typing.Iterable) and not isinstance(text, str) else evaluation[0]

        return result # type: ignore
    
##-------------------start-of-evaluate()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    @staticmethod
    def evaluate(text:str | typing.Iterable[str] | ModelTranslationMessage | typing.Iterable[ModelTranslationMessage],
                  service:typing.Optional[typing.Literal["openai", "gemini", "anthropic"]],
                  **kwargs) -> typing.Union[typing.List[str], str, 
                                            typing.List[ChatCompletion], ChatCompletion,
                                            typing.List[GenerateContentResponse], GenerateContentResponse,
                                            typing.List[AnthropicMessage], AnthropicMessage]:
        
        """

        Evaluates the given text using the specified service. Your text attribute should contain both the original untranslated text and the translated text.

        Please see the documentation for the specific evaluation function for the service you want to use.

        OpenAI: openai_evaluate()
        Gemini: gemini_evaluate()
        Anthropic: anthropic_evaluate()

        All functions can return a list of strings or a string, depending on the input. The response type can be specified to return the raw response instead:
        OpenAI: ChatCompletion
        Gemini: GenerateContentResponse
        Anthropic: AnthropicMessage
        
        Parameters:
        text (str | ModelTranslationMessage | typing.Iterable[str] | typing.Iterable[ModelTranslationMessage]) : The text to evaluate. This should be the original untranslated text along with the translated text.
        service (string) : The service to use for evaluation.
        **kwargs : The keyword arguments to pass to the evaluation function.

        Returns:
        result (See Function Signature) : The evaluation result.

        """

        assert service in ["openai", "gemini", "anthropic"], InvalidAPITypeException("Invalid service specified. Must be 'openai', 'gemini' or 'anthropic'.")

        if(service == "openai"):
            return Elucidate.openai_evaluate(text, **kwargs)
        
        elif(service == "gemini"):
            return Elucidate.gemini_evaluate(text, **kwargs) # type: ignore
        
        elif(service == "anthropic"):
            return Elucidate.anthropic_evaluate(text, **kwargs)
        
##-------------------start-of-translate_async()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @staticmethod
    async def evaluate_async(text:str | typing.Iterable[str] | ModelTranslationMessage | typing.Iterable[ModelTranslationMessage],
                              service:typing.Optional[typing.Literal["openai", "gemini", "anthropic"]],
                              **kwargs) -> typing.Union[typing.List[str], str, 
                                                        typing.List[ChatCompletion], ChatCompletion,
                                                        typing.List[AsyncGenerateContentResponse], AsyncGenerateContentResponse,
                                                        typing.List[AnthropicMessage], AnthropicMessage]:

        
        """

        Asynchronous version of evaluate().
        Will generally be faster for iterables. Order is preserved.
        
        Evaluates the given text using the specified service. Your text attribute should contain both the original untranslated text and the translated text.

        Please see the documentation for the specific evaluation function for the service you want to use.

        OpenAI: openai_evaluate_async()
        Gemini: gemini_evaluate_async()
        Anthropic: anthropic_evaluate_async()

        All functions can return a list of strings or a string, depending on the input. The response type can be specified to return the raw response instead:
        OpenAI: ChatCompletion
        Gemini: AsyncGenerateContentResponse
        Anthropic: AnthropicMessage

        Parameters:
        text (str | ModelTranslationMessage | typing.Iterable[str] | typing.Iterable[ModelTranslationMessage]) : The text to evaluate. This should be the original untranslated text along with the translated text.
        service (string) : The service to use for evaluation.
        **kwargs : The keyword arguments to pass to the evaluation function.

        Returns:
        result (See function signature) : The evaluation result.

        """

        assert service in ["openai", "gemini", "anthropic"], InvalidAPITypeException("Invalid service specified. Must be 'openai', 'gemini' or 'anthropic'.")

        if(service == "openai"):
            return await Elucidate.openai_evaluate_async(text, **kwargs)
        
        elif(service == "gemini"):
            return await Elucidate.gemini_evaluate_async(text, **kwargs) # type: ignore
        
        elif(service == "anthropic"):
            return await Elucidate.anthropic_evaluate_async(text, **kwargs)

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