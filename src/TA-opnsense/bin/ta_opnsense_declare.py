# encode = utf-8

import os
import sys
import re

ta_name = 'TA-opnsense'
pattern = re.compile(r"[\\/]etc[\\/]apps[\\/][^\\/]+[\\/]bin[\\/]?$")
new_paths = [path for path in sys.path if not pattern.search(
    path) or ta_name in path]
new_paths.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
sys.path = new_paths
