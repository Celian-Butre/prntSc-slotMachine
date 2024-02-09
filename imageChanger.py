import time
import shutil

def update_image(image_path):
    # Update the image file
    shutil.copy(image_path, 'loadedImage')

# Example usage:
if __name__ == "__main__":
    while True:
        image_path = input("Enter the path to the new image: ")
        update_image(image_path)
        print("Image updated successfully!")
