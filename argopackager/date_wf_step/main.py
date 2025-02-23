import datetime
import sys

def main():   
    
    input_var = "no var detected"
    if len(sys.argv) == 2:
        input_var = sys.argv[1]

    

    print(f"Input text: {input_var}")

    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    formatted_datetime = f"Current date and time: {formatted_datetime}, input_var: {input_var}"

    with open("/tmp/output.txt", "w") as f:
        f.write(formatted_datetime + "\n")

    print(f"Wrote to /tmp/output.txt: {formatted_datetime}")

if __name__ == "__main__":
    main()
