import runpy

options = {
    0: {"desc":"2D simulation with matplotlib visualisation", "filename":"2d.py"},
    1: {"desc":"3D simulation with matplotlib visualisation", "filename":"3d.py"},
    2: {"desc":"Any dimension simulation with raw values only", "filename":"any-dimension.py"}
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

    runpy.run_path(f"python/{options[choice]["filename"]}")

    print("\n"*20)