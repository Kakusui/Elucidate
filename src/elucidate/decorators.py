## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## One day this absolute disaster of a file will break and I will have to fix it. But today is not that day either.

## built-in libraries
from functools import wraps

import datetime
import os

## custom modules
from .util.classes import AnthropicTextBlock, AnthropicToolUseBlock, LDHelper

##-------------------start-of-get_nested_attribute()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def _get_nested_attribute(obj, attrs):
    for attr, type_hint in attrs:
        try:
            if(isinstance(obj, list) and attr.isdigit()):
                obj = obj[int(attr)]
            else:
                try:
                    if(type_hint is None or isinstance(obj, type_hint)):
                        obj = getattr(obj, attr)
                except AttributeError:
                    ## Try dictionary access
                    obj = obj[attr]

        except (AttributeError, IndexError, KeyError):
            raise ValueError(f"Attribute {attr} in object {obj} not found.")
        
    return str(obj)

##-------------------start-of-logging_decorator()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def _async_logging_decorator(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):

        directory, cls_name = LDHelper.get_logging_directory_attributes()

        if(directory is None):
            return await func(*args, **kwargs)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        filename = f"elucidate-log.txt"
        filepath = os.path.join(directory, filename)
        
        result = await func(*args, **kwargs)

        ## Get the attribute to log
        attr_to_logs = log_attributes.get(cls_name, None)
        if(attr_to_logs):
            log_data = []
            for attr_to_log in attr_to_logs:
                if(not isinstance(attr_to_log, list) and cls_name != 'OpenAIService'):
                    ## coerce to list
                    attr_to_log = [attr_to_log]
                if(not isinstance(result, str)):
                    log_data.append(_get_nested_attribute(result, attr_to_log))
            log_data = '\n'.join(log_data)
        
        ## did you know multi-line f-strings take leading spaces into account?
        log_data = f"""
{'=' * 40}
Function Call Details:
{'-' * 40}
Class Name: {cls_name}
Function Name: {func.__name__}
Arguments: {args}
Keyword Arguments: {kwargs}
{'-' * 40}
Result Details:
{'-' * 40}
Result: {log_data}
{'-' * 40}
Timestamp: {timestamp}
{'=' * 40}
        """
        
        with open(filepath, 'a+', encoding='utf-8') as file:
            file.write(log_data)
        
        return result
    
    return wrapper

def _sync_logging_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
            
        directory, cls_name = LDHelper.get_logging_directory_attributes() 

        if(directory is None):
            return func(*args, **kwargs)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        filename = f"elucidate-log.txt"
        filepath = os.path.join(directory, filename)
        
        result = func(*args, **kwargs)

        ## Get the attribute to log
        attr_to_logs = log_attributes.get(cls_name, None)
        if(attr_to_logs):
            log_data = []
            for attr_to_log in attr_to_logs:
                if(not isinstance(attr_to_log, list) and cls_name != 'OpenAIService'):
                    ## coerce to list
                    attr_to_log = [attr_to_log]
                if(not isinstance(result, str)):
                    log_data.append(_get_nested_attribute(result, attr_to_log))
            log_data = '\n'.join(log_data)
        
        ## did you know multi-line f-strings take leading spaces into account?
        log_data = f"""
{'=' * 40}
Function Call Details:
{'-' * 40}
Class Name: {cls_name}
Function Name: {func.__name__}
Arguments: {args}
Keyword Arguments: {kwargs}
{'-' * 40}
Result Details:
{'-' * 40}
Result: {log_data}
{'-' * 40}
Timestamp: {timestamp}
{'=' * 40}
        """
        
        with open(filepath, 'a+', encoding='utf-8') as file:
            file.write(log_data)
        
        return result
    
    return wrapper

## Since we're dealing with objects here...
log_attributes = {
    'GeminiService': [('text', None)],
    'DeepLService': [('text', None)],
    'OpenAIService': [[('choices', None), ('0', None), ('message', None), ('content', None)],
                      [('choices', None), ('0', None), ('message', None), ('content', None)],
                      ],
    'GoogleTLService': [('translatedText', None)],
    'AnthropicService': [
        [('content', None), ('0', None), ('text', AnthropicTextBlock)],
        [('content', None), ('0', None), ('input', AnthropicToolUseBlock)]
    ],
    'AzureService': [
        [('0', None), ('translations', None), ('0', None), ('text', None)]
    ]
}
