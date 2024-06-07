#!/usr/bin/env python3
from FlaskApp import *
import os
import importlib



"""from Apps.App1 import routes as routes1
from Apps.BettyLinter import routes as routebetty"""

prefixes = ""

print(__file__, "sdftygsyhsdiuqxljlkwchgfchgjhkjkxfvxdghcnj,wxkhjhvcbjxkxckhgwxjhkjlcjwxjgcjkwxjlc")
os.chdir(os.path.dirname(os.path.realpath(__file__)))


for filename in os.listdir('./Apps'):  # Iterate over each file in the folder

    if filename.endswith('.py') and filename != '__init__.py':                              # Check if the file is a Python module
        module_name = filename[:-3]                                                         # Remove the .py extension
        module = importlib.import_module(f"Apps.{module_name}")       # Import the module dynamically

        if hasattr(module, 'routes') and hasattr(module, 'prefix'):
            module.routes()                 # Call the routes function
            addr = f'http://{server_ip}{ module.prefix}'
            prefixes += f'<a href="{addr}">{addr}</a><br>'

@app.route('/')
def index2():
    print(prefixes)
    return prefixes

if __name__ == '__main__':
    app.run(port=8000, debug=True)
