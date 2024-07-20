## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

from .util.imports.easytl_importer import InvalidResponseFormatException, InvalidTextInputException, EasyTLException, InvalidAPITypeException, OpenAIError, GoogleAPIError, AnthropicAPIError, InvalidEasyTLSettingsException

class ElucidateException(EasyTLException):
    
    def __init__(self, message:str):
        super().__init__(message)

class InvalidElucidateSettingsException(InvalidEasyTLSettingsException):
    
    def __init__(self, message:str):
        super().__init__(message)