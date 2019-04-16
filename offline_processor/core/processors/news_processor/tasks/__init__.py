# __all__ = []
# __all__ = ["DistinctTask", "PreProcessTask"]

import os

dir = os.path.abspath(__file__)
dir = os.path.dirname(dir)

temp_list = []
for file in os.listdir(dir):
    if os.path.isfile(file):
        if file != "__init__.py":
            temp_list.append(file.strip(".py"))

__all__ = temp_list
