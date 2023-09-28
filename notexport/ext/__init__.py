import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
submodules = ["mdxanalysis"]
for module in submodules:
    sys.path.append(os.path.join(current_dir, module))
