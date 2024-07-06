## Copyright 2024 Kakusui LLC (https://kakusui.org) (https://github.com/Kakusui) (https://github.com/Kakusui/Elucidate)
## Use of this source code is governed by an GNU Lesser General Public License v2.1
## license that can be found in the LICENSE file.

import sys
import os

## Append the src directory to sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..')
src_path = os.path.abspath(os.path.join(parent_dir, 'src'))

sys.path.append(src_path)

## Now you can import Elucidate from elucidate.elucidate, no need to test from site-packages
from elucidate.elucidate import Elucidate