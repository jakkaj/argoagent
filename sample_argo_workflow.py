from hera.workflows import Workflow
from hera.shared import global_config
import time
import yaml
import os


def main():
    # Configure connection to Argo Workflows server
    global_config.host = "http://localhost:2746"
    
    # Load the workflow definition from YAML file using an absolute path
    yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "argo-math-service.yaml")
    with open(yaml_path, "r") as f:
        wf_dict = yaml.safe_load(f)
    
    # Set namespace in the workflow definition
    # if "metadata" not in wf_dict:
    #     wf_dict["metadata"] = {}
    # wf_dict["metadata"]["namespace"] = "argo"
    
    # Create Workflow object from the YAML definition
    w = Workflow.from_dict(wf_dict)
    print(f"Loaded workflow: {w.name}")
    
    # Set namespace for the workflow object
    w.namespace = "argo"
    
    # Submit the workflow
    w.create()
    print(f"Submitted workflow: {w.name}")
    
    wf = w.wait()
    status = wf.status
    print(f"Workflow status: {status.phase}")
    # Watch the workflow status
   
    
    print (status)
    
        
    print(f"Workflow status: {status.phase}")
    
    if status.phase in ["Succeeded", "Failed", "Error"]:
        # Print workflow outputs
        print("\nWorkflow Outputs:")
        if status.outputs:
            for param in status.outputs.parameters or []:
                print(f"Parameter {param.name}: {param.value}")
            for artifact in status.outputs.artifacts or []:
                print(f"Artifact {artifact.name}: {artifact.s3.key if artifact.s3 else 'N/A'}")
        
        # Print individual node outputs
        print("\nNode Outputs:")
        for node_id, node in status.nodes.items():
            if node.outputs:
                print(f"\nNode: {node_id}")
                for param in node.outputs.parameters or []:
                    print(f"Parameter {param.name}: {param.value}")
                for artifact in node.outputs.artifacts or []:
                    print(f"Artifact {artifact.name}: {artifact.s3.key if artifact.s3 else 'N/A'}")
        
    
      # Poll every 2 seconds


if __name__ == '__main__':
    main()
