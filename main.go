package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"path/filepath"

	wfv1 "github.com/argoproj/argo-workflows/v3/pkg/apis/workflow/v1alpha1"
	wfclientset "github.com/argoproj/argo-workflows/v3/pkg/client/clientset/versioned"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
	"sigs.k8s.io/yaml"
)

func main() {
	// Load kubernetes configuration
	kubeconfig := filepath.Join(homedir.HomeDir(), ".kube", "config")
	config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
	if err != nil {
		log.Fatalf("Error building kubeconfig: %v", err)
	}

	// Create Argo Workflows clientset
	wfClient, err := wfclientset.NewForConfig(config)
	if err != nil {
		log.Fatalf("Error creating workflow client: %v", err)
	}

	// Read the workflow template
	wfBytes, err := ioutil.ReadFile("argo-math-service.yaml")
	if err != nil {
		log.Fatalf("Error reading workflow file: %v", err)
	}

	// Parse the workflow template
	var wf wfv1.Workflow
	err = yaml.Unmarshal(wfBytes, &wf)
	if err != nil {
		log.Fatalf("Error parsing workflow template: %v", err)
	}

	// Submit the workflow
	wf.Namespace = "argo"
	createdWf, err := wfClient.ArgoprojV1alpha1().Workflows("argo").Create(
		context.Background(),
		&wf,
		metav1.CreateOptions{},
	)
	if err != nil {
		log.Fatalf("Error submitting workflow: %v", err)
	}

	fmt.Printf("Workflow %s submitted successfully\n", createdWf.Name)

	// Watch the workflow status
	fmt.Printf("Watching workflow status...\n")
	watch, err := wfClient.ArgoprojV1alpha1().Workflows("argo").Watch(
		context.Background(),
		metav1.ListOptions{
			FieldSelector: fmt.Sprintf("metadata.name=%s", createdWf.Name),
		},
	)
	if err != nil {
		log.Fatalf("Error watching workflow: %v", err)
	}

	for event := range watch.ResultChan() {
		wf, ok := event.Object.(*wfv1.Workflow)
		if !ok {
			log.Printf("Unexpected type in watch event")
			continue
		}

		fmt.Printf("Workflow status: %s\n", wf.Status.Phase)
		if wf.Status.Phase == wfv1.WorkflowSucceeded ||
			wf.Status.Phase == wfv1.WorkflowFailed ||
			wf.Status.Phase == wfv1.WorkflowError {

			// Get the final workflow state to access outputs
			finalWf, err := wfClient.ArgoprojV1alpha1().Workflows("argo").Get(
				context.Background(),
				wf.Name,
				metav1.GetOptions{},
			)
			if err != nil {
				log.Fatalf("Error getting final workflow state: %v", err)
			}

			// Print workflow outputs
			fmt.Println("\nWorkflow Outputs:")
			if finalWf.Status.Outputs != nil {
				for _, param := range finalWf.Status.Outputs.Parameters {
					fmt.Printf("Parameter %s: %s\n", param.Name, param.Value.String())
				}
				for _, artifact := range finalWf.Status.Outputs.Artifacts {
					fmt.Printf("Artifact %s: %s\n", artifact.Name, artifact.S3.Key)
				}
			}

			// Print individual node outputs
			fmt.Println("\nNode Outputs:")
			for nodeName, node := range finalWf.Status.Nodes {
				if node.Outputs != nil {
					fmt.Printf("\nNode: %s\n", nodeName)
					for _, param := range node.Outputs.Parameters {
						fmt.Printf("Parameter %s: %s\n", param.Name, param.Value.String())
					}
					for _, artifact := range node.Outputs.Artifacts {
						fmt.Printf("Artifact %s: %s\n", artifact.Name, artifact.S3.Key)
					}
				}
			}
			break
		}
	}
}
