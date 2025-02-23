
import os

import openai
import sys
def main():   
    name = "Summariser"
    # open /tmp/input.txt and read the first line
    input_var = """
To list all repositories (images) stored in your local Docker registry at k3d-registry.localhost:5000, you can use the Docker Registry HTTP API V2. Here's how you can do it using curl:

sh
Copy
Edit
curl -X GET http://k3d-registry.localhost:5000/v2/_catalog
This command will return a JSON object containing a list of repositories available in the
    """
   
    

    input_var = "no var detected"
    if len(sys.argv) == 2:
        input_var = sys.argv[1]

    
    
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        print("OPENAI_API_KEY not found in environment variables.")
        return

    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"Summarize the following text: {input_var}"}
            ]
        )
        summary = completion.choices[0].message.content
        print(summary)

        output_file = f"/tmp/output.txt"
        with open(output_file, "w") as f:
            f.write(summary)

    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return

if __name__ == "__main__":
    main()
