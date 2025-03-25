package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

/*************  ✨ Codeium Command ⭐  *************/
// main is the entry point of the application. It sends a GET request to the
// Bing image API, checks if the request was successful, reads the response
// body, and prints it to the console. If any errors occur during the process,
// the application logs the error and terminates.

/******  743abd1c-01be-4a03-b2e4-470f6dd091ac  *******/
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


