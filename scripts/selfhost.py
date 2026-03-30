import os
import subprocess
def main():
    sigmaboy = False
    try:
        result = subprocess.run(['node', '-v'], capture_output=True, text=True, check=True, shell=False)
        if str(result.stdout).startswith("v"):
            print("Running selfhost script in js with node...")
            sigmaboy = True
    except FileNotFoundError:
        print("u should install nodejs (or its not in the path) if u want to selfhost")
        print("and then run this script again")
        sigmaboy = False

    if sigmaboy:
        os.system("node scripts/selfhost.js")

if __name__ == "__main__":
    main()