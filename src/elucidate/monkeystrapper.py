## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## third-party libraries
from easytl.services.openai_service import OpenAIService ## imported by Elucidate.py

import easytl.services.openai_service

## custom modules 
from .evaluators.openai_evaluator import _default_evaluation_instructions, _evaluate_translation, internal_evaluate_translation, _build_evaluation_batches

def monkeystrap():

    ## monkeystrapping new functions to OpenAIService
    setattr(easytl.services.openai_service.OpenAIService, "_evaluate_translation", _evaluate_translation)
    setattr(easytl.services.openai_service.OpenAIService, "__evaluate_translation", internal_evaluate_translation)
    setattr(easytl.services.openai_service.OpenAIService, "_build_evaluation_batches", _build_evaluation_batches)

    ## monkeystrapping new attributes to OpenAIService
    setattr(easytl.services.openai_service.OpenAIService, "_default_evaluation_instructions", _default_evaluation_instructions)