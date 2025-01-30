import sys 
sys.path.insert(1, '../trippy-mako/core')
import trippyMako
import builtins
import os 
import pytest

# source for first four functions: https://www.youtube.com/watch?v=tBAj2FqgIwg
# these functions simulate input and output
def mock_input(s):
    print_values.append(s)
    return input_values.pop(0)

def mock_input_output_start():
    global input_values, print_values

    input_values = []
    print_values = []

    builtins.input = mock_input
    builtins.print = lambda s: print_values.append(s)

def get_display_output():
    global print_values
    return print_values

def set_keyboard_input(mocked_inputs):
    global input_values

    mock_input_output_start()
    input_values = mocked_inputs

# tests help menu
def test_help(capsys):
    trippyMako.help()
    out, err = capsys.readouterr()

    assert out != 'Error: Welcome file not found...\n'
    assert err == ''

# adds a mock configuration to a fake config file
def test_addConfig():
    global fileSize
    fileSize = os.path.getsize("configs.ini")
    trippyMako.configSetup()
    set_keyboard_input(['myConfig', '0.0.0.0', '999', 'TCP'])
    trippyMako.addConfig()
    output = get_display_output()
    assert output == ['Enter configuration name: ', 
    'Enter TURN server IP address: ', 
    'Enter TURN server port number: ', 
    'Enter desired protocol: ', 
    'Configuration successfully added!']

# displays mock config
def test_displayConfig():
    set_keyboard_input(['myConfig'])
    trippyMako.displayConfig()
    list = ['myConfig']
    output = get_display_output()
    assert output == [ list, 'Choose configuration to display: ',
    'TURN IP: 0.0.0.0',
    'TURN Port: 999',
    'Protocol: TCP',
    ]

# edits the IP address of the mock config
def test_editConfig():
    set_keyboard_input(['myConfig', 'turnIP', '0.0.0.1', 'n'])
    trippyMako.editConfig()
    set_keyboard_input(['myConfig'])
    trippyMako.displayConfig()
    list2 = ['myConfig']
    output = get_display_output()
    assert output == [ list2, 'Choose configuration to display: ',
    'TURN IP: 0.0.0.1',
    'TURN Port: 999',
    'Protocol: TCP',
    ]

# removes the configuration from the file
def test_removeConfig():
    set_keyboard_input(['myConfig'])
    trippyMako.removeConfig()
    assert os.path.getsize("configs.ini") == fileSize

# tests that exit functions don't cause program crash after 
# running configuration options
def test_exitAfter():
    set_keyboard_input(['exit'])
    trippyMako.config()
    set_keyboard_input(['exit'])
    trippyMako.trippyMako()
    output = get_display_output()

    assert output == ['\n> ', 'Exiting...']