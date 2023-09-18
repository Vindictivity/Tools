import os
from time import sleep
from PIL import Image

# Give instructions for the program
def instruct():
    print("\n\nHey, welcome to my little image conversion tool!\n")
    print("Before you use this tool, please follow the instructions below:\n\n")
    print("1.Create a new folder on your desktop.\n")
    print("2.Drag this .exe file into that folder.\n")
    print("3.Drag the root folder of the directory you'd like to convert into the same folder.\n")
    folder = input("To proceed, enter the name of the folder you would like to convert from:\n\n")
    navigate(folder)

# Convert images
def convert(input_file, output_file):
    with Image.open(input_file) as image:
        image.save(output_file, 'WEBP', quality=100)

# Sift through the input folder
def navigate(folder):
    input_path = os.path.join(os.getcwd(), folder)
    output_path = os.path.join(os.getcwd(), "Output")

    if not os.path.exists(input_path):
        print("\nThis path is not available, make sure it is in the same folder as the .exe\n")
        print("\nThe program will shut off shortly, please address the issue and try again\n")
        sleep(5)
        return

    if os.path.exists(output_path):
        print("\nA folder named `Output` already exists, please delete it\n")
        print("\nThe program will shut off shortly, please address the issue and try again\n")
        sleep(5)
        return

    image_counter = 0
    conversion_counter = 0
    
    os.mkdir(output_path)
    print("\nOutput folder created\n")

    for dirpath, dirnames, filenames, in os.walk(input_path):
        print("-" * 60)
        print(f"Directory: {dirpath}")
        print("-" * 60)

        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_counter += 1

        relative_path = os.path.relpath(dirpath, input_path)
        output_directory = os.path.join(output_path, relative_path)

        if not os.path.exists(output_directory):
            os.mkdir(output_directory)

        print('• Directory generated: ' + relative_path)

        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_file_path = os.path.join(dirpath, filename)
                print('• Converting: ' + filename)
                output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.webp')

                convert(input_file_path, output_file_path)
                conversion_counter += 1
    
    print(f"\nTotal .png, .jpg, .jpeg images found: {image_counter}")

    print(f"Converted {conversion_counter} images to webp format")
    
# Driver function
def main():
    instruct()

# Initialization
if __name__ == "__main__":
    main()
