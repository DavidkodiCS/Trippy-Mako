# Dev Docs for running and adding tests

## Adding a cli Test to use options as a user
In test_cli.py find test_config_options(options). Using the @pytest.mark.parametrize()
Call above adding a tuple that contains `(testname, [options list])` add a new named
test with options as a user would enter them. Here is an example use:

`("Exit Config Menu", ["config", "exit", "exit"])`
This tests opening the configurations menu and then immediatly exiting out and exiting
trippy mako

As of now all option lists need to completely exit trippy mako to resolve successful
test