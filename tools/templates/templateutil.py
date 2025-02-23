import os
import yaml

def compose_templates(param, templates):
    all_templates = get_templates()

    composed_templates = []

    for template in all_templates:
        if template['filename'] in templates:
            composed_templates.append(template)

    root_template = None

    with open(os.path.join(os.path.dirname(__file__), '../../wf_templates/wf-template.yaml'), 'r') as file:
        root_template = yaml.safe_load(file)


    for composeitem in composed_templates:
        filename = composeitem['filename']
        with open(os.path.join(os.path.dirname(__file__), '../../wf_templates', filename), 'r') as file:
            template = yaml.safe_load(file)
            

    return composed_templates

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
                    description = item.get('metadata', {}).get('annotations', {}).get('description', 'No description available')
                    templates.append({'filename': filename, 'description': description})
    
    #print(templates)
    return templates

if __name__ == "__main__":
    get_templates()