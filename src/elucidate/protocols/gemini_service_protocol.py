## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in imports
import typing
import asyncio

## third-party imports
import google.generativeai as genai

## custom modules
from ..util.classes import GenerationConfig, GenerateContentResponse, AsyncGenerateContentResponse

class GeminiServiceProtocol(typing.Protocol):

    _default_evaluation_instructions:str = "Please suggest a revised of the given text given it's original text and it's translation."
    _default_model:str = "gemini-pro"

    _system_message = _default_evaluation_instructions

    _model:str = _default_model
    _temperature:float = 0.5
    _top_p:float = 0.9
    _top_k:int = 40
    _candidate_count:int = 1
    _stream:bool = False
    _stop_sequences:typing.List[str] | None = None
    _max_output_tokens:int | None = None

    _client:genai.GenerativeModel
    _generation_config:GenerationConfig

    _semaphore_value:int = 5
    _semaphore:asyncio.Semaphore = asyncio.Semaphore(_semaphore_value)

    _rate_limit_delay:float | None = None

    _decorator_to_use:typing.Union[typing.Callable, None] = None

    _log_directory:str | None = None

    ## Set to prevent any blockage of content
    _safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    _json_mode:bool = False
    _response_schema:typing.Mapping[str, typing.Any] | None = None
    
    @staticmethod
    def _redefine_client() -> None: ...

    @staticmethod
    def _evaluate_translation(text_to_evaluate:str
                        ) -> GenerateContentResponse: ...
    @staticmethod
    def __evaluate_translation(text_to_evaluate:str
                                    ) -> GenerateContentResponse: ...
    
    @staticmethod
    async def _evaluate_translation_async(text_to_evaluate:str
                                    ) -> AsyncGenerateContentResponse: ...
    
    @staticmethod
    async def __evaluate_translation_async(text_to_evaluate:str
                                    ) -> AsyncGenerateContentResponse: ...

    
    @staticmethod
    def _set_attributes(model:str="gemini-pro",
                        system_message:str | None = _default_evaluation_instructions,
                        temperature:float=0.5,
                        top_p:float=0.9,
                        top_k:int=40,
                        candidate_count:int=1,
                        stream:bool=False,
                        stop_sequences:typing.List[str] | None=None,
                        max_output_tokens:int | None=None,
                        decorator:typing.Union[typing.Callable, None]=None,
                        logging_directory:str | None=None,
                        semaphore:int | None=None,
                        rate_limit_delay:float | None=None,
                        json_mode:bool=False,
                        response_schema:typing.Mapping[str, typing.Any] | None = None
                        ) -> None: ...