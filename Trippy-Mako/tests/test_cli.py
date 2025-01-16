import sys 
sys.path.insert(1, '../trippy-mako/core')
import trippyMako
import builtins
import os 

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

def test_help(capsys):
    trippyMako.help()
    out, err = capsys.readouterr()

    assert out != 'Error: Welcome file not found...\n'
    assert err == ''

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

def test_displayConfig():
    set_keyboard_input(['myConfig', '0.0.0.0', '999', 'TCP'])
    configs = 
    trippyMako.displayConfig()
    output = get_display_output()
    assert output == [f"{configs}", 'Choose configuration to display: ',
    'TURN IP: ',
    'TURN Port: ',
    'Protocol: ',
    ]

# this test fails because the remove function does not work
# properly
def test_removeConfig():
    set_keyboard_input(['myConfig'])
    trippyMako.removeConfig()
    assert os.path.getsize("configs.ini") == fileSize