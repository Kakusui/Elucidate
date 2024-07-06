---------------------------------------------------------------------------------------------------------------------------------------------------

**Table of Contents**
- [**About**](#about)
- [**Notes**](#notes)
  - [Known Issues:](#known-issues)

---------------------------------------------------------------------------------------------------------------------------------------------------

## **About**<a name="about"></a>

Elucidate has a trello board [here](https://trello.com/b/uOmiU7by/elucidate).

---------------------------------------------------------------------------------------------------------------------------------------------------

## **Notes**<a name="notes"></a>

**Elucidate**

"Smarter Translations through LLM Self-Evaluation"

This repository remains to be actually developed upon in mass, and is currently more of a placeholder rather than a fully functional package. Although is does have some functionality, it is not yet ready for use.

The package is currently being planned and is expected to begin full development on July 8, 2024, when Backdrop Build v5 begins.

We're seeking contributors to help us develop this package. If you're interested in contributing, please contact us at [Bikatr7@proton.me](mailto:Bikatr7@proton.me).

The general idea is to use OpenAI (initially) and other LLM's (Anthropic and Gemini later) to continuously iterate upon translations to improve the quality. The package aims to utilize [EasyTL](https://github.com/Bikatr7/EasyTL) as a translation engine, but will also support providing already translated text to the package.

This package utilizes Python protocols to "monkeystrap" new functions onto the EasyTL package. This allows for Elucidate to utilize a lot of the common logic already present in EasyTL, without having to duplicate it. For an idea of how this works, see [here](/src/elucidate/evaluators/protocols.py).

### Known Issues:

- **Logging Directory Management**: EasyTL manages its logging directory by retrieving the class name from the qualified function name of the logged function. This setup allows for extensive code reuse but   poses a challenge for protocol-based functions in Elucidate, which are classless static functions. Consequently, the logging directory attribute is not present. This issue can be addressed by:
    - Monkeystrapping a new decorator definition for Elucidate.
    - Modifying EasyTL's logging directory management approach.
    - Changing how protocol-based functions are arranged in Elucidate.
   
   The former approach is preferred. Currently, the logging directory parameter does not function as intended in Elucidate.

- **Complexity from Protocols**: The extensive use of protocols adds significant background complexity. While this enables high code reuse and flexibility, it can make the code harder to follow. We are actively working on improving code clarity.

---------------------------------------------------------------------------------------------------------------------------------------------------
