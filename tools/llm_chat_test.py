import os
import pickle
import tempfile
import unittest

from autogen_core import CancellationToken

from templates.templateutil import compose_templates
from argoagent.argoagent import get_run_artefacts_for_llm, save_run_artefacts_from_nodes_string
from argoagent.argorunner import ArgoSubmitConfigModel, print_mcp_tools
from autogen_ext.tools.mcp import mcp_server_tools, StdioMcpToolAdapter, StdioServerParams

class TestLLMChat(unittest.IsolatedAsyncioTestCase):
    def test_template_build(self):
        templates = list()
        templates.append("template-wikistep.yaml")
        templates.append("template-summarystep.yaml")

        compose = compose_templates("Bendigo", templates)

    async def test_parsers(self):
        save_path = None
        test_data_path = os.path.join(os.path.dirname(__file__), 'test_data')
        
        res4 = None
        with open(os.path.join(test_data_path, "res4.pkl"), "rb") as f:
            res4 = pickle.load(f)

        
        for item in res4:
            if save_path is None:
                save_path = os.path.join(os.path.dirname(__file__), '../outputs', item.text)
            #print(f"Item: {item.text}")
            #f.write(f"{item.text}\n")
            if item.text.startswith("{"):
                save_run_artefacts_from_nodes_string(save_path, item.text) 
                llm_text = get_run_artefacts_for_llm(item.text)
                print(llm_text)
                    


    async def test_wf_run(self):
        templates = list()
        templates.append("template-wikistep.yaml")
        templates.append("template-summarystep.yaml")

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
