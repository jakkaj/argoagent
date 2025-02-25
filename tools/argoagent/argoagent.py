import json
import os

from autogen_core import CancellationToken

from templates.templateutil import compose_templates, get_templates_filtered_templates
from tools.llm_chat import extract_json
from argoagent.argorunner import ArgoSubmitConfigModel, print_mcp_tools
from autogen_ext.tools.mcp import mcp_server_tools, StdioMcpToolAdapter, StdioServerParams

config_sample = {
    "name": "wikiagent",
    "description": "Can search wikipedia for things",
    "templates":[
        "wikistep",
        "summarystep"
    ],
    "extra_initial_prompt_instruction": "Don't summarise unless the user explicitly asks you to"
}


class ArgoAgent:

    template_prompt = """
You have a list of templates to solve the query. These templates will allow you to compose a workflow to solve the query. 
The workflow will run all at once an you will get the final result, you will not get see intermediate results.

{extra_initial_prompt_instruction}

The query is: {query}
The templates are:
#### templates ####

{wf_templates}

#### end templates ####

You only need to provide a param to the outer template, each step does not need to be provided with a param.

Be sure to read the instructions in the description for the first template to ensure you prepare the input query properly. 

You do not need to use all the templates. Think of them as tools to sovle the query. 

Example: if you were to receive information on templates like this: [{{'name': 'wolfram', 'description': 'Queries the Wolfram API with a search query'}}, {{'name': 'google', 'description': 'This searches google for the input text'}}]

Please compose it in this way. The example  here is "please find me information on Bendigo and summarise it"

{{
"param": "<wikipedia search term>",
"steps": [
    "<name of template 1>",
    "<additional templates only if needed by user query>"
]
}}

However please only include the steps you need to precicely solve the users query. 

**Only output the json data and nothing else. **   

"""



    def __init__(self, config, llm):
        if config is None:
            config = json.dumps(config_sample)
        self.config = config       
        self.llm = llm
        self.templates = None
        
        self.llm_template_string = ""
        self.name = None
        self.description = None
        self.extra_initial_prompt_instruction = ""

        self.messages = list()

        ## Setting up for a run
        self.ready_query = None
        self.ready_prompt = None

        ## composing
        self.llm_selected_template_string = None
        self.wf_input_param = None
        self.template_to_compose = None
        self.composed_templates = None

        ## running
        self.argo_result = None
        self.result_for_llm = None

        self.final_result = None

        self.workflow_output_files = None

        self.setup()        
    
    def setup(self):
        #parse the config
        parsed_config = None
        try:
            parsed_config = json.loads(self.config)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return
        
        self.name = parsed_config["name"]
        self.description = parsed_config["description"]

        if "extra_initial_prompt_instruction" in parsed_config:
            self.extra_initial_prompt_instruction = parsed_config["extra_initial_prompt_instruction"]

        #get the templates
        template_filters = parsed_config["templates"]
        self.templates = get_templates_filtered_templates(template_filters)
        self._get_templates_for_prompt()

    def _get_templates_for_prompt(self):        
        
        for template in self.templates:
            self.llm_template_string += f"\n{template['name']}: {template['description']}\n"

    def _set_query(self, query):
        self.ready_query = query
        
        prompt = self.template_prompt.format(query=query, 
                                             wf_templates=self.llm_template_string,
                                             extra_initial_prompt_instruction=self.extra_initial_prompt_instruction)
    
        self.ready_query = prompt

    def _add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def _run_llm_compose_templates(self):
        self._add_message("user", self.ready_query)       
        result = self.llm.send(self.messages)
        self._add_message("assistant", result)
        self.llm_selected_template_string = result

    def _build_composed_templates(self):
        json_only = extract_json(self.llm_selected_template_string)
        if json_only == None:
            return "LLM did not return a valid JSON"
        templates = list()

        for step in json_only["steps"]:
            # get the template
            templates.append(step)
            
        self.template_to_compose = templates

        param = json_only["param"]
        self.wf_input_param = param
        self.composed_templates = compose_templates(param, templates)
        # with open("composed_templates.json", "w") as f:
        #     json.dump(self.composed_templates, f, indent=4)
        print(self.composed_templates)

    async def run_workflow(self, query):
        self._set_query(query)
        self._run_llm_compose_templates()
        self._build_composed_templates()       

        save_path = None

        argo_system_mcp_server = StdioServerParams(
            command="/workspaces/argoagent/bin/mcp-argo-server",        
        )

        argo_tools = await mcp_server_tools(argo_system_mcp_server)
        #print_mcp_tools(argo_tools)       
        token = CancellationToken()
        argo_config_wait = ArgoSubmitConfigModel(manifest=self.composed_templates, namespace="argo", wait=True)
        res4 = await argo_tools[0].run(argo_config_wait, token)

        self.argo_result = res4

        for item in res4:
            if save_path is None:
                save_path = os.path.join(os.path.dirname(__file__), '../outputs', item.text)
            #print(f"Item: {item.text}")
            #f.write(f"{item.text}\n")
            if item.text.startswith("{"):
                self.save_run_artefacts_from_nodes_string(save_path, item.text) 
                llm_text = self.get_run_artefacts_for_llm(item.text)
                self.result_for_llm = llm_text
    
    def process_final_result(self):
        
        final_prompt = f"""
We have the results back from the workflow> use them to answer the users initial query. 
Reminder, initial query was: {self.ready_query}
#### results from workflow ###
{self.result_for_llm}
#### end results from workflow ###
        """
        self._add_message("user", final_prompt)
        result = self.llm.send(self.messages)
        self._add_message("assistant", result)

        self.final_result = result
        return self.final_result

    def get_run_artefacts_for_llm(self, string_nodes):
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

    def save_run_artefacts_from_nodes_string(self, path, string_nodes):
        # parse string_nodes to json
        nodes = None
        try:
            nodes = json.loads(string_nodes)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return
        
        wrote_files = list()

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
                wrote_files.append(file_path)
        self.workflow_output_files = wrote_files