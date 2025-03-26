import requests
import os
import ctypes
from bs4 import BeautifulSoup
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
    response = requests.get(url)

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
    
    return meta_description['content']


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
    
    image_path =download_file(image, save_directory, filename=filename)
    set_wallpaper(image_path)