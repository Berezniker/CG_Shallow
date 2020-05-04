import subprocess
import os

venv: str = "venv"


def check_venv():
    if os.path.exists(venv):
        print("A virtual environment has already been created.")
        while True:
            key: str = input("Re-create? [Y/N]")
            if key.upper() == 'Y':
                subprocess.call(f"rm -r {venv}")
                break
            elif key.upper() == 'N':
                print("\n> End of run.")
                exit(0)
            else:
                print("Invalid input")


if __name__ == "__main__":
    print("> Run!\n")
    check_venv()
    # install 'virtualenv'
    subprocess.call(args="pip3 install virtualenv", shell=True)
    # create virtual environment:
    subprocess.call(args=f"virtualenv {venv}", shell=True)
    # activate virtual environment:
    subprocess.call(args=f"source {venv}/bin/source", shell=True)
    # load libraries
    subprocess.call(args="pip3 install --upgrade -r requirements.txt", shell=True)
    # deactivate virtual environment:
    subprocess.call(args="deactivate", shell=True)
    print("\n> End of run.")
