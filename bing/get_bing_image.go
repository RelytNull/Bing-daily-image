package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	// Define URL of the API
	url := "https://bing.biturl.top/"

	// Make GET request
	response, err := http.Get(url)
	if err != nil {
		log.Fatalf("Failed to make GET request: %v", err)
	}
	defer response.Body.Close() // Ensure the response body id closed

	// Check if the request was successful
	if response.StatusCode != http.StatusOK {
		log.Fatalf("error: received statis code %d", response.StatusCode)
	}

	// Read response body
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatalf("Failed to read response body: %v", err)
	}

	// Print the response body
	fmt.Println(string(body))
}


