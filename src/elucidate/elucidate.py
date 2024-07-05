## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import typing

## third-party libraries
import easytl.services.openai_service

## custom modules 
from .evaluators.openai_evaluator import test, _default_evaluation_instructions, _evaluate_translation, internal_evaluate_translation
from .evaluators.protocols import OpenAIServiceProtocol

## bootstrapping new functions to EasyTL
setattr(easytl.services.openai_service.OpenAIService, "test", test)

## bootstrapping new functions to OpenAIService
setattr(easytl.services.openai_service.OpenAIService, "_evaluate_translation", _evaluate_translation)
setattr(easytl.services.openai_service.OpenAIService, "__evaluate_translation", internal_evaluate_translation)

## bootstrapping new attributes to OpenAIService
setattr(easytl.services.openai_service.OpenAIService, "_default_evaluation_instructions", _default_evaluation_instructions)

## finally importing EasyTL with modified OpenAIService
from easytl import EasyTL

from easytl.classes import ModelTranslationMessage, SystemTranslationMessage, ChatCompletion, NOT_GIVEN, NotGiven

class Elucidate:

    """
    
    Elucidate global client.

    """

##-------------------start-of-test()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def test(service: OpenAIServiceProtocol = typing.cast(OpenAIServiceProtocol, easytl.services.openai_service.OpenAIService)):

        """
        
        Allows you to use the modified OpenAIService with type hints.

        No need to subclass or deal with lack of type hints.

        """

        service.test()

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
                        service:OpenAIServiceProtocol = typing.cast(OpenAIServiceProtocol, easytl.services.openai_service.OpenAIService)
                        ) -> typing.Union[typing.List[str], str, typing.List[ChatCompletion], ChatCompletion]:
        
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
        
        translations = []
        
        for _text, _translation_instructions in translation_batches:

            _result = service._evaluate_translation(_translation_instructions, _text)

            translation = _result if response_type in ["raw", "raw_json"] else _result.choices[0].message.content
            
            translations.append(translation)
        
        ## If originally a single text was provided, return a single translation instead of a list
        result = translations if isinstance(text, typing.Iterable) and not isinstance(text, str) else translations[0]
        
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