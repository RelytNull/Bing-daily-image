import requests
import os
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

        # Determine the filename
        # if filename is None:
            # If no filename is provided, extract it from the URL
        #    filename = os.path.join(save_dir, url.split('/')[-1])
        # else:
        #    filename = os.path.join(save_dir, filename)


        # Write the content to a file
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded and save to: {file_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error has occurred: {err}")




if __name__ == "__main__":
    url = "https://bing.biturl.top/"
    params = {}
    headers = {}
    save_directory = "C:\Scripts"
    filename = None

    response_data = make_get_request(url, params=params, headers=headers)
    if response_data:
        # Get URL of image to download the image
        image = response_data.get('url')
    
    print(image)
    download_file(image, save_directory, filename=filename)
