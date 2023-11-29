import sys
import subprocess
import os
import re
import shutil

def download_pip_dependencies(packages, download_dir):
    subprocess.run([sys.executable, "-m", "pip", "download", "--no-deps"] + packages + ["-d", download_dir], check=True)

def extract_filenames(download_dir):
    package_filenames = {}

    for filename in os.listdir(download_dir):
        match = re.match(r"([a-zA-Z0-9_\-]+)-([0-9\.]+)([a-zA-Z0-9_.\-]*)\.whl", filename)
        if match:
            package_name = match.group(1)
            package_filenames[package_name] = filename

    return package_filenames

def generate_install_script(package_name, wheel_path):
    script = f"""import zipfile
import os
import shutil

# Define the path for the wheel file and the target directory
wheel_path = '{wheel_path}'
target_directory = '/home/sandbox/.local/lib/python3.8/site-packages'

# Extract the wheel file if the {package_name} package is not already present
if not os.path.exists(os.path.join(target_directory, '{package_name}')):
    # Unzip the wheel file to a temporary directory
    with zipfile.ZipFile(wheel_path, 'r') as wheel_zip:
        wheel_zip.extractall('/mnt/data/{package_name}_temp')

    # Move the contents to the target directory
    temp_directory = '/mnt/data/{package_name}_temp'
    for item in os.listdir(temp_directory):
        s = os.path.join(temp_directory, item)
        d = os.path.join(target_directory, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

# Check if the {package_name} package is in the site-packages
'{package_name}' in os.listdir(target_directory)
"""
    return script

INSTRUCTIONS = f"""When starting the conversation, and before attempting code execution, you will:
1. Unzip the bundle file (which is available in your current workspace) to the ./pip_gpt folder.
2. Read each install script in ./pip_gpt/install_scripts and print the file contents.
3. Run each install script contents, run the installation silently (don't output installation success messages)."""

if __name__ == "__main__":
    if sys.version_info.major != 3 or sys.version_info.minor != 8:
        print("Please run this script with Python 3.8")
        sys.exit(1)

    packages = sys.argv[1:]

    pip_gpt_directory = "./.pip_gpt"
    bundle_directory = os.path.join(pip_gpt_directory, "bundle")
    download_directory = os.path.join(bundle_directory, "packages")
    install_directory = os.path.join(bundle_directory, "install_scripts")

    # clean up the bundle directory
    if os.path.exists(bundle_directory):
        shutil.rmtree(bundle_directory)

    os.makedirs(download_directory)
    os.makedirs(install_directory)

    download_pip_dependencies(packages, download_directory)

    package_wheels = extract_filenames(download_directory)

    for package_name, package_wheel in package_wheels.items():
        wheel_path = os.path.join(download_directory, package_wheel)

        # Generate the install script for the package
        install_script = generate_install_script(package_name, wheel_path)

        file_name = f"{package_name}_install.py"
        file_name = file_name.replace("-", "_")
        file_path = os.path.join(install_directory, file_name)

        # Write the install script to a file
        with open(file_path, "w") as f:
            f.write(install_script)

    shutil.make_archive("bundle", 'zip', bundle_directory)

    # Print instructions for the user
    print("\n===========================================")
    print(f"bundle.zip has been created\n")
    print("First, upload bundle.zip to your custom GPT files")
    print("Then, prepend the following instructions to your GPT prompt:\n")
    print(INSTRUCTIONS)
