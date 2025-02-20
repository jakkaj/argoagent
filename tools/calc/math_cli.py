#!/usr/bin/env python3
import sys
import numexpr


def parse_and_solve(problem_str: str) -> str:
    try:
        print(f"Parsing and solving the problem: {problem_str}")
        # Assume the problem_str is already in a valid numexpr format
        result = numexpr.evaluate(problem_str)
        if hasattr(result, 'item'):
            result = result.item()
        
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} '<math expression>'")
        sys.exit(1)
    problem = sys.argv[1]
    result = parse_and_solve(problem)
    #create /tmp directory if it does not exist
    import os
    if not os.path.exists("/tmp"):
        os.makedirs("/tmp")
    # Output the result to a file

    with open("/tmp/outputs.txt", "w") as f:
        f.write(str(result))
    # verify the file was written
    with open("/tmp/outputs.txt", "r") as f:
        f.seek(0)
        print(f"File contents: {f.read()}")
        
        print(f"Result written to /tmp/outputs.txt")
    print("Result:", result)


if __name__ == '__main__':
    main()
