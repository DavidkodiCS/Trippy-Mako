import socket
import pytest
import trippyMako
import builtins
import os
from unittest.mock import patch

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


#DEPRECIATED SECTION (I WILL FIX ALL OF THESE POST MEETING)
# adds a mock configuration to a fake config file
#def test_addConfig():
#    global fileSize
#    fileSize = os.path.getsize("configs.ini")
#    trippyMako.configSetup()
#    set_keyboard_input(['myConfig', '0.0.0.0', '999', 'TCP'])
#    trippyMako.addConfig()
#    output = get_display_output()
#    assert output == ['Enter configuration name: ', 
#    'Enter TURN server IP address: ', 
#    'Enter TURN server port number: ', 
#    'Enter desired protocol: ', 
#    'Configuration successfully added!']

# displays mock config
#def test_displayConfig():
#    set_keyboard_input(['myConfig'])
#    trippyMako.displayConfig()
#    list = ['myConfig']
#    output = get_display_output()
#    assert output == [ list, 'Choose configuration to display: ',
#    'TURN IP: 0.0.0.0',
#    'TURN Port: 999',
#    'Protocol: TCP',
#    ]

# edits the IP address of the mock config
#def test_editConfig():
#    set_keyboard_input(['myConfig', 'turnIP', '0.0.0.1', 'n'])
#    trippyMako.editConfig()
#    set_keyboard_input(['myConfig'])
#    trippyMako.displayConfig()
#    list2 = ['myConfig']
#    output = get_display_output()
#    assert output == [ list2, 'Choose configuration to display: ',
#    'TURN IP: 0.0.0.1',
#    'TURN Port: 999',
#    'Protocol: TCP',
#    ]

# removes the configuration from the file
#def test_removeConfig():
#    set_keyboard_input(['myConfig'])
#    trippyMako.removeConfig()
#    assert os.path.getsize("configs.ini") == fileSize

# tests that exit functions don't cause program crash after 
# running configuration options
#def test_exitAfter():
#    set_keyboard_input(['exit'])
#    trippyMako.config()
#    set_keyboard_input(['exit'])
#    trippyMako.trippyMako()
#    output = get_display_output()

#    assert output == ['\n> ', 'Exiting...']


@pytest.mark.parametrize("host, port", [("localhost", 5349)])
def test_coturn_running(host, port):
    """Verify that Coturn server is running and listening on port 5349"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # Set timeout for connection attempt
    try:
        sock.connect((host, port))
        sock.close()
        assert True  # If connection succeeds, the test passes
    except (socket.error, socket.timeout):
        pytest.fail(f"Could not connect to Coturn server at {host}:{port}")

def test_demo_option():
    """See if demo option can be opened"""
    with patch("builtins.input", side_effect=["demo","new", "test", "127.0.0.1", "5349", "TCP", "exit","exit"]):
        try:
            trippyMako.main()
            assert True
        except Exception as e:
            pytest.fail(f"Demo did not run: {e}")


# Adding a new set of options as here allows you to run a set of trippymako user
# inputs and see if it runs succesfully

# NEED TO FIGURE OUT HOW TO DEAL WITH CONFIG FILE GENERATION IN A CONFIG SENSE
@pytest.mark.parametrize(
    "options",
    [
        ("Create Config", ["config", "create", "test", "10.0.0.1", "5349", "TCP", "exit", "exit"]),
        ("Edit Config", ["config", "edit", "protocol", "UDP", "n", "exit", "exit"]),
        ("List Configs", ["config", "list", "exit", "exit"]),
        ("Display Config", ["config", "display", "test", "exit", "exit"]),
        ("Help Config", ["config", "help", "exit", "exit"]),
        ("Exit Config Menu", ["config", "exit", "exit"]),
        ("Remove Config", ["config", "remove", "test", "exit", "exit"]),
    ],
    ids=lambda opt: opt[0]  # Use the first tuple item (name) as the test identifier
)
def test_config_options(options):
    """See if config options run correctly"""
    test_name, input_sequence  = options  # Unpack tuple

    with patch("builtins.input", side_effect=input_sequence):
        try:
            trippyMako.main()
            assert True
        except Exception as e:
            pytest.fail(f"Test '{test_name}' failed: {e}")

