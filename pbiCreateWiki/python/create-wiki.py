import os
import openai
import json
import mdutils
import sys
import base64
import subprocess
from datetime import datetime

def load_data():
    with open('export/scanResult.json', 'r') as file:
        return json.load(file)
    
def get_openai_explanation(systemmessage, text, openai_url, openai_modelname, openai_api_key):
    openai.api_key = openai_api_key
    openai.api_type = "azure"
    openai.api_base = openai_url
    openai.api_version = "2023-03-15-preview"
    messages = [{"content": systemmessage, "role": "assistant"}, {"content": text, "role": "user"}]
    response = openai.ChatCompletion.create(
      engine=openai_modelname,
      messages = messages,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None)
    return response.choices[0].message.content

def prepare_markdown(workspace, scan_date, mdIndex, wiki_path, openai_url,  openai_modelname, openai_api_key):
    reports = sorted(workspace['reports'], key=lambda x: x['modifiedDateTime'], reverse=True)
    datasets = workspace['datasets']
    datasets_dict = {obj["id"]: obj for obj in datasets}

    mdIndex.new_header(level=1, title=workspace['name'])
    mdIndex.new_paragraph("Last Scan: " + scan_date)
    mdIndex.new_paragraph("Last Wiki updated: " + datetime.now().strftime('%B %d, %Y %H:%M:%S'))
    mdIndex.new_header(level=2, title='Reports')

    list_of_datasets = []
    list_of_datasets.extend(['Dataset Name', 'Last Modified'])

    for dataset in datasets:
        dataset_wiki_name = dataset['name'].replace(' ', '-')
        list_of_datasets.extend([f"[{dataset['name']}](./{dataset_wiki_name}.md)", datetime.strptime(dataset['createdDate'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])  
        dataset_path = os.path.join(wiki_path, "Datasets")
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)

        mdOverview = mdutils.MdUtils(file_name=os.path.join(dataset_path, dataset_wiki_name))
        mdOverview.new_header(level=1, title=dataset['name'])
        list_of_rows = []
        list_of_rows.extend(['Dataset ID', dataset['id']])
        list_of_rows.extend(['Configured By', dataset['configuredBy']])
        list_of_rows.extend(['Target Storage Mode', dataset['targetStorageMode']])
        list_of_rows.extend(['Content Provider Type', dataset['contentProviderType']])
        list_of_rows.extend(['Created Date', datetime.strptime(dataset['createdDate'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
        mdOverview.new_table(columns=2, rows=5, text=list_of_rows, text_align='left')
        
        if 'roles' in dataset and len(dataset['roles']) > 0:
            roles = dataset['roles']
            mdOverview.new_header(level=2, title='Roles')
            for role in roles:
                mdOverview.new_header(level=3, title=role['name'])
                mdOverview.new_paragraph('Model Permission: ' + role['modelPermission'])
                if 'tablePermissions' in role and len(role['tablePermissions']) > 0:
                    for table_row in role['tablePermissions']:
                        mdOverview.new_paragraph(table_row['name'])
                        mdOverview.insert_code(table_row['filterExpression'], 'm')
        mdOverview.create_md_file()

    list_of_reports = []
    list_of_reports.extend(['Report Name', 'Last Modified'])

    for report in reports:
        report_wiki_name = report['name'].replace(' ', '-')
        list_of_reports.extend([f"[{report['name']}](./{report_wiki_name}.md)", datetime.strptime(report['modifiedDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
        report_path = os.path.join(wiki_path, report_wiki_name)
        if not os.path.exists(report_path):
            os.makedirs(report_path)

        mdOverview = mdutils.MdUtils(file_name=os.path.join(wiki_path, report_wiki_name))
        mdOverview.new_header(level=1, title=report['name'])
        dataset = datasets_dict[report['datasetId']]
        dataset_wiki_path = 'Datasets/' + dataset['name'].replace(' ', '-') + '.md'

        list_of_rows = []
        list_of_rows.extend(['Report ID', report['id']])
        list_of_rows.extend(['Dataset Name', f"[{dataset['name']}](./{dataset_wiki_path})"])
        list_of_rows.extend(['Created By', report['createdBy']])
        list_of_rows.extend(['Created Date', datetime.strptime(report['createdDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
        list_of_rows.extend(['Modified By', report['modifiedBy']])
        list_of_rows.extend(['Modified Date', datetime.strptime(report['modifiedDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])

        mdOverview.new_table(columns=2, rows=6, text=list_of_rows, text_align='left')    
        mdOverview.create_md_file()

        mdMCode = mdutils.MdUtils(file_name=os.path.join(report_path, 'mcode'))
        mdMCode.new_header(level=1, title='M Code')
        
        mdDAX = mdutils.MdUtils(file_name=os.path.join(report_path, 'dax'))
        mdDAX.new_header(level=1, title='DAX')
        
        tables = dataset['tables']
        for table in tables:
            
            calculated_table_columns = [column for column in table['columns'] if column.get('columnType') == 'CalculatedTableColumn']
            calculated_columns = [column for column in table['columns'] if column.get('columnType') == 'Calculated' and column.get('expression') is not None]
            measures = [measure for measure in table['measures'] if measure.get('expression') is not None]
            if len(calculated_table_columns) == 0:
                mdMCode.new_header(level=2, title='Table: ' + table['name'])
                gpt_response = get_openai_explanation("Explain the following M Code:", table['source'][0]['expression'], openai_url,  openai_modelname, openai_api_key)
                mdMCode.new_paragraph(gpt_response)
                mdMCode.insert_code(table['source'][0]['expression'], 'm')

            if len(calculated_columns) > 0 or len(measures) > 0 or len(calculated_table_columns) > 0:
                mdDAX.new_header(level=2, title='Table: ' + table['name'])
                if len(calculated_table_columns) > 0:
                    mdDAX.insert_code(table['source'][0]['expression'], 'dax')
                if len(measures) > 0:
                    mdDAX.new_header(level=3, title='Measures:')
                    for measure in measures:
                        mdDAX.insert_code(measure['name'] + ' = ' + measure['expression'], 'dax')
                if len(calculated_columns) > 0:
                    mdDAX.new_header(level=3, title='Calculated Columns:')
                    for column in calculated_columns:
                        mdDAX.insert_code(column['name'] + ' = ' + column['expression'], 'dax')
        
        parameters = [parameter for parameter in dataset['expressions'] if 'IsParameter' in parameter.get('expression', '')]        
        if len(parameters) > 0:
            for parameter in parameters:
                mdMCode.new_header(level=2, title='Parameter: ' + parameter['name'])
                if parameter.get('description') is not None:
                    mdMCode.new_paragraph(parameter['description'])
                gpt_response = get_openai_explanation("Explain the following M Code of a Parameter:", parameter['expression'], openai_url,  openai_modelname, openai_api_key)
                mdMCode.new_paragraph(gpt_response)
                mdMCode.insert_code(parameter['expression'], 'm')

        mdMCode.create_md_file()
        mdDAX.create_md_file()

    columns = 2
    mdIndex.new_table(columns=columns, rows=len(list_of_reports)//columns, text=list_of_reports, text_align='left')

    mdIndex.new_line()
    mdIndex.new_line()
    return mdIndex

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

def main():
    work_dir = sys.argv[1]
    pat = sys.argv[2]
    openai_url = sys.argv[3]
    openai_modelname = sys.argv[4]
    openai_api_key = sys.argv[5]

    data = load_data()
    scan_date = data['lastScanDate']
    workspaces = data['workspaces']

    wiki_path = os.path.join(work_dir, 'wiki')
    if not os.path.exists(wiki_path):
        os.makedirs(wiki_path)

    mdIndex = mdutils.MdUtils(file_name=os.path.join(wiki_path, 'Workspaces-Scan'))
    for workspace in workspaces:
        mdIndex = prepare_markdown(workspace, scan_date, mdIndex, wiki_path, openai_url, openai_modelname, openai_api_key)
    mdIndex.create_md_file()
    git_operations(pat)

if __name__ == '__main__':
    main()
