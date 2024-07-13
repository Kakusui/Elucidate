## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## custom modules 
from .util.classes import openai_service

from .evaluators.openai_evaluator import _default_evaluation_instructions, _evaluate_translation, internal_evaluate_translation, _build_evaluation_batches, _evaluate_translation_async, internal_evaluate_translation_async

def monkeystrap():

    ## monkeystrapping new sync functions to OpenAIService
    setattr(openai_service.OpenAIService, "_evaluate_translation", _evaluate_translation)
    setattr(openai_service.OpenAIService, "__evaluate_translation", internal_evaluate_translation)
    
    setattr(openai_service.OpenAIService, "_build_evaluation_batches", _build_evaluation_batches)

    ## monkeystrapping new async functions to OpenAIService
    setattr(openai_service.OpenAIService, "_evaluate_translation_async", _evaluate_translation_async)
    setattr(openai_service.OpenAIService, "__evaluate_translation_async", internal_evaluate_translation_async)

    ## monkeystrapping new attributes to OpenAIService
    setattr(openai_service.OpenAIService, "_default_evaluation_instructions", _default_evaluation_instructions)