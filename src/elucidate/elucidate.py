## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import typing

## third-party libraries
import easytl.services.openai_service

## custom modules 
from .evaluators.openai_evaluator import test
from .evaluators.protocols import OpenAIServiceProtocol

## bootstrapping new functions to EasyTL
setattr(easytl.services.openai_service.OpenAIService, "test", test)

## finally importing EasyTL with modified OpenAIService
from easytl import EasyTL

class Elucidate:

    """
    
    Elucidate global client.

    """

##-------------------start-of-openai_self_eval()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def openai_self_eval(service: OpenAIServiceProtocol = typing.cast(OpenAIServiceProtocol, easytl.services.openai_service.OpenAIService)):

        """
        
        Allows you to use the modified OpenAIService with type hints.

        No need to subclass or deal with lack of typehints.

        """

        service.test()

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