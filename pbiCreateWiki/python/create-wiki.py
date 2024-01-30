import csv
import os
import openai
import json
import mdutils
import sys
import base64
import subprocess
import uuid
import re
from datetime import datetime

invalid_chars_regex = re.compile(r'[<>:"/\\|?*#\x00-\x1F]')
schema_item_regex = r'Schema="(.+?)",Item="(.+?)"'

def check_schema_item_in_string(s, schema, item):
    # Create the regular expression pattern using the provided schema and item
    pattern = f'Schema="{schema}",Item="{item}"'
    # Use re.search to find the first match in the string
    match = re.search(pattern, s)
    # If a match is found, return True, otherwise return False
    return match is not None

def get_clean_file_name(name):
    return f"{get_clean_name(name)}.md"

def get_clean_name(name):
    return invalid_chars_regex.sub('', name.replace(' ', '-')).lower()

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)
        
def git_operations(pat, branch_name):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "azure-pipeline@coso.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "Azure Pipeline"], check=True)
        if branch_name is None or branch_name == '':
            current_date = datetime.now().strftime('%Y-%m-%d-%H-%M')
            b64_pat = base64.b64encode(f":{pat}".encode()).decode()
            branch_name = f"wiki-{current_date}"
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(["git", "-c", f"http.extraHeader=Authorization: Basic {b64_pat}", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "-c", f"http.extraHeader=Authorization: Basic {b64_pat}", "commit", "-m", "Update WIKI"], check=True, capture_output=True)
        subprocess.run(["git", "-c", f"http.extraHeader=Authorization: Basic {b64_pat}", "push", "--set-upstream", "origin", branch_name ], check=True, capture_output=True)
        print('Git commands completed')

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during Git operations: {str(e)}")
        print(f"Git command: {e.cmd}")
        print(f"Git command output: {e.output}")
        print(f"Git command return code: {e.returncode}")
        print(f"Git command stderr: {e.stderr}")
        print(f"Git command stdout: {e.stdout}")
        print(f"Git command args: {e.args}")
        sys.exit(1)

def get_openai_explanation(systemmessage, text, openai_config):    
    if os.path.exists('export/openai.json'):
        with open('export/openai.json', 'r') as json_file:
            openai_content = json.load(json_file)
    else:
        openai_content = []

    matching = next((item for item in openai_content if item["text"] == text), None)
    if matching is not None:
        #print(f"OpenAI {text[:20]}... explanation found".replace("\n", ""))
        return matching["content"]

    if (openai_config['url'] is None or openai_config['url'] == '') or (openai_config['modelname'] is None or openai_config['modelname'] == '') or (openai_config['api_key'] is None or openai_config['api_key'] == ''): 
        #print('OpenAI configuration is not set. Skipping OpenAI explanation.')
        return ''
    try:
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
    except Exception as e:
        print(f"An error occurred during OpenAI explanation: {str(e)}")
        print(f"OpenAI text: {text}")
        return ''
    
    content = response.choices[0].message.content
    openai_content.append({"text": text, "content": content, "date": datetime.now().strftime('%B %d, %Y %H:%M:%S')})
    with open('export/openai.json', 'w') as outfile:
        json.dump(openai_content, outfile, indent=10)
    print(f"OpenAI {text[:20]}... explanation created".replace("\n", ""))
    return content

