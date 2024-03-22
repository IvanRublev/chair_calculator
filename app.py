import argparse

from src.chair_calculator_main import chairs_per_room

if __name__ == "__main__":
    """This is the main entry point of the application.
    
    It processes command line arguments, then calculates and prints chair type statistics for apartment and per room.
    """

    parser = argparse.ArgumentParser(description="Prints the chair statistics of the floor plan.")
    parser.add_argument(
        "--file", metavar="file_path", type=str, help="path to a file with the floor plan", required=True
    )

    args = parser.parse_args()

    file_path = args.file

    with open(file_path, "r") as file:
        plan_content = file.read()

    print(chairs_per_room(plan_content))
