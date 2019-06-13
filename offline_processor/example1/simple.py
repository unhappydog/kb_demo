import os
from settings import BASE_DIR

import aiml
from aiml.constants import *

# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()
aiml_path = os.path.join(BASE_DIR, "resources", "aiml")

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
k.learn(os.path.join(aiml_path, "cn-startup.xml"))

# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.
k.respond("load aiml cn")

# Loop forever, reading user input from the command
# line and printing responses.
while True: 
    if PY3:
        print(k.respond(input("> ")))
    else:
        print(k.respond(raw_input("> ")))
