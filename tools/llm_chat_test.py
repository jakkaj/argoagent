import unittest

from templates.templateutil import compose_templates
from mcptools.argorunner import print_mcp_tools
from autogen_ext.tools.mcp import mcp_server_tools, StdioMcpToolAdapter, StdioServerParams

class TestLLMChat(unittest.TestCase):
    def test_template_build(self):
        templates = list()
        templates.append("template-wikistep.yaml")
        templates.append("template-summarystep.yaml")

        compose = compose_templates("Bendigo", templates)

    async def test_wf_run(self):
        templates = list()
        templates.append("template-wikistep.yaml")
        templates.append("template-summarystep.yaml")

        compose = compose_templates("Bendigo", templates)

        print (compose)
        argo_system_mcp_server = StdioServerParams(
            command="/workspaces/argoagent/bin/mcp-argo-server",        
        )
        argo_tools = await mcp_server_tools(argo_system_mcp_server)
        print_mcp_tools(argo_tools)       
    

    

if __name__ == '__main__':
    unittest.main()
