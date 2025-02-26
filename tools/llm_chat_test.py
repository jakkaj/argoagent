import os
import pickle
import tempfile
import unittest

from autogen_core import CancellationToken

from templates.templateutil import compose_templates
from argoagent.argoagent import ArgoAgent
from argoagent.argorunner import ArgoSubmitConfigModel, print_mcp_tools
from autogen_ext.tools.mcp import mcp_server_tools, StdioMcpToolAdapter, StdioServerParams

from llm.llm_helper import LLMHelper
from argoagent.argoagent_datasets import AgentRunsDataset
from ml.entailment import check_entailment

##### These are not really tests, they are more helpers to build the code #####


class TestLLMChat(unittest.IsolatedAsyncioTestCase):
    

    def setUp(self):
        self.config_sample = """{
            "name": "wikiagent",
            "description": "Can search wikipedia for things.",
            "templates":[
                "wikistep",
                "summarystep",
                "extractstatsstep",
                "writeapoemstep",
                "aussifystep"
            ],
            "extra_initial_prompt_instruction": "You should always start with wikipedia. Don't summarise unless the user explicitly asks you to. Don't extract statistics unless the user explicitly asks you to. Don't write a poem unless th user explicitly asks you to. "
        }"""
    
    async def test_build_test_dataset(self):
        
        json_data = None
        with open (os.path.join(os.path.dirname(__file__), 'argoagent', 'test_data', 'agent_runs_dataset.json'), 'r') as f:
            json_data = f.read()

        llm_client = LLMHelper("gpt-4o")

        input_test_dataset = AgentRunsDataset.from_json(json_data)      

        entails, score = check_entailment("The dog is white", "The house is a building")
        assert not entails

        for t_run in input_test_dataset:
            a = ArgoAgent(self.config_sample, llm_client)

            a._set_query(t_run.input_data)
            a._run_llm_compose_templates()
            a._build_composed_templates()
            t_run.argo_agent = a

        for t_run in input_test_dataset:
            a = t_run.argo_agent
            print(t_run.steps)
            print(a.template_to_compose)

            wf_input_param = a.wf_input_param
            expected_param = t_run.param    
            entails, score = check_entailment(wf_input_param, expected_param)
            assert entails
            assert t_run.steps == a.template_to_compose
            
            
        
        
    async def test_agent(self):
        
        llm_client = LLMHelper("gpt-4o")

        a = ArgoAgent(self.config_sample, llm_client)
        await a.run_workflow("Find me information on the city of Bendigo in Victoria, Australia and extract key statistics and turn it in to aussie slang.")
        final_result = a.process_final_result()
        print(final_result)
        print(a.workflow_output_files)
        


    def test_template_build(self):
        templates = list()
        templates.append("template-wikistep.yaml")
        templates.append("template-summarystep.yaml")

        compose = compose_templates("Bendigo", templates)

        # assert compose is not none
        self.assertIsNotNone(compose)

   


    async def test_wf_run(self):
        templates = list()
        templates.append("wikistep")
        templates.append("summarystep")

        compose = compose_templates("Bendigo", templates)

        #print (compose)
        argo_system_mcp_server = StdioServerParams(
            command="/workspaces/argoagent/bin/mcp-argo-server",        
        )
        argo_tools = await mcp_server_tools(argo_system_mcp_server)
        #print_mcp_tools(argo_tools)       
        token = CancellationToken()
        argo_config_wait = ArgoSubmitConfigModel(manifest=compose, namespace="argo", wait=True)
        res4 = await argo_tools[0].run(argo_config_wait, token) 

        # generate a random temp filename
        
        
        test_data_path = os.path.join(os.path.dirname(__file__), 'test_data')
        if not os.path.exists(test_data_path):
            os.makedirs(test_data_path, exist_ok=True)
        # save res4 using pickle
        with open(os.path.join(test_data_path, "res4.pkl"), "wb") as f:
            pickle.dump(res4, f)

       
        #save the result to a file
        

    

if __name__ == '__main__':
    unittest.main()
