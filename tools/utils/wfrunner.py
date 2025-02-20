from hera.workflows import Workflow
from hera.shared import global_config
import time
import yaml
import os

def run_workflow(workflow_yaml: str, namespace: str = "argo"):
    # Configure connection to Argo Workflows server
    global_config.host = "http://localhost:2746"
    # Load workflow definition from YAML string
    wf_dict = yaml.safe_load(workflow_yaml)
    # Create Workflow object and assign namespace
    w = Workflow.from_dict(wf_dict)
    w.namespace = namespace
    # Submit and wait for workflow execution
    w.create()
    wf = w.wait()
    # Optionally, return the workflow for further processing
    return wf

if __name__ == '__main__':
    # For testing: load YAML from file and run the workflow
    yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "argo-math-service.yaml")
    with open(yaml_path, "r") as f:
        workflow_yaml = f.read()
    wf = run_workflow(workflow_yaml)
    status = wf.status
    print(f"Workflow {wf.name} finished with phase: {status.phase}")
