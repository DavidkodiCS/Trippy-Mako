#!/usr/bin/env python
import click

@click.command()
    
def trippyMako():
    while True:
        try:
            with open("w1.txt", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("Error: Welcome file not found...")
            
        t = input()
        print(t)

if __name__ == '__main__':
    trippyMako()