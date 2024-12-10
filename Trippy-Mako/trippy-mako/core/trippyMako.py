#!/usr/bin/env python
while True:
    try:
        with open("C:\Users\dhkre\Desktop\Capstone\Trippy-Mako\Trippy-Mako\trippy-mako\core\welcome\w1.txt", "r") as f:
            print(f.read())
            
    except FileNotFoundError:
        print("Error: Welcome file not found...")
    except Exception as e:
        print("Error: Unexpected error occurred, {e}")
        raise