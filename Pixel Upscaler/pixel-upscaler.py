import os
from PIL import Image

def upscale_images():
    # Ask the user for the scaling factor
    try:
        scale_factor = int(input("How many times bigger do you want the images? "))
        if scale_factor <= 0:
            raise ValueError("Scale factor must be a positive integer.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    # Define the script's directory as the base path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the output directory relative to the script's location
    output_dir = os.path.join(script_dir, "upscaled_images")
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all files in the script's directory
    files = os.listdir(script_dir)

    # Supported image formats
    supported_formats = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

    # Process each file
    for file in files:
        # Check if the file is an image
        if any(file.lower().endswith(ext) for ext in supported_formats):
            try:
                # Open the image
                file_path = os.path.join(script_dir, file)
                image = Image.open(file_path)
                
                # Calculate the new size
                new_width = image.width * scale_factor
                new_height = image.height * scale_factor

                # Resize the image using nearest-neighbor interpolation
                upscaled_image = image.resize((new_width, new_height), Image.NEAREST)
                
                # Save the upscaled image in the output directory
                filename, ext = os.path.splitext(file)
                output_path = os.path.join(output_dir, f"{filename}-enhanced{ext}")
                upscaled_image.save(output_path)
                print(f"Upscaled and saved: {output_path}")
            except Exception as e:
                print(f"Failed to process {file}: {e}")

if __name__ == "__main__":
    upscale_images()
