import datetime
import os

def main():   
    name = "DateThing"
    # open /tmp/input.txt and read the first line
    input_var = "no var detected"
    input_file = f"/temp/{name}_input.txt"
    if os.path.exists(input_file):
        with open(input_file, "r") as f:
            input_var = f.readline().strip() 

    print(f"First line of /tmp/input.txt: {input_var}")

    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    formatted_datetime = f"Current date and time: {formatted_datetime}, input_var: {input_var}"

    with open("/tmp/output.txt", "w") as f:
        f.write(formatted_datetime + "\n")

    print(f"Wrote to /tmp/output.txt: {formatted_datetime}")

if __name__ == "__main__":
    main()
