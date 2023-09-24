import os
import openai
import json
import mdutils
import sys
import base64
import subprocess
from datetime import datetime

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)
        
def git_operations(pat):
    current_date = datetime.now().strftime('%Y-%m-%d-%H-%M')
    b64_pat = base64.b64encode(f":{pat}".encode()).decode()
    branch_name = f"wiki-{current_date}"

    try:
        subprocess.run(["git", "config", "--global", "user.email", "azure-pipeline@coso.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "Azure Pipeline"], check=True)
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(["git", "-c", f"http.extraHeader=Authorization: Basic {b64_pat}", "add", "."], check=True)
        subprocess.run(["git", "-c", f"http.extraHeader=Authorization: Basic {b64_pat}", "commit", "-m", "Update WIKI"], check=True)
        subprocess.run(["git", "-c", f"http.extraHeader=Authorization: Basic {b64_pat}", "push", "--set-upstream", "origin", branch_name ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during Git operations: {str(e)}")
    print('Git commands completed')

def get_openai_explanation(systemmessage, text, openai_config):

    if (openai_config['url'] is None or openai_config['url'] == '') and (openai_config['modelname'] is None or openai_config['modelname'] == '') and (openai_config['api_key'] is None or openai_config['api_key'] == ''): 
        return ''
    if openai_config['url'] is None or openai_config['url'] == '':
        return 'OpenAI URL is not configured'
    if openai_config['modelname'] is None or openai_config['modelname'] == '':
        return 'OpenAI Modelname is not configured'
    if openai_config['api_key'] is None or openai_config['api_key'] == '':
        return 'OpenAI API Key is not configured'
    
    if os.path.exists('export/openai.json'):
        with open('export/openai.json', 'r') as json_file:
            openai_content = json.load(json_file)
    else:
        openai_content = []

    matching = next((item for item in openai_content if item["text"] == text), None)
    if matching is not None:
        return matching["content"]
    
    openai.api_key = openai_config['api_key']
    openai.api_type = "azure"
    openai.api_base = openai_config['url']
    openai.api_version = "2023-03-15-preview"
    messages = [{"content": systemmessage, "role": "assistant"}, {"content": text, "role": "user"}]
    response = openai.ChatCompletion.create(
      engine=openai_config['modelname'],
      messages = messages,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None)
    
    content = response.choices[0].message.content
    openai_content.append({"text": text, "content": content, "date": datetime.now().strftime('%B %d, %Y %H:%M:%S')})
    with open('export/openai.json', 'w') as outfile:
        json.dump(openai_content, outfile, indent=10)
    return content

def create_mdMCode(workspace_name, dataset, dataset_path, openai_config):
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    mdMCode = mdutils.MdUtils(file_name=os.path.join(dataset_path, 'mcode'))
    mdMCode.new_header(level=1, title='M Code')
    list_of_rows = []
    list_of_rows.extend(['Dataset', f"[{dataset['name']}](./../{dataset['name'].replace(' ', '-')}.md)"])
    list_of_rows.extend(['Workspace', f"[{workspace_name}](../../Workspaces/{workspace_name.replace(' ', '-')}.md)"]) 
    mdMCode.new_table(columns=2, rows=2, text=list_of_rows, text_align='left')

    tables = dataset['tables']
    for table in tables:
        calculated_table_columns = [column for column in table['columns'] if column.get('columnType') == 'CalculatedTableColumn']
        if len(calculated_table_columns) == 0:
            mdMCode.new_header(level=2, title='Table: ' + table['name'])
            mdMCode.insert_code(table['source'][0]['expression'], 'm')
            gpt_response = get_openai_explanation("Explain the following M Code:", table['source'][0]['expression'], openai_config)
            mdMCode.new_paragraph(gpt_response)
    
    parameters = [parameter for parameter in dataset['expressions'] if 'IsParameter' in parameter.get('expression', '')]        
    if len(parameters) > 0:
        for parameter in parameters:
            mdMCode.new_header(level=2, title='Parameter: ' + parameter['name'])
            if parameter.get('description') is not None:
                mdMCode.new_paragraph(parameter['description'])
            mdMCode.insert_code(parameter['expression'], 'm')
            gpt_response = get_openai_explanation("Explain the following M Code of a Parameter:", parameter['expression'], openai_config)
            mdMCode.new_paragraph(gpt_response)

    if 'roles' in dataset and len(dataset['roles']) > 0:
        roles = dataset['roles']
        mdMCode.new_header(level=2, title='Roles')
        for role in roles:
            mdMCode.new_header(level=3, title=role['name'])
            mdMCode.new_paragraph('Model Permission: ' + role['modelPermission'])
            if 'tablePermissions' in role and len(role['tablePermissions']) > 0:
                for table_row in role['tablePermissions']:
                    mdMCode.new_paragraph(table_row['name'])
                    mdMCode.insert_code(table_row['filterExpression'], 'm')
                    gpt_response = get_openai_explanation("Explain the following M Code of a Role:", table_row['filterExpression'], openai_config) 
                    mdMCode.new_paragraph(gpt_response)

    mdMCode.create_md_file()
    print(dataset_path + '/mcode created')

def create_mdDAX(workspace_name, dataset, dataset_path, openai_config):
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    
    mdDAX = mdutils.MdUtils(file_name=os.path.join(dataset_path, 'dax'))
    mdDAX.new_header(level=1, title='DAX')
    list_of_rows = []
    list_of_rows.extend(['Dataset', f"[{dataset['name']}](./../{dataset['name'].replace(' ', '-')}.md)"])
    list_of_rows.extend(['Workspace', f"[{workspace_name}](../../Workspaces/{workspace_name.replace(' ', '-')}.md)"]) 
    mdDAX.new_table(columns=2, rows=2, text=list_of_rows, text_align='left')

    tables = dataset['tables']
    for table in tables:
        calculated_table_columns = [column for column in table['columns'] if column.get('columnType') == 'CalculatedTableColumn']
        calculated_columns = [column for column in table['columns'] if column.get('columnType') == 'Calculated' and column.get('expression') is not None]
        measures = [measure for measure in table['measures'] if measure.get('expression') is not None]
        if len(calculated_columns) > 0 or len(measures) > 0 or len(calculated_table_columns) > 0:
            mdDAX.new_header(level=2, title='Table: ' + table['name'])
            if len(calculated_table_columns) > 0:
                mdDAX.insert_code(table['source'][0]['expression'], 'dax')
                gpt_response = get_openai_explanation("Explain the following DAX Code:", table['source'][0]['expression'], openai_config)
                mdDAX.new_paragraph(gpt_response)
            if len(measures) > 0:
                mdDAX.new_header(level=3, title='Measures:')
                for measure in measures:
                    mdDAX.insert_code(measure['name'] + ' = ' + measure['expression'], 'dax')
                    gpt_response = get_openai_explanation("Explain the following DAX Code:", measure['expression'], openai_config)
                    mdDAX.new_paragraph(gpt_response)
            if len(calculated_columns) > 0:
                mdDAX.new_header(level=3, title='Calculated Columns:')
                for column in calculated_columns:
                    mdDAX.insert_code(column['name'] + ' = ' + column['expression'], 'dax')
                    gpt_response = get_openai_explanation("Explain the following DAX Code:", column['expression'], openai_config)   
                    mdDAX.new_paragraph(gpt_response)

    mdDAX.create_md_file()
    print(dataset_path + '/dax created')

def create_mdWorkspace(workspace, wiki_path, wiki_name, list_of_total_reports, openai_config):
    workspace_path = os.path.join(wiki_path, "Workspaces")
    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path)
    
    mdWorkspace = mdutils.MdUtils(file_name=os.path.join(workspace_path, wiki_name))
    mdWorkspace.new_header(level=1, title=workspace['name'])
    list_of_rows = []
    list_of_rows.extend(['Workspace ID', workspace['id']])
    list_of_rows.extend(['Type', workspace['type']])
    list_of_rows.extend(['State', workspace['state']])
    mdWorkspace.new_table(columns=2, rows=3, text=list_of_rows, text_align='left')

    datasets = workspace['datasets']

    mdWorkspace.new_header(level=2, title=workspace['name'])
    mdWorkspace.new_header(level=3, title='Datasets')

    list_of_datasets = []
    list_of_datasets.extend(['Dataset Name', 'Last Modified'])

    for dataset in datasets:
        try:
            list_of_datasets.extend([f"[{dataset['name']}](../Datasets/{dataset['name'].replace(' ', '-')}.md)", datetime.strptime(dataset['createdDate'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
        except:
            list_of_datasets.extend([f"[{dataset['name']}](../Datasets/{dataset['name'].replace(' ', '-')}.md)", dataset['createdDate']])
        create_mdDataset(workspace['name'], dataset, wiki_path, dataset['name'].replace(' ', '-'), list_of_total_reports, openai_config) 

    mdWorkspace.new_table(columns=2, rows=len(list_of_datasets)//2, text=list_of_datasets, text_align='left')
    mdWorkspace.new_header(level=3, title='Reports')
    reports = sorted(workspace['reports'], key=lambda x: x['modifiedDateTime'], reverse=True)

    list_of_reports = []
    list_of_reports.extend(['Report Name', 'Last Modified'])

    for report in reports:
        try:
            list_of_reports.extend([f"[{report['name']}](../Reports/{report['name'].replace(' ', '-')}.md)", datetime.strptime(report['modifiedDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
        except:
            list_of_reports.extend([f"[{report['name']}](../Reports/{report['name'].replace(' ', '-')}.md)", report['modifiedDateTime']])
        create_mdReport(workspace['name'], report, wiki_path, report['name'].replace(' ', '-'), dataset['name'])

    columns = 2
    mdWorkspace.new_table(columns=columns, rows=len(list_of_reports)//columns, text=list_of_reports, text_align='left')
    mdWorkspace.create_md_file()

    print(workspace_path + '/' + wiki_name + ' created')

def create_mdDataset(workspace_name, dataset, wiki_path, wiki_name, list_of_total_reports, openai_config):
    datasets_path = os.path.join(wiki_path, "Datasets")
    if not os.path.exists(datasets_path):
        os.makedirs(datasets_path)

    mdDataset = mdutils.MdUtils(file_name=os.path.join(datasets_path, wiki_name))
    mdDataset.new_header(level=1, title=dataset['name'])
    list_of_rows = []
    list_of_rows.extend(['Dataset ID', dataset['id']])
    list_of_rows.extend(['Workspace', f"[{workspace_name}](../Workspaces/{workspace_name.replace(' ', '-')}.md)"]) 
    list_of_rows.extend(['Configured By', dataset['configuredBy']])
    list_of_rows.extend(['Target Storage Mode', dataset['targetStorageMode']])
    list_of_rows.extend(['Content Provider Type', dataset['contentProviderType']])
    try:
        list_of_rows.extend(['Created Date', datetime.strptime(dataset['createdDate'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
    except:
        list_of_rows.extend(['Created Date', dataset['createdDate']]) 
    list_of_rows.extend(['MCode', f"[M Code](./{wiki_name}/mcode.md)"])
    list_of_rows.extend(['DAX', f"[DAX](./{wiki_name}/dax.md)"])
    
    columns = 2
    mdDataset.new_table(columns=columns, rows=len(list_of_rows)//columns, text=list_of_rows, text_align='left')
    
    create_mdMCode(workspace_name, dataset, os.path.join(datasets_path, wiki_name), openai_config)
    create_mdDAX(workspace_name, dataset, os.path.join(datasets_path, wiki_name), openai_config)

    mdDataset.new_header(level=2, title='Reports')
    list_of_reports = []
    list_of_reports.extend(['Report', 'Workspace'])
    for report in list_of_total_reports:
        if report['datasetId'] == dataset['id']:
            list_of_reports.extend([f"[{report['name']}](../Reports/{report['name'].replace(' ', '-')}.md)", f"[{workspace_name}](../Workspaces/{workspace_name.replace(' ', '-')}.md)"])
    
    columns = 2
    mdDataset.new_table(columns=columns, rows=len(list_of_reports)//columns, text=list_of_reports, text_align='left')

    mdDataset.create_md_file()
    print(datasets_path + '/' + wiki_name + ' created')

def create_mdReport(workspace_name, report, wiki_path, wiki_name, dataset_name):
    report_path = os.path.join(wiki_path, "Reports")
    if not os.path.exists(report_path):
        os.makedirs(report_path)

    mdReport = mdutils.MdUtils(file_name=os.path.join(report_path, wiki_name))
    mdReport.new_header(level=1, title=report['name'])
    list_of_rows = []
    list_of_rows.extend(['Report ID', report['id']])
    list_of_rows.extend(['Workspace', f"[{workspace_name}](../Workspaces/{workspace_name.replace(' ', '-')}.md)"])  
    list_of_rows.extend(['Dataset', f"[{dataset_name}](../Datasets/{dataset_name.replace(' ', '-')}.md)"])
    list_of_rows.extend(['Created By', report['createdBy']])
    try:
        list_of_rows.extend(['Created Date', datetime.strptime(report['createdDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
    except:
        list_of_rows.extend(['Created Date', report['createdDateTime']])
    list_of_rows.extend(['Modified By', report['modifiedBy']])
    try:
        list_of_rows.extend(['Modified Date', datetime.strptime(report['modifiedDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
    except:
        list_of_rows.extend(['Modified Date', report['modifiedDateTime']])

    columns = 2
    mdReport.new_table(columns=columns, rows=len(list_of_rows)//columns, text=list_of_rows, text_align='left')
    mdReport.create_md_file()
    print(report_path + '/' + wiki_name + ' created')

def create_mdWorkspaces(workspaces, wiki_path, scan_date, openai_config):
    mdWorkspaces = mdutils.MdUtils(file_name=os.path.join(wiki_path, 'Workspaces'))
    mdWorkspaces.new_header(level=1, title='Workspace List')
    mdWorkspaces.new_paragraph("Last Scan: " + scan_date)
    mdWorkspaces.new_paragraph("Last Wiki updated: " + datetime.now().strftime('%B %d, %Y %H:%M:%S'))
    mdWorkspaces.new_line()
    list_of_workspaces = []
    list_of_workspaces.extend(['Workspace Name', 'ID'])
    list_of_total_reports = []

    for workspace in workspaces:
        for report in workspace['reports']:
            list_of_total_reports.append({'workspace': workspace['name'], 'id': report['id'], 'name': report['name'], 'datasetId': report['datasetId']})
    
    for workspace in workspaces:
        workspace_wiki_name = workspace['name'].replace(' ', '-')
        workspace_wiki_url = f"[{workspace['name']}](./Workspaces/{workspace_wiki_name}.md)"
        create_mdWorkspace(workspace, wiki_path, workspace_wiki_name, list_of_total_reports,openai_config)
        list_of_workspaces.extend([workspace_wiki_url, workspace['id']])
        mdWorkspaces.new_line()

    mdWorkspaces.new_table(columns=2, rows=len(list_of_workspaces)//2, text=list_of_workspaces, text_align='left')
    mdWorkspaces.create_md_file()

def create_wiki(workspaces, work_dir, scan_date, openai_config):
    wiki_path = os.path.join(work_dir, 'wiki')
    if not os.path.exists(wiki_path):
        os.makedirs(wiki_path)

    create_mdWorkspaces(workspaces, wiki_path, scan_date, openai_config)
    print('WIKI created')

def main():
    work_dir = sys.argv[1]
    pat = sys.argv[2]
    openai_url = sys.argv[3]
    openai_modelname = sys.argv[4]
    openai_api_key = sys.argv[5]

    openai_config = {"url": openai_url, "modelname": openai_modelname, "api_key": openai_api_key}

    print('Work Directory: ' + work_dir)
    print('PAT: ' + pat)
    print('OpenAI URL: ' + openai_config['url'])
    print('OpenAI Model Name: ' + openai_config['modelname'])
    print('OpenAI API Key: ' + openai_config['api_key'])

    for file in os.listdir('export'):
        print(file)
        if file.startswith('scanResult'):
            data = load_data(os.path.join('export', file))
            scan_date = data['lastScanDate']
            workspaces = data['workspaces']
            create_wiki(workspaces, work_dir, scan_date, openai_config)

    git_operations(pat)

if __name__ == '__main__':
    main()
