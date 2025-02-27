import copy
import os
import yaml


new_step = [{
    "name": "new-step",
    "template": "new_template",
    "arguments": {
        "parameters": [
            {"name": "input_param", "value": "value"}
        ]
    }
}]

def get_step_config(name, previous_step_name=None):
    new_step_json = copy.deepcopy(new_step)
    new_step_json[0]["name"] = f"step-{name}" 
    new_step_json[0]["template"] = name

    if previous_step_name is None:
        new_step_json[0]["arguments"]["parameters"][0]["value"] = "{{workflow.parameters.intput_param}}"
    else:        
        param_value = f"{{{{steps.step-{previous_step_name}.outputs.parameters.stepResult}}}}"
        new_step_json[0]["arguments"]["parameters"][0]["value"] = param_value
    return new_step_json

def find_template_by_name(name, composed_templates):
    for template in composed_templates:
        if template.get('name') == name:
            return template
    return None

def compose_templates(input_param, templates):
    all_templates = get_templates()

    composed_templates = []

    for template in templates:
        for existing_template in all_templates:
            if existing_template['name'] == template:
                composed_templates.append(existing_template)
      
    root_template = None

    with open(os.path.join(os.path.dirname(__file__), '../../wf_templates/wf-template.yaml'), 'r') as file:
        root_template = yaml.safe_load(file)

    for param in root_template.get("spec", {}).get("arguments", {}).get("parameters", []):
        if param.get("name") == "intput_param":
            param["value"] = input_param


    # Composition, let's start by finding the steps template
    template_steps = None
    for template in root_template['spec']['templates']:
        if template.get('name') == 'template-steps':
            template_steps = template
            break

    if template_steps is None:
        raise ValueError("Could not find 'template-steps' template")
    
    prev_template_name = None    
    last_parallel_step = None
    for composeitem in composed_templates:
        filename = composeitem['filename']
        template = None
        with open(os.path.join(os.path.dirname(__file__), '../../wf_templates', filename), 'r') as file:
            template = yaml.safe_load(file)
        
        if template is None:
            raise ValueError(f"Could not load template {filename}")
        
        

        for subtemplate in template:

            template_name = subtemplate.get('name')
            if template_name is None:
                raise ValueError(f"Template {filename} does not have a name")
            root_template['spec']['templates'].append(subtemplate)
            step_config = get_step_config(template_name, prev_template_name)
            
            
            
            # find the composed template with the same name
            composed_template = find_template_by_name(template_name, composed_templates)

            if composed_template is None:
                raise ValueError(f"Could not find composed template with name {template_name}")
            
            is_parallel = composed_template.get("template", {}).get("metadata", {}).get("annotations", {}).get("parallel", False)

            if is_parallel and template_steps.get("steps") != None:
                if last_parallel_step != None:
                    last_parallel_step.append(step_config[0])
                else:
                    template_steps.setdefault('steps', []).append(step_config)
                last_parallel_step = template_steps["steps"][-1]
            else:
                template_steps.setdefault('steps', []).append(step_config)
                last_parallel_step = None
                prev_template_name = template_name
                
            
            

    output_path = os.path.join(os.path.dirname(__file__), './wf-composed.yaml')        
    with open(output_path, 'w') as file:
        #print(f"Writing template: {root_template}")  # Add debug print
        yaml.dump(root_template, file)
    
    yaml_str = yaml.dump(root_template)

    return yaml_str

def get_templates_filtered_templates(filters):
    templates = get_templates()
    filtered_templates = []
    for template in templates:
        if any(filter in template['name'] for filter in filters):
            filtered_templates.append(template)
    return filtered_templates

def get_templates():
    templates = []
    templates_dir = os.path.join(os.path.dirname(__file__), '../../wf_templates')

    if not os.path.exists(templates_dir):
        print(f"Directory {templates_dir} does not exist.")
        return templates

    for filename in os.listdir(templates_dir):
        if filename.startswith('template-') and filename.endswith('.yaml'):
            with open(os.path.join(templates_dir, filename), 'r') as file:
                template = yaml.safe_load(file)
                for item in template:
                    template_name = item.get('name')
                    description = item.get('metadata', {}).get('annotations', {}).get('description', 'No description available')
                    templates.append({'filename': filename, 'description': description, 'name': template_name, 'template': item})
    
    #print(templates)
    return templates

if __name__ == "__main__":
    get_templates()