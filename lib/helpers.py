# lib/helpers.py
import os
import sys

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause(msg: str = "Press Enter to continue..."):
    try:
        input(msg)
    except (EOFError, KeyboardInterrupt):
        pass

def prompt(text: str):
    try:
        return input(text).strip()
    except (EOFError, KeyboardInterrupt):
        return ""

def prompt_nonempty(text: str):
    while True:
        s = prompt(text)
        if s:
            return s
        print("Value is required.")

def prompt_int(text: str):
    s = prompt(text)
    if not s:
        return None
    if not s.isdigit():
        return None
    return int(s)

def confirm(question: str) -> bool:
    ans = prompt(f"{question} (yes/no): ").lower()
    return ans == "yes"

def choose_from_list(items, title: str = ""):
    if not items:
        print("Nothing to choose from.")
        return None
    if title:
        print(title)

    for i, obj in enumerate(items, start=1):
        label = getattr(obj, "name", None)
        if label is None:
            year = getattr(obj, "year", None)
            make = getattr(obj, "make", None)
            model = getattr(obj, "model", None)
            label = f"{year} {make} {model}" if year and make and model else str(obj)
        print(f"{i}. {label}")

    idx = prompt_int("Pick a number (or Enter to cancel): ")
    if idx is None:
        return None
    if not (1 <= idx <= len(items)):
        print("Invalid choice.")
        return None
    return items[idx - 1]

def exit_program():
    print("Goodbye!")
    sys.exit(0)
