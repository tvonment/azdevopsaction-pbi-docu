import os
import json
import mdutils
import sys
import base64
import subprocess
from datetime import datetime

def load_data():
    with open('export/scanResult.json', 'r') as file:
        return json.load(file)

def prepare_markdown(workspace, scan_date, work_dir):
    reports = sorted(workspace['reports'], key=lambda x: x['modifiedDateTime'], reverse=True)
    datasets = workspace['datasets']
    datasets_dict = {obj["id"]: obj for obj in datasets}

    wiki_path = os.path.join(work_dir, 'wiki')
    if not os.path.exists(wiki_path):
        os.makedirs(wiki_path)

    mdIndex = mdutils.MdUtils(file_name=os.path.join(wiki_path, 'Workspaces-Scan'))
    mdIndex.new_header(level=1, title='Power BI Workspaces Scan')
    mdIndex.new_paragraph("Last Scan: " + scan_date)
    mdIndex.new_paragraph("Last Wiki updated: " + datetime.now().strftime('%B %d, %Y %H:%M:%S'))
    mdIndex.new_header(level=3, title='Reports')
    list_of_reports = []
    list_of_reports.extend(['Workspace', 'Report Name', 'Last Modified'])

    for report in reports:
        report_wiki_name = report['name'].replace(' ', '-')
        list_of_reports.extend([f"{workspace['name']}", f"[{report['name']}](./{report_wiki_name}.md)", datetime.strptime(report['modifiedDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
        report_path = os.path.join(wiki_path, report_wiki_name)
        if not os.path.exists(report_path):
            os.makedirs(report_path)

        mdOverview = mdutils.MdUtils(file_name=os.path.join(wiki_path, report_wiki_name))
        mdOverview.new_header(level=1, title=report['name'])
        dataset = datasets_dict[report['datasetId']]
        
        list_of_rows = []
        list_of_rows.extend(['Workspace', workspace['name']])
        list_of_rows.extend(['Report ID', report['id']])
        list_of_rows.extend(['Dataset Name', dataset['name']])
        list_of_rows.extend(['Dataset ID', dataset['id']])
        list_of_rows.extend(['Created By', report['createdBy']])
        list_of_rows.extend(['Created Date', datetime.strptime(report['createdDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])
        list_of_rows.extend(['Modified By', report['modifiedBy']])
        list_of_rows.extend(['Modified Date', datetime.strptime(report['modifiedDateTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y %H:%M:%S')])

        mdOverview.new_table(columns=2, rows=8, text=list_of_rows, text_align='left')    
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
                mdMCode.insert_code(parameter['expression'], 'm')

        mdMCode.create_md_file()
        mdDAX.create_md_file()

    columns = 2
    mdIndex.new_table(columns=columns, rows=len(list_of_reports)//columns, text=list_of_reports, text_align='left')  
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

    data = load_data()
    scan_date = data['lastScanDate']
    workspace = data['workspaces'][0]
    mdIndex = prepare_markdown(workspace, scan_date, work_dir)
    mdIndex.create_md_file()
    #git_operations(pat)

if __name__ == '__main__':
    main()
