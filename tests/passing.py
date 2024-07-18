## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import asyncio
import os
import sys
import time
import logging

## third-party libraries
import backoff

from elucidate import Elucidate

from elucidate.exceptions import OpenAIError, GoogleAPIError, AnthropicAPIError

##-------------------start-of-read_api_key()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def read_api_key(filename):

    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except:
        pass

##-------------------start-of-setup_preconditions()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def setup_preconditions():

    openai_api_key = os.environ.get('OPENAI_API_KEY')
    gemini_api_key = os.environ.get('GEMINI_API_KEY')
    anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')

    ## the following will replace the keys with local test keys if the environment variables are not set (not a github actions environment)
    logging_directory = os.getenv('LOGGING_DIRECTORY', '/tmp/')

    if(openai_api_key is None):
        openai_api_key = read_api_key("tests/openai.txt")
        logging_directory = "tests/"

    if(gemini_api_key is None):
        gemini_api_key = read_api_key("tests/gemini.txt")

    if(anthropic_api_key is None):
        anthropic_api_key = read_api_key("tests/anthropic.txt")

    ## if any of these trigger, something is wrong (not in local test environment or github actions environment)
    assert openai_api_key is not None, "OPENAI_API_KEY environment variable must be set"
    assert gemini_api_key is not None, "GEMINI_API_KEY environment variable must be set"
    assert anthropic_api_key is not None, "ANTHROPIC_API_KEY environment variable must be set"

    ## set the credentials for the services
    Elucidate.set_credentials("openai", openai_api_key)
    Elucidate.set_credentials("gemini", gemini_api_key)
    Elucidate.set_credentials("anthropic", anthropic_api_key)

    return logging_directory

##-------------------start-of-main()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

async def main():

    logging_directory = setup_preconditions()

    ## probably self explanatory from this point on

    decorator = backoff.on_exception(backoff.expo, exception=(OpenAIError), logger=logging.getLogger())

    print("------------------------------------------------OpenAI------------------------------------------------")

    print("-----------------------------------------------Text response-----------------------------------------------")

    print(Elucidate.openai_evaluate("山村美紀の独白\nYamamura Miki's Monologue", model="gpt-3.5-turbo", evaluation_instructions="Please suggest a revised English translation based on the original Japanese text. Do not change if the translation is already correct.", decorator=decorator))

    print(await Elucidate.openai_evaluate_async("山村美紀の独白\nYamamura Miki's Monologue", model="gpt-3.5-turbo", evaluation_instructions="Please suggest a revised English translation based on the original Japanese text. Do not change if the translation is already correct.", decorator=decorator))

    print("-----------------------------------------------Gemini-----------------------------------------------")

    print("-----------------------------------------------Text response-----------------------------------------------")

    print(Elucidate.gemini_evaluate("山村美紀の独白\nYamamura Miki's Monologue", model="gemini-pro", evaluation_instructions="Please suggest a revised English translation based on the original Japanese text. Do not change if the translation is already correct.", decorator=decorator))

    print(await Elucidate.gemini_evaluate_async("山村美紀の独白\nYamamura Miki's Monologue", model="gemini-pro", evaluation_instructions="Please suggest a revised English translation based on the original Japanese text. Do not change if the translation is already correct.", decorator=decorator))

##-------------------end-of-main()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if(__name__ == "__main__"):
    ## setup logging
    logging.basicConfig(level=logging.DEBUG, 
                        filename='passing.log',
                        filemode='w', 
                        format='[%(asctime)s] [%(levelname)s] [%(filename)s] %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    asyncio.run(main())
