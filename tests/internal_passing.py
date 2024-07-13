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

## custom modules

## Append the src directory to sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..')
src_path = os.path.abspath(os.path.join(parent_dir, 'src'))

sys.path.append(src_path)

## Now you can import Elucidate from elucidate.elucidate, no need to test from site-packages
from elucidate.elucidate import Elucidate

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

    ## the following will replace the keys with local test keys if the environment variables are not set (not a github actions environment)
    logging_directory = os.getenv('LOGGING_DIRECTORY', '/tmp/')

    if(openai_api_key is None):
        openai_api_key = read_api_key("tests/openai.txt")
        logging_directory = "tests/"

    ## if any of these trigger, something is wrong (not in local test environment or github actions environment)
    assert openai_api_key is not None, "OPENAI_API_KEY environment variable must be set"


    ## set the credentials for the services
    Elucidate.set_credentials("openai", openai_api_key)

    return logging_directory

##-------------------start-of-main()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

async def main():

    logging_directory = setup_preconditions()

    ## probably self explanatory from this point on

   ## decorator = backoff.on_exception(backoff.expo, exception=(DeepLException, GoogleAPIError, OpenAIError, AnthropicAPIError), logger=logging.getLogger())

    print("------------------------------------------------OpenAI------------------------------------------------")

    print("-----------------------------------------------Text response-----------------------------------------------")

    print(Elucidate.openai_evaluate("山村美紀の独白\nYamamura Miki's Monologue", model="gpt-3.5-turbo", evaluation_instructions="Please suggest a revised English translation based on the original Japanese text. Do not change if the translation is already correct.")) 

    print(await Elucidate.openai_evaluate_async("山村美紀の独白\nYamamura Miki's Monologue", model="gpt-3.5-turbo", evaluation_instructions="Please suggest a revised English translation based on the original Japanese text. Do not change if the translation is already correct.")) 

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
