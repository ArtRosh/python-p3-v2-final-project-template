# lib/cli.py
from lib.models import Owner, Car
from lib.helpers import (
    clear_screen, pause, prompt, prompt_nonempty, prompt_int,
    choose_from_list, confirm, exit_program
)

def ensure_schema():
    """Create tables if they don't exist."""
    Owner.create_table()
    Car.create_table()

# ---------------- Main Menus ----------------

def owners_menu():
    while True:
        clear_screen()
        print("=== Owners Menu ===")
        print("A. List owners")
        print("B. Create owner")
        print("C. Rename owner")
        print("D. Delete owner")
        print("E. Show owner's cars")
        print("BCK. Back")
        choice = prompt("> ").lower()

        if choice == "a":
            clear_screen()
            owners = Owner.all()
            if not owners:
                print("No owners yet.")
            else:
                for i, o in enumerate(owners, start=1):
                    print(f"{i}. {o.name}")
            pause()

        elif choice == "b":
            name = prompt_nonempty("Owner name: ")
            Owner(name).save()
            print("Owner created.")
            pause()

        elif choice == "c":
            owner = choose_from_list(Owner.all(), "Choose an owner to rename:")
            if owner:
                new_name = prompt_nonempty(f"New name for {owner.name}: ")
                owner.name = new_name
                owner.save()
                print("Owner updated.")
                pause()

        elif choice == "d":
            owner = choose_from_list(Owner.all(), "Choose an owner to delete:")
            if owner and confirm(f"Delete '{owner.name}' and all their cars?"):
                owner.delete()
                print("Owner deleted.")
                pause()

        elif choice == "e":
            owner = choose_from_list(Owner.all(), "Choose an owner:")
            if owner:
                owner_cars_menu(owner)

        elif choice == "bck":
            return
        else:
            print("Invalid choice.")
            pause()

def owner_cars_menu(owner: Owner):
    while True:
        clear_screen()
        print(f"=== {owner.name}'s Cars ===")
        print("A. List cars")
        print("B. Add car")
        print("C. Update a car")
        print("D. Delete a car")
        print("BCK. Back")
        choice = prompt("> ").lower()

        if choice == "a":
            cars = owner.cars
            if not cars:
                print("No cars for this owner.")
            else:
                for i, c in enumerate(cars, start=1):
                    print(f"{i}. {c.year} {c.make} {c.model}")
            pause()

        elif choice == "b":
            make = prompt_nonempty("Make: ")
            model = prompt_nonempty("Model: ")
            year = prompt_int("Year (e.g., 2020): ")
            if not isinstance(year, int):
                print("Year must be a number.")
            else:
                Car(make=make, model=model, year=year, owner_id=owner.id).save()
                print("Car added.")
            pause()

        elif choice == "c":
            cars = owner.cars
            car = choose_from_list(cars, "Choose a car to update:")
            if car:
                new_make = prompt("New make (Enter to keep): ") or car.make
                new_model = prompt("New model (Enter to keep): ") or car.model
                year_in = prompt("New year (Enter to keep): ")
                new_year = car.year if not year_in.strip() else int(year_in)

                car.make, car.model, car.year = new_make, new_model, new_year
                car.save()
                print("Car updated.")
                pause()

        elif choice == "d":
            car = choose_from_list(owner.cars, "Choose a car to delete:")
            if car and confirm("Delete this car?"):
                car.delete()
                print("Car deleted.")
                pause()

        elif choice == "bck":
            return
        else:
            print("Invalid choice.")
            pause()

def main_menu():
    ensure_schema()
    while True:
        clear_screen()
        print("=== Owners & Cars CLI ===")
        print("1. Owners")
        print("0. Exit")
        choice = prompt("> ").strip()

        if choice == "1":
            owners_menu()
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice.")
            pause()

if __name__ == "__main__":
    main_menu()
