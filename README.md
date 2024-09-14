---------------------------------------------------------------------------------------------------------------------------------------------------
**Table of Contents**

- [**Notes**](#notes)
- [**Quick Start**](#quick-start)
- [**Installation**](#installation)
- [**Features**](#features)
- [**API Usage**](#api-usage)
  - [Evaluating Text](#evaluating-text)
  - [Generic Translation Methods](#generic-translation-methods)
  - [Cost Calculation](#cost-calculation)
  - [Credentials Management](#credentials-management)
- [**License**](#license)
- [**Contribution**](#contribution)

--------------------------------------------------------------------------------------------------------------------------------------------------

## **Notes**<a name="notes"></a>

Smarter Translations through LLM Self-Evaluation

Elucidate has a [Trello board](https://trello.com/b/uOmiU7by/elucidate) for tracking planned features and issues:

---------------------------------------------------------------------------------------------------------------------------------------------------
## **Quick Start**<a name="quick-start"></a>

To get started with Elucidate, install the package via pip:

```bash
pip install elucidate
```

Then, you can evaluate text using by importing the global client.

For example, with OpenAI:

```python
from easytl import Elucidate

## Set your API key
Elucidate.set_credentials("openai", "YOUR_API_KEY")

## You can also validate your API keys; evaluation functions will do this automatically
is_valid, e = Elucidate.test_credentials("openai")

evaluated_text = Elucidate.openai_evaluate("山村美紀の独白\nYamamura Miki's Speech", model="gpt-4o-mini", evaluation_instructions="Please suggest a revised English translation based on the original Japanese text. Do not change if the translation is already correct.")

print(evaluated_text) ## Output: "Yamamura Miki's Monologue"

if(__name__ == "__main__"):
    asyncio.run(main())

```

---------------------------------------------------------------------------------------------------------------------------------------------------

## **Installation**<a name="installation"></a>

Python 3.10+

Elucidate can be installed using pip:

```bash
pip install elucidate
```

This will install Elucidate along with its dependencies and requirements.

These are the dependencies/requirements that will be installed:
```bash
setuptools>=61.0
wheel
setuptools_scm>=6.0
tomli
easytl>=0.4.10
```
---------------------------------------------------------------------------------------------------------------------------------------------------

## **Features**<a name="features"></a>

Elucidate offers seamless integration with several APIs, allowing users to easily switch between services based on their needs. Key features include:

- Support for multiple APIs including OpenAI, Gemini, and Anthropic.
- Simple API key and credential management and validation.
- Cost estimation tools to help manage usage based on text length, evaluation instructions for LLMs, and evaluation services.
- Highly customizable evaluation options, with each API's original features and more. 
- Lots of optional arguments for additional functionality. Such as decorators, semaphores, and rate-limit delays.

---------------------------------------------------------------------------------------------------------------------------------------------------

## **API Usage**<a name="api-usage"></a>

### Evaluating Text

`openai_evaluate`, `gemini_evaluate`, and `anthropic_evaluate` are LLM functions.

Each method accepts various parameters to customize the evaluation process, such as language, text format, and API-specific features like formality level or temperature. However these vary wildly between services, so it is recommended to check the documentation for each service for more information.

All services offer asynchronous evaluation methods that return a future object for concurrent processing. These methods are suffixed with `_async` and can be awaited to retrieve the evaluated text.

Instead of receiving the evaluated text directly, you can also use the `response_type` parameter to get the raw response object, specify a json response where available, or both.
  
  `text` - Default. Returns the evaluated text.

  `json` - Returns the response as a JSON object. Not all services support this.

  `raw` - Returns the raw response object from the API. This can be useful for accessing additional information or debugging.
  
  `raw_json` - Returns the raw response object with the text but with the response also a json object. Again, not all services support this.

### Generic Translation Methods

Elucidate has generic evaluation methods `evaluate` and `evaluate_async` that can be used to evaluation text with any of the supported services. These methods accept the text, service, and kwargs of the respective service as parameters.

### Cost Calculation

The `calculate_cost` method provides an estimate of the cost associated with evaluating a given text with specified settings for each supported service.

```python
num_tokens, cost, model = Elucidate.calculate_cost("This has a lot of tokens.", "openai", model="gpt-4", evaluation_instructions="Translate this text to Japanese.")
```

### Credentials Management

Credentials can be set and validated using `set_credentials` and `test_credentials` methods to ensure they are active and correct before submitting evaluation requests.

If you don't provide an api key, the package will attempt to read it from the environment variables. The format for this is as follows:

```python

# This is a dictionary mapping the service names to their respective environment variables.
environment_map = 
{
  ## Gemini evaluation service
  "gemini": "GEMINI_API_KEY",
  
  ## OpenAI evaluation service
  "openai": "OPENAI_API_KEY",
  
  ## Anthropic evaluation service
  "anthropic": "ANTHROPIC_API_KEY",
}

```

---------------------------------------------------------------------------------------------------------------------------------------------------

## **License**<a name="license"></a>

This project, Elucidate, is licensed under the GNU Lesser General Public License v2.1 (LGPLv2.1) - see the LICENSE file for complete details.

The LGPL is a permissive copyleft license that enables this software to be freely used, modified, and distributed. It is particularly designed for libraries, allowing them to be included in both open source and proprietary software. When using or modifying Elucidate, you can choose to release your work under the LGPLv2.1 to contribute back to the community or incorporate it into proprietary software as per the license's permissions.

---------------------------------------------------------------------------------------------------------------------------------------------------

## **Contribution**<a name="contribution"></a>

Contributions are welcome! I don't have a specific format for contributions, but please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

---------------------------------------------------------------------------------------------------------------------------------------------------
