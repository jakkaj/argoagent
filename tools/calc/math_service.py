from fastapi import FastAPI
from pydantic import BaseModel
import numexpr

app = FastAPI()

class Problem(BaseModel):
    problem: str


def parse_and_solve(problem_str: str) -> str:
    # Assume the problem_str is already in a valid numexpr format
    try:
        result = numexpr.evaluate(problem_str)
        if hasattr(result, 'item'):
            result = result.item()
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


@app.post("/solve")
def solve_math(problem: Problem):
    answer = parse_and_solve(problem.problem)
    return {"answer": answer}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
