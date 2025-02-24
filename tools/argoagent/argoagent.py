import json
import os

def get_run_artefacts_for_llm(string_nodes):
    # parse string_nodes to json
    nodes = None
    try:
        nodes = json.loads(string_nodes)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    artefacts = ""
    for node in nodes["nodes"]:
        node_name = node["templateName"]
        for param in node["parameters"]:            
            param_value = param["value"]
            artefacts += f"\n###Output from {node_name}\n{param_value}\n\n"
    return artefacts

def save_run_artefacts_from_nodes_string(path, string_nodes):
    # parse string_nodes to json
    nodes = None
    try:
        nodes = json.loads(string_nodes)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    for node in nodes["nodes"]:
        node_name = node["templateName"]
        for param in node["parameters"]:
            param_name = param["name"]
            param_value = param["value"]
            file_path = os.path.join(path, f"{node_name}_{param_name}_output.txt")
            #get parent of file_path
            #parent_dir = os.path.dirname(file_path)
            # create the directory if it does not exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # write the file
            with open(file_path, "w") as f:
                f.write(param_value)