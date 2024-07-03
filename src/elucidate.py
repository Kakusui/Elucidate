## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

## built-in libraries
import typing

## third-party libraries
from easytl import EasyTL

class Elucidate:

    """
    
    Elucidate global client.

    """

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