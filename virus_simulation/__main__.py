import runpy
import os
from virus_simulation import __path__ as pck_path

options = {
    0: {"desc":"2D simulation with matplotlib 2d visualisation", "filename":"2d.py"},
    1: {"desc":"3D simulation with matplotlib 3d visualisation", "filename":"3d.py"},
    2: {"desc":"Any dimension simulation with raw values or graphics", "filename":"any-dimension.py"},
    3: {"desc":"Exit"}
}

while True:
    print("Available options:")
    for id0, option in options.items():
        print(f"[{id0}] {option['desc']}")
    try:
        choice = int(input("Enter your an option id: "))
    except ValueError:
        print("\n" * 20)
        print(f"You entered not a number\n")
        continue
    if choice not in options:
        print("\n" * 20)
        print(f"\"{choice}\" is not an option\n")
        continue

    if choice == 3:
        exit()

    runpy.run_path(os.path.join(pck_path[0],options[choice]["filename"]))

    print("\n"*20)