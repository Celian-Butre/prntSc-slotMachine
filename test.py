import cv2
import time
import Xlib.display as display
import Xlib.X as X
import Xlib.Xlib as xlib

def main():
    # Load the image
    image = cv2.imread('images/asdasj')

    # Check if the image was loaded successfully
    if image is None:
        print("Error: Unable to open or read the image file.")
        return

    # Get the dimensions of the screen
    screen_height = 1080  # Replace with your actual screen height
    screen_width = 1920   # Replace with your actual screen width

    # Calculate the dimensions for the quarter-sized window
    quarter_height = screen_height // 4
    quarter_width = screen_width // 4

    # Calculate the scaling factor to fit the image within the quarter-sized window
    scale_factor = min(quarter_height / image.shape[0], quarter_width / image.shape[1])

    # Resize the image while maintaining its aspect ratio with bilinear interpolation
    resized_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    # Create a window and display the resized image
    cv2.namedWindow('Overlay', cv2.WINDOW_NORMAL)
    cv2.imshow('Overlay', resized_image)

    # Set the window to be always on top
    cv2.setWindowProperty('Overlay', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Create X11 display
    disp = display.Display()

    # Get the root window
    root = disp.screen().root

    # Listen for window focus events
    root.change_attributes(event_mask=Xlib.X.FocusChangeMask)

    # Check for window focus every 100 milliseconds
    while True:
        try:
            # Get the focused window
            focused = disp.get_input_focus().focus
            
            # Check if the focused window is not our overlay window
            if focused != root:
                # Bring the overlay window to the front
                cv2.setWindowProperty('Overlay', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        except xlib.error.DisplayConnectionError:
            break

        # Wait for 100 milliseconds
        time.sleep(0.1)

    # Destroy all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