def create_mdTables(workspace_name, dataset, dataset_path, list_of_total_reports, list_of_total_mcode, openai_config):
    for table in dataset['tables']:
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
        mdTable = mdutils.MdUtils(file_name=os.path.join(dataset_path, get_clean_name(table['name'])))
        mdTable.new_header(level=1, title='Table: ' + table['name'])
        if table.get('source') is not None:
            gpt_response = get_openai_explanation("Explain the following M Code:", table['source'][0]['expression'], openai_config)
            mdTable.new_paragraph(gpt_response)
            mdTable.insert_code(table['source'][0]['expression'], 'm')
             # if schame and item is available, add it to the wiki
            match = re.search(schema_item_regex, table['source'][0]['expression'])
            list_mcreports_found = []
            if match:
                schema, item = match.groups()
                #print(f'Schema: {schema}, Item: {item}')
                for mc in list_of_total_mcode:
                    if check_schema_item_in_string(mc['mcode'], schema=schema, item=item):
                        datasetid = mc['datasetId']
                        reports = [report for report in list_of_total_reports if report['datasetId'] == datasetid]
                        for report in reports:
                            #print(f"Found MCode '{schema}' item '{item}':{report['name']} - {mc['datasetId']} - {mc['workspace']}")
                            mcr = mc.copy()
                            mcr['report'] = report
                            list_mcreports_found.append(mcr)
                        #print(f"Found MCode '{schema}' item '{item}': {mc['datasetId']} - {mc['datasetName']} - {mc['workspace']}")
            if len(list_mcreports_found) > 0:
                mdTable.new_header(level=2, title='Usage of similar Table')
                mdTable.new_paragraph('The following reports are using a similar table:')
                list_of_mc_found = []
                list_of_mc_found.extend(['Report', 'Dataset', 'Workspace'])
                for mc in list_mcreports_found:
                    list_of_mc_found.extend([f"[{mc['report']['name']}](../../Reports/{get_clean_file_name(mc['report']['name'])})",f"[{mc['datasetName']}](../../Datasets/{get_clean_file_name( mc['datasetName'] )})", f"[{mc['workspace']}](../../Workspaces/{get_clean_file_name( mc['workspace'] )})"])
                columns = 3
                mdTable.new_table(columns=columns, rows=len(list_of_mc_found)//columns, text=list_of_mc_found, text_align='left')
        mdTable.create_md_file()
        print(f"File {os.path.join(dataset_path, get_clean_name(table['name']))} created")
        

def create_mdMCode(workspace_name, dataset, dataset_path,list_of_total_mcode, openai_config):
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    mdMCode = mdutils.MdUtils(file_name=os.path.join(dataset_path, 'mcode'))
    mdMCode.new_header(level=1, title='M Code')
    list_of_rows = []
    list_of_rows.extend(['Dataset', f"[{dataset['name']}](./../{get_clean_file_name(dataset['name'])})"])
    list_of_rows.extend(['Workspace', f"[{workspace_name}](../../Workspaces/{get_clean_file_name(workspace_name)})"]) 
    mdMCode.new_table(columns=2, rows=2, text=list_of_rows, text_align='left')

    tables = dataset['tables']
    for table in tables:
        calculated_table_columns = [column for column in table['columns'] if column.get('columnType') == 'CalculatedTableColumn']
        if len(calculated_table_columns) == 0:
            mdMCode.new_header(level=2, title='Table: ' + table['name'])
            if table.get('source') is not None:
                mdMCode.insert_code(table['source'][0]['expression'], 'm')
                gpt_response = get_openai_explanation("Explain the following M Code:", table['source'][0]['expression'], openai_config)
                mdMCode.new_paragraph(gpt_response)

                # if schame and item is available, add it to the wiki
                match = re.search(schema_item_regex, table['source'][0]['expression'])
                list_mc_found = []
                if match:
                    schema, item = match.groups()
                    #print(f'Schema: {schema}, Item: {item}')
                    for mc in list_of_total_mcode:
                        if check_schema_item_in_string(mc['mcode'], schema=schema, item=item):
                            list_mc_found.append(mc)
                            #print(f"Found MCode '{schema}' item '{item}': {mc['datasetId']} - {mc['datasetName']} - {mc['workspace']}")
                if len(list_mc_found) > 0:
                    mdMCode.new_header(level=3, title='Similar Table')
                    list_of_mc_found = []
                    list_of_mc_found.extend(['Dataset', 'Workspace'])
                    for mc in list_mc_found:
                        list_of_mc_found.extend([f"[{mc['datasetName']}](../../Datasets/{get_clean_file_name( mc['datasetName'] )})", f"[{mc['workspace']}](../../Workspaces/{get_clean_file_name( mc['workspace'] )})"])
                    columns = 2
                    mdMCode.new_table(columns=columns, rows=len(list_of_mc_found)//columns, text=list_of_mc_found, text_align='left')


    parameters = [parameter for parameter in dataset.get('expressions', []) if 'IsParameter' in parameter.get('expression', '')]        
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
                    if table_row.get('filterExpression') is not None:
                        mdMCode.new_paragraph(table_row['name'])
                        mdMCode.insert_code(table_row['filterExpression'], 'm')
                        gpt_response = get_openai_explanation("Explain the following M Code of a Role:", table_row['filterExpression'], openai_config) 
                        mdMCode.new_paragraph(gpt_response)

    mdMCode.create_md_file()
    print(f"File {os.path.join(dataset_path, 'mcode')} created")

def create_mdDAX(workspace_name, dataset, dataset_path, openai_config):
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    
    mdDAX = mdutils.MdUtils(file_name=os.path.join(dataset_path, 'dax'))
    mdDAX.new_header(level=1, title='DAX')
    list_of_rows = []
    list_of_rows.extend(['Dataset', f"[{dataset['name']}](./../{get_clean_file_name(dataset['name'])})"])
    list_of_rows.extend(['Workspace', f"[{workspace_name}](../../Workspaces/{get_clean_file_name(workspace_name)})"]) 
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
    print(f"File {os.path.join(dataset_path, 'dax')} created")

def create_mdWorkspace(workspace, work_dir, wiki_path, wiki_name, list_of_total_reports, list_of_total_mcode,  openai_config):
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

    if 'users' in workspace and workspace['users'] and len(workspace['users']) > 0:
        mdWorkspace.new_header(level=2, title='Users')
        list_of_users = []
        list_of_users.extend(['User', 'User Type', 'Email', 'Workspace Access'])
        for user in workspace['users']:
            if user['displayName']:
                list_of_users.extend([f"[{user['displayName']}](../Users/{get_clean_file_name(user['displayName'])})", user['userType'], user['emailAddress'], user['groupUserAccessRight']])
        columns = 4
        mdWorkspace.new_table(columns=columns, rows=len(list_of_users)//columns, text=list_of_users, text_align='left')
    else:
        mdWorkspace.new_header(level=2, title='Users')
        mdWorkspace.new_paragraph('No users found')

    datasets = workspace['datasets']

    mdWorkspace.new_header(level=2, title=workspace['name'])
    mdWorkspace.new_header(level=3, title='Datasets')

    list_of_datasets = []
    list_of_datasets.extend(['Dataset Name', 'Last Modified'])

    for dataset in datasets:
        try:
            list_of_datasets.extend([f"[{dataset['name']}](../Datasets/{get_clean_file_name(dataset['name'])})", datetime.strptime(dataset['createdDate'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
        except:
            list_of_datasets.extend([f"[{dataset['name']}](../Datasets/{get_clean_file_name(dataset['name'])})", dataset['createdDate']])
        create_mdDataset(workspace['name'], dataset, work_dir, wiki_path, get_clean_name(dataset['name']), list_of_total_reports, list_of_total_mcode,openai_config) 

    mdWorkspace.new_table(columns=2, rows=len(list_of_datasets)//2, text=list_of_datasets, text_align='left')
    mdWorkspace.new_header(level=3, title='Reports')
    reports = sorted(workspace['reports'], key=lambda x: x.get('modifiedDateTime', 'not set'), reverse=True)

    list_of_reports = []
    list_of_reports.extend(['Report Name', 'Last Modified'])

    for report in reports:
        dataset = next((dataset for dataset in datasets if dataset['id'] == report.get('datasetId', '')), None)
        try:
            list_of_reports.extend([f"[{report['name']}](../Reports/{get_clean_file_name(report['name'])})", datetime.strptime(report['modifiedDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
        except:
            list_of_reports.extend([f"[{report['name']}](../Reports/{get_clean_file_name(report['name'])})", report.get('modifiedDateTime', 'not set')])
        create_mdReport(workspace['name'], report, wiki_path, get_clean_name(report['name']), dataset['name'] if dataset and 'name' in dataset else 'not set')

    columns = 2
    mdWorkspace.new_table(columns=columns, rows=len(list_of_reports)//columns, text=list_of_reports, text_align='left')
    mdWorkspace.create_md_file()
    print(f"File {os.path.join(workspace_path, wiki_name)} created")

def create_mdDataset(workspace_name, dataset, work_dir, wiki_path, wiki_name, list_of_total_reports, list_of_total_mcode, openai_config):
    datasets_path = os.path.join(wiki_path, "Datasets")
    if not os.path.exists(datasets_path):
        os.makedirs(datasets_path)

    mdDataset = mdutils.MdUtils(file_name=os.path.join(datasets_path, wiki_name))
    mdDataset.new_header(level=1, title=dataset['name'])
    list_of_rows = []
    list_of_rows.extend(['Dataset ID', dataset['id']])
    list_of_rows.extend(['Workspace', f"[{workspace_name}](../Workspaces/{get_clean_file_name(workspace_name)})"]) 
    list_of_rows.extend(['Configured By', dataset.get('configuredBy', 'not set')])
    list_of_rows.extend(['Target Storage Mode', dataset.get('targetStorageMode', 'not set')])
    list_of_rows.extend(['Content Provider Type', dataset.get('contentProviderType', 'not set')])
    if 'refreshSchedule' in dataset:
        list_of_rows.extend(['Refresh Schedule', ', '.join(dataset['refreshSchedule']['days']) + ' / ' + ', '.join(dataset['refreshSchedule']['times'])])

    if 'directQueryRefreshSchedule' in dataset and 'frequency' in dataset['directQueryRefreshSchedule']:
        list_of_rows.extend(['Direct Query Refresh Schedule', dataset['directQueryRefreshSchedule']['frequency']])
    
    if 'refreshSchedule' and 'directQueryRefreshSchedule' not in dataset:
        list_of_rows.extend(['Refresh Schedule', 'not set'])
    
    try:
        list_of_rows.extend(['Created Date', datetime.strptime(dataset['createdDate'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
    except:
        list_of_rows.extend(['Created Date', dataset['createdDate']]) 

    try:
        if 'roles' in dataset and len(dataset['roles']) > 0:
            list_of_rows.extend(['Row Level Security', 'Yes'])
        else:
            list_of_rows.extend(['Row Level Security', 'No'])
    except:
        list_of_rows.extend(['Row Level Security', 'unknown'])

    
    list_of_rows.extend(['MCode', f"[M Code](./{wiki_name}/mcode.md)"])
    list_of_rows.extend(['DAX', f"[DAX](./{wiki_name}/dax.md)"])
    
    columns = 2
    mdDataset.new_table(columns=columns, rows=len(list_of_rows)//columns, text=list_of_rows, text_align='left')

    if 'users' in dataset and len(dataset['users']) > 0:
        mdDataset.new_header(level=2, title='Users')
        list_of_users = []
        list_of_users.extend(['User', 'User Type', 'Email', 'Dataset Access'])
        for user in dataset['users']:
            if user['displayName']:
                list_of_users.extend([f"[{user['displayName']}](../Users/{get_clean_file_name(user['displayName'])})", user['userType'], user['emailAddress'], user['datasetUserAccessRight']])
        columns = 4
        mdDataset.new_table(columns=columns, rows=len(list_of_users)//columns, text=list_of_users, text_align='left')
    else:
        mdDataset.new_header(level=2, title='Users')
        mdDataset.new_paragraph('No users found')

    if 'roles' in dataset and len(dataset['roles']) > 0:
        roles = dataset['roles']
        mdDataset.new_header(level=2, title='Roles')
        for role in roles:
            mdDataset.new_header(level=3, title=role['name'])
            mdDataset.new_paragraph('Model Permission: ' + role['modelPermission'])
            if 'tablePermissions' in role and len(role['tablePermissions']) > 0:
                for table_row in role['tablePermissions']:
                    mdDataset.new_paragraph(table_row['name'])
                    if table_row.get('filterExpression') is not None:
                        mdDataset.insert_code(table_row['filterExpression'], 'm')
            if 'members' in role and len(role['members']) > 0:
                list_of_members = []
                list_of_members.extend(['Member Type', 'Member Name'])
                for member in role['members']:
                    list_of_members.extend([member['memberType'], member['memberName']])
                columns = 2
                mdDataset.new_table(columns=columns, rows=len(list_of_members)//columns, text=list_of_members, text_align='left')


    create_mdTables(workspace_name, dataset, os.path.join(datasets_path, wiki_name),list_of_total_reports, list_of_total_mcode, openai_config)
    create_mdMCode(workspace_name, dataset, os.path.join(datasets_path, wiki_name),list_of_total_mcode, openai_config)
    create_mdDAX(workspace_name, dataset, os.path.join(datasets_path, wiki_name), openai_config)

    mdDataset.new_header(level=2, title='Reports')
    list_of_reports = []
    list_of_reports.extend(['Report', 'Workspace'])
    for report in list_of_total_reports:
        if report['datasetId'] == dataset['id']:
            list_of_reports.extend([f"[{report['name']}](../Reports/{get_clean_file_name(report['name'])})", f"[{workspace_name}](../Workspaces/{get_clean_file_name(workspace_name)})"])
    columns = 2
    mdDataset.new_table(columns=columns, rows=len(list_of_reports)//columns, text=list_of_reports, text_align='left')

    mdDataset.new_header(level=2, title='Tables')
    list_of_tables = []
    list_of_tables.extend(['Table', 'Workspace'])
    for table in dataset['tables']:
        list_of_tables.extend([f"[{table['name']}](./{get_clean_name(dataset['name'])}/{get_clean_file_name(table['name'])})", f"[{workspace_name}](../Workspaces/{get_clean_file_name(workspace_name)})"])
    columns = 2
    mdDataset.new_table(columns=columns, rows=len(list_of_tables)//columns, text=list_of_tables, text_align='left')

    for report in list_of_total_reports:
        for table in dataset['tables']:
            append_csv(work_dir, {'Table Name': table.get('name'), 'Report Name': report['name'], 'Report ID': report['id']})

    mdDataset.create_md_file()
    print(f"File {os.path.join(datasets_path, wiki_name)} created")

def create_mdReport(workspace_name, report, wiki_path, wiki_name, dataset_name):
    report_path = os.path.join(wiki_path, "Reports")
    if not os.path.exists(report_path):
        os.makedirs(report_path)

    mdReport = mdutils.MdUtils(file_name=os.path.join(report_path, wiki_name))
    mdReport.new_header(level=1, title=report['name'])
    list_of_rows = []
    list_of_rows.extend(['Report ID', report['id']])
    list_of_rows.extend(['Workspace', f"[{workspace_name}](../Workspaces/{get_clean_file_name(workspace_name)})"])  
    list_of_rows.extend(['Dataset', f"[{dataset_name}](../Datasets/{get_clean_file_name(dataset_name)})"])
    list_of_rows.extend(['Created By', report.get('createdBy', 'not set')])
    try:
        list_of_rows.extend(['Created Date', datetime.strptime(report['createdDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
    except:
        list_of_rows.extend(['Created Date', report.get('createdDateTime', 'not set')])
    list_of_rows.extend(['Modified By', report.get('modifiedBy', 'not set')])
    try:
        list_of_rows.extend(['Modified Date', datetime.strptime(report['modifiedDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
    except:
        list_of_rows.extend(['Modified Date', report.get('modifiedDateTime', 'not set')])

    columns = 2
    mdReport.new_table(columns=columns, rows=len(list_of_rows)//columns, text=list_of_rows, text_align='left')
    
    if 'users' in report and len(report['users']) > 0:
        mdReport.new_header(level=2, title='Users')
        list_of_users = []
        list_of_users.extend(['User', 'User Type', 'Email', 'Report Access'])
        for user in report['users']:
            if user['displayName']:
                list_of_users.extend([f"[{user['displayName']}](../Users/{get_clean_file_name(user['displayName'])})", user['userType'], user['emailAddress'], user['reportUserAccessRight']])
        columns = 4
        mdReport.new_table(columns=columns, rows=len(list_of_users)//columns, text=list_of_users, text_align='left')
    else:
        mdReport.new_header(level=2, title='Users')
        mdReport.new_paragraph('No users found')
    mdReport.create_md_file()
    print(f"File {os.path.join(report_path, wiki_name)} created")

def create_mdWorkspaces(workspaces, work_dir, wiki_path, scan_date, list_of_total_reports, list_of_total_mcode, openai_config):
    list_of_workspaces = []
    list_of_workspaces.extend(['Workspace Name', 'ID'])
    
    mdWorkspaces = mdutils.MdUtils(file_name=os.path.join(wiki_path, 'Workspaces'))
    mdWorkspaces.new_header(level=1, title='Workspace List')
    mdWorkspaces.new_paragraph("Last Scan: " + scan_date)
    mdWorkspaces.new_paragraph("Last Wiki updated: " + datetime.now().strftime('%B %d, %Y %H:%M:%S'))
    mdWorkspaces.new_line()

    for workspace in workspaces:
        workspace_wiki_name = get_clean_name(workspace['name'])
        workspace_wiki_url = f"[{workspace['name']}](./Workspaces/{get_clean_file_name(workspace['name'])})"
        create_mdWorkspace(workspace, work_dir, wiki_path, workspace_wiki_name, list_of_total_reports, list_of_total_mcode, openai_config)
        list_of_workspaces.extend([workspace_wiki_url, workspace['id']])
        mdWorkspaces.new_line()

    mdWorkspaces.new_table(columns=2, rows=len(list_of_workspaces)//2, text=list_of_workspaces, text_align='left')
    mdWorkspaces.create_md_file()
    print(f"File {os.path.join(wiki_path, 'Workspaces')} created")

def create_mdUsers(workspaces, wiki_path):
    users_path = os.path.join(wiki_path, "Users")
    if not os.path.exists(users_path):
        os.makedirs(users_path)

    users = []
    for workspace in workspaces:
        if workspace.get('users') is not None and workspace['users']:
            for user in workspace['users']:
                if next((item for item in users if item["identifier"] == user['identifier']), None) is not None:
                    for i, u in enumerate(users):
                        if u['identifier'] == user['identifier']:
                            users[i]['workspaces'].append({'workspaceName': workspace['name'], 'workspaceId': workspace['id'], 'groupUserAccessRight': user['groupUserAccessRight']})
                else: 
                    users.append({
                        'identifier': user['identifier'], 
                        'displayName': user['displayName'],
                        'userType': user['userType'], 
                        'emailAddress': user['emailAddress'], 
                        'workspaces': 
                            [{'workspaceName': workspace['name'], 
                            'workspaceId': workspace['id'], 
                            'groupUserAccessRight': user['groupUserAccessRight']
                            }], 
                        'reports': [], 
                        'datasets': []
                    })
        for report in workspace['reports']:
            if report.get('users') is not None and report['users']:
                for user in report['users']:
                    for i, u in enumerate(users):
                        if u['identifier'] == user['identifier']:
                            if users[i].get('reports') is None:
                                users[i]['reports'] = []
                            users[i]['reports'].append({'reportName': report['name'], 'reportId': report['id'], 'reportUserAccessRight': user['reportUserAccessRight']})
                            break
        for dataset in workspace['datasets']:
            if dataset.get('users') is not None and dataset['users']:
                for user in dataset['users']:
                    for i, u in enumerate(users):
                        if u['identifier'] == user['identifier']:
                            users[i]['datasets'].append({'datasetName': dataset['name'], 'datasetId': dataset['id'], 'datasetUserAccessRight': user['datasetUserAccessRight']})
                            break
    mdUsers = mdutils.MdUtils(file_name=os.path.join(wiki_path, 'Users'))
    mdUsers.new_header(level=1, title='User List')
    list_of_users = []
    list_of_users.extend(['User Name', 'Email', 'User Type', 'Workspaces', 'Reports', 'Datasets'])
    for user in users:
        if user['displayName']:
            list_of_users.extend([f"[{user['displayName']}](./Users/{get_clean_file_name(user['displayName'])})", user['emailAddress'], user['userType'], len(user['workspaces']), len(user['reports']), len(user['datasets'])])
            mdUser = mdutils.MdUtils(file_name=os.path.join(wiki_path, 'Users', get_clean_name(user['displayName'])))
            mdUser.new_header(level=1, title=user['displayName'])
            if user['emailAddress'] is not None:
                mdUser.new_paragraph('Email: ' + user['emailAddress'])
            if user['userType'] is not None:
                mdUser.new_paragraph('User Type: ' + user['userType'])
            if len(user['workspaces']) > 0:
                mdUser.new_header(level=2, title='Workspaces')
                list_of_workspaces = []
                list_of_workspaces.extend(['Workspace', 'Workspace ID', 'Workspace Access'])
                for workspace in user['workspaces']:
                    list_of_workspaces.extend([f"[{workspace['workspaceName']}](./../Workspaces/{get_clean_file_name(workspace['workspaceName'])})", workspace['workspaceId'], workspace['groupUserAccessRight']])
                columns = 3
                mdUser.new_table(columns=columns, rows=len(list_of_workspaces)//columns, text=list_of_workspaces, text_align='left')
            if len(user['reports']) > 0:
                mdUser.new_header(level=2, title='Reports')
                list_of_reports = []
                list_of_reports.extend(['Report', 'Report ID', 'Report Access'])
                for report in user['reports']:
                    list_of_reports.extend([f"[{report['reportName']}](./../Reports/{get_clean_file_name(report['reportName'])})", report['reportId'], report['reportUserAccessRight']])
                columns = 3
                mdUser.new_table(columns=columns, rows=len(list_of_reports)//columns, text=list_of_reports, text_align='left')
            if len(user['datasets']) > 0:
                mdUser.new_header(level=2, title='Datasets')
                list_of_datasets = []
                list_of_datasets.extend(['Dataset', 'Dataset ID', 'Dataset Access'])
                for dataset in user['datasets']:
                    list_of_datasets.extend([f"[{dataset['datasetName']}](./../Datasets/{get_clean_file_name(dataset['datasetName'])})", dataset['datasetId'], dataset['datasetUserAccessRight']])
                columns = 3
                mdUser.new_table(columns=columns, rows=len(list_of_datasets)//columns, text=list_of_datasets, text_align='left')
            mdUser.create_md_file()
            print(f"File {os.path.join(wiki_path, 'Users', get_clean_name(user['displayName']))} created")
    columns = 6
    mdUsers.new_table(columns=columns, rows=len(list_of_users)//columns, text=list_of_users, text_align='left')
    mdUsers.create_md_file()
    print(f"File {os.path.join(wiki_path, 'Users')} created")

def create_mdDatasets(list_of_total_datasets, wiki_path):
    mdDatasets = mdutils.MdUtils(file_name=os.path.join(wiki_path, 'Datasets')) 
    mdDatasets.new_header(level=1, title='Dataset List')
    list_of_datasets = []
    list_of_datasets.extend(['Dataset Name', 'Dataset ID', 'Workspace'])
    for dataset in list_of_total_datasets:
        list_of_datasets.extend([f"[{dataset['name']}](./Datasets/{get_clean_file_name(dataset['name'])})", dataset['id'], f"[{dataset['workspace']}](./Workspaces/{get_clean_file_name(dataset['workspace'])})"])
    columns = 3
    mdDatasets.new_table(columns=columns, rows=len(list_of_datasets)//columns, text=list_of_datasets, text_align='left')
    mdDatasets.create_md_file()
    print(f"File {os.path.join(wiki_path, 'Datasets')} created")

def create_mdReports(list_of_total_reports, wiki_path):
    mdReports = mdutils.MdUtils(file_name=os.path.join(wiki_path, 'Reports')) 
    mdReports.new_header(level=1, title='Report List')
    list_of_reports = []
    list_of_reports.extend(['Report Name', 'Report ID', 'Workspace', 'Dataset'])
    for report in list_of_total_reports:
        list_of_reports.extend([f"[{report['name']}](./Reports/{get_clean_file_name(report['name'])})", report['id'], report['workspace'], report['datasetId']])
    columns = 4
    mdReports.new_table(columns=columns, rows=len(list_of_reports)//columns, text=list_of_reports, text_align='left')
    mdReports.create_md_file()
    print(f"File {os.path.join(wiki_path, 'Reports')} created")
                
def create_wiki_workspaces(workspaces, list_of_total_reports, list_of_total_datasets, list_of_total_mcode, work_dir, scan_date, openai_config):
    wiki_path = os.path.join(work_dir, 'wiki')
    if not os.path.exists(wiki_path):
        os.makedirs(wiki_path)

    create_mdWorkspaces(workspaces, work_dir, wiki_path, scan_date, list_of_total_reports=list_of_total_reports, list_of_total_mcode=list_of_total_mcode, openai_config=openai_config)
    create_mdUsers(workspaces, wiki_path)
    create_mdDatasets(list_of_total_datasets, wiki_path)
    create_mdReports(list_of_total_reports, wiki_path)
    print('WIKI created')

def create_wiki_datasources(datasources, list_of_total_datasets, list_of_total_reports, work_dir):
    wiki_path = os.path.join(work_dir, 'wiki')
    if not os.path.exists(wiki_path):
        os.makedirs(wiki_path)

    mdDatasources = mdutils.MdUtils(file_name=os.path.join(wiki_path, 'Datasources')) 
    mdDatasources.new_header(level=1, title='Datasource List')
    list_of_datasources = []
    list_of_datasources.extend(['Datasource Type', 'Datasource ID', 'Gateway ID', 'Connection Details'])
    for datasource in datasources:
        list_of_datasources.extend([datasource['datasourceType'], datasource['datasourceId'], datasource['gatewayId'], ' - '.join(map(str, datasource['connectionDetails'].values()))])
        create_mdDatasource(datasource, list_of_total_datasets, list_of_total_reports, wiki_path, work_dir)
    columns = 4
    mdDatasources.new_table(columns=columns, rows=len(list_of_datasources)//columns, text=list_of_datasources, text_align='left')
    mdDatasources.create_md_file()
    print(f"File {os.path.join(wiki_path, 'Datasources')} created")

def create_mdDatasource(datasource, datasets, reports, wiki_path, work_dir):
    wiki_path = os.path.join(wiki_path, "Datasources")
    if not os.path.exists(wiki_path):
        os.makedirs(wiki_path)
    mdDatasource = mdutils.MdUtils(file_name=os.path.join(wiki_path, datasource.get('datasourceId'))) 
    mdDatasource.new_header(level=1, title=datasource.get('datasourceId'))
    mdDatasource.new_paragraph('Datasource Type: ' + datasource.get('datasourceType'))
    mdDatasource.new_paragraph('Gateway ID: ' + datasource.get('gatewayId'))
    mdDatasource.new_paragraph('Connection Details: ' + ' - '.join(map(str, datasource['connectionDetails'].values())))
    mdDatasource.new_header(level=2, title='Datasets')
    list_of_datasets = []
    list_of_datasets.extend(['Dataset'])
    used_datasets = []
    for dataset in datasets:
        if dataset.get('datasourceUsages') is not None and len(dataset['datasourceUsages']) > 0:
            for ds in dataset['datasourceUsages']:
                if ds['datasourceInstanceId'] == datasource['datasourceId']:
                    list_of_datasets.extend([f"[{dataset['name']}](../Datasets/{get_clean_file_name(dataset['name'])})"])
                    used_datasets.append(dataset)
    columns = 1
    mdDatasource.new_table(columns=columns, rows=len(list_of_datasets)//columns, text=list_of_datasets, text_align='left')
    
    list_of_reports = []
    list_of_reports.extend(['Report'])
    mdDatasource.new_header(level=2, title='Reports')
    for report in reports:
        if report.get('datasetId') is not None:
            for dataset in used_datasets:
                if report['datasetId'] == dataset['id']:
                    list_of_reports.extend([f"[{report['name']}](../Reports/{get_clean_file_name(report['name'])})"])
    columns = 1
    mdDatasource.new_table(columns=columns, rows=len(list_of_reports)//columns, text=list_of_reports, text_align='left')
    mdDatasource.create_md_file()
    print(f"File {os.path.join(wiki_path, 'Datasource')} created")

def create_csv(work_dir):
    export_path = os.path.join(work_dir, 'export')  
    with open(os.path.join(export_path, "tables.csv"), 'w') as csvfile:
        fieldnames = ['Table Name', 'Report Name', 'Report ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def append_csv(work_dir, object):
    export_path = os.path.join(work_dir, 'export')  
    with open(os.path.join(export_path, "tables.csv"), 'a') as csvfile:
        fieldnames = ['Table Name', 'Report Name', 'Report ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(object)

def create_orderfile():
    orderfile_path = os.path.join('wiki')
    if not os.path.exists(orderfile_path):
        os.makedirs(orderfile_path)
    with open(os.path.join(orderfile_path, '.order'), 'w') as file:
        file.write('Workspaces\n')
        file.write('Datasets\n')
        file.write('Reports\n')
        file.write('Users\n')
        file.write('Datasources\n')
    print('Orderfile created')

def main():
    work_dir = sys.argv[1]
    pat = sys.argv[2]
    openai_url = sys.argv[3]
    openai_modelname = sys.argv[4]
    openai_api_key = sys.argv[5]
    branch_name = sys.argv[6]
    debug = sys.argv[7]

    openai_config = {"url": openai_url, "modelname": openai_modelname, "api_key": openai_api_key}

    print('Work Directory: ' + work_dir)
    print('PAT: ' + pat)
    print('OpenAI URL: ' + openai_config['url'])
    print('OpenAI Model Name: ' + openai_config['modelname'])
    print('OpenAI API Key: ' + openai_config['api_key'])

    workspaces = []
    datasources = []
    for file in os.listdir('export'):
        if file.startswith('scanResult'):
            data = load_data(os.path.join('export', file))
            workspaces.extend(data['workspaces'])
            datasources.extend(data['datasourceInstances'])
            scan_date = data['lastScanDate']

    list_of_total_reports = []
    list_of_total_datasets = []
    list_of_total_mcode = []

    for workspace in workspaces:
        for report in workspace['reports']:
            list_of_total_reports.append({'workspace': workspace['name'], 'id': report['id'], 'name': report['name'], 'datasetId': report.get('datasetId', 'not set')})
        for dataset in workspace['datasets']:
            list_of_total_datasets.append({'workspace': workspace['name'], 'id': dataset['id'], 'name': dataset['name'], 'datasourceUsages': dataset.get('datasourceUsages', None)})
            for table in dataset['tables']:
                if table.get('source') is not None:
                    mcode = table['source'][0]['expression']
                    list_of_total_mcode.append({'workspace': workspace['name'], 'datasetId': dataset['id'], 'datasetName': dataset.get('name', 'not set'), 'mcode': mcode})
    create_csv(work_dir)
    create_wiki_workspaces(workspaces, list_of_total_reports, list_of_total_datasets, list_of_total_mcode, work_dir, scan_date, openai_config)
    create_wiki_datasources(datasources, list_of_total_datasets, list_of_total_reports, work_dir)
    create_orderfile()

    if debug != 'true' or pat != '':
        git_operations(pat, branch_name)
    else:
        print('Debug mode enabled or PAT empty. Git operations are not executed.')

if __name__ == '__main__':
    main()
