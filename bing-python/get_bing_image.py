import requests
import os
import ctypes
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import PhotoImage
import time

def make_get_request(url, params=None, headers=None):
    try:
        # Make the get request
        response = requests.get(url, params=params, headers=headers, verify=False)

        # Check if the request wa successful
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        # Process the response
        return response.json()  # or response.txt for raw text

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}") # e.g. 404 Not Found
    except Exception as err:
        print(f"An error occurred: {err}") # Other errors


def download_file(url, save_dir, filename=None):
    try:
        # Send a get requests
        response = requests.get(url, stream=True, verify=False) # Use stream for large files

        # Check is request was successful
        response.raise_for_status() # Raises an HTTPError for bad response 4xx or 5xx

        # Create save_dir if it does not exist
        os.makedirs(save_dir, exist_ok=True)
        base_url = url.split('=')[1]
        filename = os.path.basename(base_url)

        file_path = os.path.join(save_dir, filename)
        print(file_path)

        # Write the content to a file
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded and save to: {file_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error has occurred: {err}")

    return file_path

def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)


def get_description(url):
    # URL to fetch
    url = "https://bing.gifposter.com/"

    # Fetch the webpage
    response = requests.get(url, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the meta tag element
        meta_description = soup.find('meta', property='og:description')

        # Extract the meta tag with property 'og:description'
        if meta_description and 'content' in meta_description.attrs:
            print(meta_description['content'])
        else:
            print("meta description not found.")
    
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    
    #print(meta_description['content'])
    return meta_description['content']


def create_transparent_window(content):
    # Create main windows
    root = tk.Tk()

    # Set Window Title
    root.title("Bing Daily Image Description")

    # Set Window size
    window_width = 400
    window_height = 200
    # Set window size
    root.geometry(f"{window_width}x{window_height}")

    # Make window tranparent
    root.wm_attributes("-alpha", 0.7)

    # Make window always on bottom
    root.wm_attributes("-topmost", False)
    root.wm_attributes("-disabled", False)

    label = tk.Label(root, text=content, bg="lightblue", font=("Helvetica", 10), wraplength=380, justify="center")
    label.pack(expand=True, fill=tk.BOTH)

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    offset_x = 1500
    # Position the window on the right monitor
    # Assuming the right monitor is to the right of the primary monitor
    # You may need to adjust this based on your display configuration
    root.geometry(f"+{screen_width + offset_x}+10")  # Positioning the window (x=screen_width + offset, y=100)

    # Set the window to be bottommost
    hwnd = ctypes.windll.user32.FindWindowW(None, root.title())
    ctypes.windll.user32.SetWindowPos(hwnd, 1, 0, 0, 0, 0, 0x0001 | 0x0002)  # SWP_NOSIZE | SWP_NOMOVE | HWND_BOTTOM

     # Function to close the application after 12 hours
    def close_application():
        print("Terminating the application after 12 hours.")
        root.destroy()  # Close the Tkinter window

    duration = 12 * 60 * 60 * 1000  # 12 hours in milliseconds
    root.after(duration, close_application)

    # Run main loop
    root.mainloop()

if __name__ == "__main__":
    url = "https://bing.biturl.top/?mkt=en-US"
    params = {}
    headers = {}
    save_directory = "C:\Scripts"
    filename = None

    response_data = make_get_request(url, params=params, headers=headers)
    if response_data:
        # Get URL of image to download the image
        image = response_data.get('url')
    
    image_path = download_file(image, save_directory, filename=filename)
    set_wallpaper(image_path)

    description = get_description(url)

    create_transparent_window(description)

    