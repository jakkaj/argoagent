import datetime
import os
import wikipedia
import sys

def main():   
    name = "WikipediaSearch"
    # open /tmp/input.txt and read the first line
    input_var = "Pluto (Dwarf Planet)"
   
    if len(sys.argv) == 2:
        input_var = sys.argv[1]

    print(f"Input text: {input_var}")
    print(f"Searching Wikipedia for: {input_var}")
    
    try:
        page = wikipedia.page(input_var)
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Ambiguous result. Reverting to search")

    if not page:    
        try:
            # Search Wikipedia for the input variable
            results = wikipedia.search(input_var)

            if results:
                # Get the title of the first result
                first_result_title = results[0]

                try:
                    # Try to get the Wikipedia page for the first result
                    page = wikipedia.page(first_result_title)
                except wikipedia.exceptions.DisambiguationError as e:
                    # If disambiguation occurs, pick the first option from the list
                    first_option = e.options[0]
                    print(f"Ambiguous result. Using first option: {first_option}")
                    page = wikipedia.page(first_option)

                

            
            

        except wikipedia.exceptions.PageError:
            print(f"PageError: Page '{input_var}' not found on Wikipedia.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    if page:
            # Print the title and summary of the page
            print(f"Title: {page.title}")
            print(f"Summary: {page.summary}")

            with open("/tmp/output.txt", "w") as f:
                f.write(f"Title: {page.title}\n")
                f.write(f"Summary: {page.summary}\n")
    else:        
        print("No results found on Wikipedia.")

if __name__ == "__main__":
    main()
