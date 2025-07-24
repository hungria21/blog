import os
import subprocess

def is_iso_file(filepath):
    """
    Checks if a file is a valid ISO file by checking its extension.
    """
    return filepath.lower().endswith('.iso')

def get_iso_files(directory):
    """
    Gets a list of all ISO files in a given directory.
    """
    iso_files = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and is_iso_file(item_path):
            iso_files.append(item)
    return iso_files

def convert_iso(input_path, output_path):
    """
    Converts a standard ISO file to a format compatible with OPL.
    """
    try:
        print(f"Converting {input_path}...")
        subprocess.run(['iso2opl', input_path, output_path], check=True, capture_output=True, text=True)
        print(f"Successfully converted {input_path} to {output_path}")
    except FileNotFoundError:
        print("Error: 'iso2opl' command not found. Please ensure the OPL toolkit is installed and in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e.stderr}")

def split_iso(input_path, output_dir):
    """
    Splits large ISO files into smaller chunks compatible with FAT32 file systems.
    """
    try:
        print(f"Splitting {input_path}...")
        subprocess.run(['opl-split', '--input', input_path, '--output', output_dir], check=True, capture_output=True, text=True)
        print(f"Successfully split {input_path} into {output_dir}")
    except FileNotFoundError:
        print("Error: 'opl-split' command not found. Please ensure the OPL toolkit is installed and in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error splitting {input_path}: {e.stderr}")

def main_menu():
    """
    Displays the main menu and handles user input.
    """
    while True:
        print("\nOPL ISO Manager")
        print("1. Convert ISO to OPL format")
        print("2. Split large ISOs")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            input_dir = input("Enter the directory containing ISO files: ")
            output_dir = input("Enter the directory to save converted files: ")
            if not os.path.isdir(input_dir):
                print("Error: Input directory not found.")
                continue
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            iso_files = get_iso_files(input_dir)
            if not iso_files:
                print("No ISO files found in the specified directory.")
                continue

            for iso_file in iso_files:
                input_path = os.path.join(input_dir, iso_file)
                output_path = os.path.join(output_dir, iso_file)
                convert_iso(input_path, output_path)

        elif choice == '2':
            input_dir = input("Enter the directory containing large ISO files: ")
            output_dir = input("Enter the directory to save split files: ")
            if not os.path.isdir(input_dir):
                print("Error: Input directory not found.")
                continue
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            iso_files = get_iso_files(input_dir)
            if not iso_files:
                print("No ISO files found in the specified directory.")
                continue

            for iso_file in iso_files:
                input_path = os.path.join(input_dir, iso_file)
                split_iso(input_path, output_dir)

        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    main_menu()

if __name__ == "__main__":
    main()
