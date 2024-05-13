# Modular Discord Bot System

This system is designed to be a modular Discord bot system. The main autoloader `main.py` is responsible for loading each module and allowing it to run on one machine.

## How it Works

The autoloader works by scanning the `modules` directory for Python files (`.py`). Each of these files is considered a module. The autoloader imports each module and checks if it has a `run` function. If it does, and the `run` function is a coroutine (i.e., it's an `async` function), the autoloader creates a new task for the `run` function and adds it to a list of tasks.

Once all modules have been processed, the autoloader uses `asyncio.gather` to run all the tasks concurrently. If any task is cancelled, the autoloader catches the `asyncio.CancelledError` exception and logs a message.

If the autoloader encounters an `ImportError` while trying to import a module, it logs an error message and continues with the next module. If any other exception occurs during the module loading process, it's caught and logged in the `main` function.

## How to Use to Make Your Own Module

To add a new module to the system, simply create a new Python file in the `modules` directory. This file should define a coroutine function named `run`. This function will be called when the module is loaded.

For example, a simple module might look like this:
```py
async def run():
    print("Hello, world!")
```

To run the system, simply execute the `main.py` script. The autoloader will automatically find and load all modules in the `modules` directory.

Please note that the system is designed to be used with Python's `asyncio` library, so your `run` function should be an `async` function. If you're not familiar with `asyncio`, you might want to read up on it before writing your modules.

## Support 
If you need help with the system, please contact me on Discord at `pabz.` and I can be found in my community [Discord](https://discord.gg/redberry).

## Purchaseable Modules
- (WIP) [RustMaps](https://redberry.gg) - A module that allows you to view and create Rust maps in Discord.
