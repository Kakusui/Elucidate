## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## custom modules 
from .util.classes import openai_service, gemini_service, anthropic_service

from .evaluators.openai_evaluator import _openai_default_evaluation_instructions, _openai_evaluate_translation, _openai_internal_evaluate_translation, _openai_build_evaluation_batches, _openai_evaluate_translation_async, _openai_internal_evaluate_translation_async

from .evaluators.gemini_evaluator import _gemini_default_evaluation_instructions, _gemini_redefine_client, _gemini_evaluate_translation, _gemini_internal_evaluate_translation, _gemini_evaluate_translation_async, _gemini_internal_evaluate_translation_async

from .evaluators.anthropic_evaluator import _anthropic_default_evaluation_instructions, _anthropic_build_evaluation_batches, _anthropic_evaluate_translation, _anthropic_internal_evaluate_translation, _anthropic_evaluate_translation_async, _anthropic_internal_evaluate_translation_async

##-------------------start-of-monkeystrap()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def monkeystrap():

    perform_openai_monkeystrapping()
    perform_gemini_monkeystrapping()
    perform_anthropic_monkeystrapping()

##-------------------start-of-perform_openai_monkeystrapping()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def perform_openai_monkeystrapping():

    ## monkeystrapping new sync functions to OpenAIService
    setattr(openai_service.OpenAIService, "_evaluate_translation", _openai_evaluate_translation)
    setattr(openai_service.OpenAIService, "__evaluate_translation", _openai_internal_evaluate_translation)
    
    setattr(openai_service.OpenAIService, "_build_evaluation_batches", _openai_build_evaluation_batches)

    ## monkeystrapping new async functions to OpenAIService
    setattr(openai_service.OpenAIService, "_evaluate_translation_async", _openai_evaluate_translation_async)
    setattr(openai_service.OpenAIService, "__evaluate_translation_async", _openai_internal_evaluate_translation_async)

    ## monkeystrapping new attributes to OpenAIService
    setattr(openai_service.OpenAIService, "_default_evaluation_instructions", _openai_default_evaluation_instructions)

##-------------------start-of-perform_gemini_monkeystrapping()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def perform_gemini_monkeystrapping():

    ## monkeystrapping new functions to GeminiServiceProtocol
    setattr(gemini_service.GeminiService, "_redefine_client", _gemini_redefine_client)
    setattr(gemini_service.GeminiService, "_evaluate_translation", _gemini_evaluate_translation)
    setattr(gemini_service.GeminiService, "__evaluate_translation", _gemini_internal_evaluate_translation)

    ## monkeystrapping new async functions to GeminiServiceProtocol
    setattr(gemini_service.GeminiService, "_evaluate_translation_async", _gemini_evaluate_translation_async)
    setattr(gemini_service.GeminiService, "__evaluate_translation_async", _gemini_internal_evaluate_translation_async)

    ## monkeystrapping new attributes to GeminiServiceProtocol
    setattr(gemini_service.GeminiService, "_default_evaluation_instructions", _gemini_default_evaluation_instructions)

##-------------------start-of-perform_anthropic_monkeystrapping()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def perform_anthropic_monkeystrapping():

    ## monkeystrapping new functions to AnthropicServiceProtocol
    setattr(anthropic_service.AnthropicService, "_evaluate_translation", _anthropic_evaluate_translation)
    setattr(anthropic_service.AnthropicService, "__evaluate_translation", _anthropic_internal_evaluate_translation)

    setattr(anthropic_service.AnthropicService, "_build_evaluation_batches", _anthropic_build_evaluation_batches)

    ## monkeystrapping new async functions to AnthropicServiceProtocol
    setattr(anthropic_service.AnthropicService, "_evaluate_translation_async", _anthropic_evaluate_translation_async)
    setattr(anthropic_service.AnthropicService, "__evaluate_translation_async", _anthropic_internal_evaluate_translation_async)

    ## monkeystrapping new attributes to AnthropicServiceProtocol
    setattr(anthropic_service.AnthropicService, "_default_evaluation_instructions", _anthropic_default_evaluation_instructions)