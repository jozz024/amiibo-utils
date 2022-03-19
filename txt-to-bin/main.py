import re
import os

# ty for your amazing code mide i appreciate it
directory = os.path.dirname(os.path.realpath(__file__))
directory = '\\'.join([directory, "txt files"])

def convert_nfc_tools_file_to_bin(file_name):
    export_string_lines = None
    hex = ''
    with open(f"{directory}\{file_name}") as file:
        export_string_lines = file.readlines()

    for line in export_string_lines:
        match = re.search(r"(?:[A-Fa-f0-9]{2}:){3}[A-Fa-f0-9]{2}", line)
        if match:
                hex = hex + match.group(0).replace(':', '')

    bin = bytes.fromhex(hex)
    with open(f"bin files\{file_name.strip('.txt')}.bin", mode="wb") as new_file:
      new_file.write(bin)

for filename in os.listdir(directory):
    folder_addon = r'/'.join(["bins", filename])


    convert_nfc_tools_file_to_bin(filename)