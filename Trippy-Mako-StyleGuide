# Trippy-Mako Style Guide

This document outlines the coding standards and best practices for contributing to this project. Adhering to these guidelines ensures code consistency, readability, and maintainability.

---

## Table of Contents

1. [General Guidelines](#general-guidelines)
2. [Commenting and Documentation](#commenting-and-documentation)
3. [Naming Conventions](#naming-conventions)
4. [Code Structure](#code-structure)
5. [Function and Method Definitions](#function-and-method-definitions)
6. [Error Handling](#error-handling)
7. [Testing](#testing)
8. [Version Control](#version-control)
9. [Other Best Practices](#other-best-practices)

---

## 1. General Guidelines

- **Consistency is key**: Follow the style guide strictly to maintain consistency across the codebase.
- **PEP 8**: Always adhere to Python's [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- **Readability first**: Prioritize writing code that is easy to understand over clever solutions.
- **DRY Principle**: Avoid duplicating code. Use functions, classes, or libraries to reuse common logic.

---

## 2. Commenting and Documentation

### 2.1 Code Comments

- **High-level purpose**: Explain the intent, not the implementation details. Comments should describe "why" more than "how."
- **Placement**: 
  - Use **inline comments** sparingly and only when necessary for clarification.
  - Place comments above the code block or function they refer to.
  
```python
# Correct: Describe why a block of code exists.
# This function ensures all user inputs are sanitized before processing.
def sanitize_input(user_input):
    ...
```

- **Avoid redundant comments**: Don’t explain what’s obvious from the code itself.

```python
# Bad: This comment doesn't add any value.
x = 10  # Set x to 10
```

### 2.2 Docstrings

- **Function-level docstrings**: Use triple quotes (`"""`) to document all public modules, classes, and functions.
- **Format**: Follow the PEP 257 convention.

```python
def fetch_data(url: str) -> dict:
    """
    Fetches data from the specified URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the URL.
    """
    ...
```

- **Class-level docstrings**: Describe the class's purpose and provide an overview of its functionality.

```python
class UserManager:
    """
    A class to manage user-related operations, such as authentication
    and user data management.
    """
    ...
```

---

## 3. Naming Conventions

- **Variables**: Use descriptive names written in `snake_case`.
  
```python
# Good
user_count = 10
fetch_user_data = True
```

- **Constants**: Use `UPPER_CASE_WITH_UNDERSCORES` for constants.
  
```python
MAX_CONNECTIONS = 5
TIMEOUT_SECONDS = 30
```

- **Classes**: Use `PascalCase` for class names.
  
```python
class UserManager:
    ...
```

- **Functions and Methods**: Use `snake_case` for function and method names.
  
```python
def fetch_user_data():
    ...
```

- **Private members**: Prefix internal or private functions/methods with an underscore (`_`).

```python
def _helper_function():
    ...
```

- **Modules**: Use short, all-lowercase names for module files. Words should be separated by underscores if necessary.

```plaintext
# Good
data_processor.py
```

---

## 4. Code Structure

- **Imports**: Organize imports in three sections, separated by a blank line:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
  
```python
import os
import sys

import requests

from my_project.utils import fetch_data
```

- **Line length**: Limit all lines to a maximum of **79 characters**.
- **Blank lines**: Use blank lines to separate logical sections of code.
  - Two blank lines between class or function definitions.
  - One blank line between methods within a class.

---

## 5. Function and Method Definitions

- **Keep functions short**: Each function should perform a single responsibility. If a function is too long, consider splitting it.
- **Type hints**: Use type hints to clarify argument and return types.

```python
def add_numbers(x: int, y: int) -> int:
    return x + y
```

- **Default arguments**: Never use mutable default arguments (like lists or dictionaries) in function definitions.

```python
# Bad
def append_item(item, item_list=[]):
    item_list.append(item)
    return item_list

# Good
def append_item(item, item_list=None):
    if item_list is None:
        item_list = []
    item_list.append(item)
    return item_list
```

---

## 6. Error Handling

- **Exceptions over returning None**: Raise exceptions when an error occurs. Avoid using `None` as a sentinel value unless documented clearly.
  
```python
# Good
try:
    value = process_data(data)
except ValueError as e:
    log_error(e)
    raise
```

- **Avoid bare exceptions**: Always specify the exception you’re catching.

```python
# Bad
except:
    handle_error()

# Good
except ValueError:
    handle_value_error()
```

---

## 7. Testing

- **Unit tests**: Write unit tests for all new features and major code changes.
- **Test coverage**: Aim for at least **90% test coverage**.
- **Naming conventions**: Prefix test function names with `test_` and use descriptive names.

```python
def test_add_numbers():
    assert add_numbers(2, 3) == 5
```

- **Testing framework**: Use `pytest` for running tests.

---

## 8. Version Control

- **Commits**: Write concise, descriptive commit messages.
  - Use present tense (e.g., "Add user authentication").
  - Avoid vague messages like "Fix bug" or "Update".
  
```plaintext
# Good
Add error handling for invalid user input.
```

- **Branching**: Use meaningful branch names.

```plaintext
# Feature branches
feature/user-authentication

# Bugfix branches
bugfix/fix-404-error
```

---

## 9. Other Best Practices

- **Avoid premature optimization**: Optimize code only when necessary, and document why.
- **Use logging**: Replace print statements with logging.
  
```python
import logging
logging.basicConfig(level=logging.INFO)

logging.info("Processing user data")
```

- **Keep dependencies minimal**: Only add dependencies that are absolutely necessary for the project.
- **Use virtual environments**: Ensure your development environment is isolated using `venv` or similar tools.
