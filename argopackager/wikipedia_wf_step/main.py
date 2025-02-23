import datetime
import os
import wikipedia

def main():   
    name = "WikipediaSearch"
    # open /tmp/input.txt and read the first line
    input_var = "Bendigo, Victoria, Australia"
   
    input_file = f"/temp/{name}_input.txt"

    if os.path.exists(input_file):
        with open(input_file, "r") as f:
            input_var = f.readline().strip() 

    print(f"Searching Wikipedia for: {input_var}")

    try:
        # Search Wikipedia for the input variable
        results = wikipedia.search(input_var)

        if results:
            # Get the title of the first result
            first_result_title = results[0]

            # Get the Wikipedia page for the first result
            page = wikipedia.page(first_result_title)

            # Print the title and summary of the page
            print(f"Title: {page.title}")
            print(f"Summary: {wikipedia.summary(first_result_title)}")

            with open("/tmp/output.txt", "w") as f:
                f.write(f"Title: {page.title}\n")
                f.write(f"Summary: {wikipedia.summary(first_result_title)}\n")

        else:
            print("No results found on Wikipedia.")

    except wikipedia.exceptions.PageError:
        print(f"PageError: Page '{input_var}' not found on Wikipedia.")
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"DisambiguationError: Multiple possible pages found for '{input_var}'. Please be more specific.")
        print(e.options)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
