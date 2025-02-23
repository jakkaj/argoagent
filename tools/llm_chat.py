import os
from dotenv import load_dotenv
from openai import OpenAI
import traceback
import json  # Add this import
import yaml
from utils.wfrunner import run_workflow  # new import
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
from typing import Optional, Any

# Load environment variables from .env file


def send_to_openai(
    text: str,
    model: str = "gpt-4",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> str:
    """
    Send text to OpenAI model and get the response.
    
    Args:
        text: The input text to send to the model
        model: The OpenAI model to use (default: gpt-4)
        temperature: Controls randomness in the output (0.0-1.0)
        max_tokens: Maximum number of tokens in the response (optional)
    
    Returns:
        The model's response as a string
    
    Raises:
        Exception: If OPENAI_API_KEY is not set or if the API call fails
    """
    # Load API key from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY not found in .env file")


    try:
        if model.startswith("gpt"):
            # For chat models like GPT-4 and GPT-3.5
            response = client.chat.completions.create(model=model,
            messages=[{"role": "user", "content": text}],
            temperature=temperature,
            max_tokens=max_tokens)
            return response.choices[0].message.content.strip()
        else:
            # For completion models
            response = client.completions.create(model=model,
            prompt=text,
            temperature=temperature,
            max_tokens=max_tokens)
            return response.choices[0].text.strip()

    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {str(e)}\n{traceback.format_exc()}")


# New function demonstrating simple tool usage with function calling
from typing import Any

def send_to_openai_with_function_call(
    text: str,
    model: str = "gpt-4",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> str:
    """
    Send text to OpenAI model using function calling and get the response.
    Demonstrates sample tool usage by including a function definition for calculation.

    Args:
        text: The input text to send to the model
        model: The OpenAI model to use (default: gpt-4)
        temperature: Controls randomness in the output (0.0-1.0)
        max_tokens: Maximum number of tokens in the response (optional)

    Returns:
        A string indicating function call details or model response.

    Raises:
        Exception: If the API call fails
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": text}],
            functions=[{
                "name": "calculate_sum",
                "description": "Solves a math problem from natural language",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "A python numexpr expression"},                      
                    },
                    "required": ["a", "b"]
                }
            }],
            function_call="auto",
            temperature=temperature,
            max_tokens=max_tokens
        )
        message = response.choices[0].message
        if hasattr(message, 'function_call'):
            fc = message.function_call
            if fc:
                # Parse the arguments from JSON string to dictionary
                arguments = json.loads(fc.arguments)
                result = handle_function_call(fc.name, arguments)
                return f"Function called: {fc.name} with arguments: {fc.arguments}, Result: {result}"
            else:
                return f"Function called: {fc.name} with arguments: {fc.arguments}"
        return message.content.strip()
    except Exception as e:
        raise Exception(f"Error in function calling: {str(e)}\n{traceback.format_exc()}")

def handle_function_call(function_name: str, arguments: Any) -> Any:
    """
    Handle the function call based on the function name and arguments.

    Args:
        function_name: The name of the function to call
        arguments: The arguments for the function

    Returns:
        The result of the function call
    """
    if function_name == "calculate_sum":
        print(f"Calculating sum with arguments: {arguments}")
        return calculate_sum(arguments["prompt"])
    else:
        raise Exception(f"Function {function_name} not recognized")

def calculate_sum(a: str) -> float:
    """
    Calculate the sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """

    result = call_wf_runner("/workspaces/argoagent/argo-math-service.yaml", a)

    return result

def call_wf_runner(wf_yaml_file: str, new_expression: str, namespace: str = "argo"):
    """
    Reads the workflow YAML from a file, updates the 'expression' parameter,
    and calls run_workflow.
    
    Args:
        wf_yaml_file: File path to the workflow YAML definition.
        new_expression: New value for the 'expression' parameter.
        namespace: Kubernetes namespace (default: "argo")
        
    Returns:
        The workflow object returned by run_workflow.
    """
    with open(wf_yaml_file, "r") as f:
        workflow_yaml = f.read()
    # Parse YAML and update the 'expression' parameter
    workflow_dict = yaml.safe_load(workflow_yaml)
    for param in workflow_dict.get("spec", {}).get("arguments", {}).get("parameters", []):
        if param.get("name") == "expression":
            param["value"] = new_expression
    updated_yaml = yaml.safe_dump(workflow_dict)
    wfresult = run_workflow(updated_yaml, namespace)
    status = wfresult.status
    if status.phase in ["Succeeded", "Failed", "Error"]:
        # Print workflow outputs
        print("\nNode Outputs:")
        for node_id, node in status.nodes.items():
            if node.outputs:
                print(f"\nNode: {node_id}")
                for param in node.outputs.parameters or []:
                    print(f"Parameter {param.name}: {param.value}")
                    return param.value
                for artifact in node.outputs.artifacts or []:
                    print(f"Artifact {artifact.name}: {artifact.s3.key if artifact.s3 else 'N/A'}")
    else:
        print("No outputs found in the workflow.")

if __name__ == "__main__":
    # Example usage of send_to_openai
    # try:
    #     response = send_to_openai("Hello, how are you?")
    #     print(f"Model response: {response}")
    # except Exception as e:
    #     print(f"Error: {e}")

    # Sample tool usage with function calling
    try:
        response_fc = send_to_openai_with_function_call("Please give me the square root of 2")
        print(f"Function calling response: {response_fc}")
    except Exception as e:
        print(f"Function calling error: {e}")