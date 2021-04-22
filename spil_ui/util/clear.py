'''
Created in the past.

@author: michael.haussmann

Unloads all xx. modules (forces a general reload)
'''
import sys

def do():
    
    tmp_modules = sys.modules.copy()
    for key, value in tmp_modules.iteritems():
        if key.startswith('spil_ui.'):
            sys.modules.pop(key, None)
        if key.startswith('spil.'):
            sys.modules.pop(key, None)
