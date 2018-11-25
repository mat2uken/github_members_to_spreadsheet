# coding: utf-8

from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import gspread

from datetime import datetime

import outside_colloaborators

scopes = ['https://www.googleapis.com/auth/spreadsheets']
json_file = 'client_secret.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scopes=scopes)
http_auth = credentials.authorize(Http())

import yaml
secrets = yaml.load(open('secret.yaml'))
doc_id = secrets['env']['ss_doc_id']
client = gspread.authorize(credentials)
gfile   = client.open_by_key(doc_id)

def get_or_create_worksheet(gfile):
    cur_sheet_name = datetime.now().strftime("%Y-%m")
    sheet = None
    for w in gfile.worksheets():
        if w.title == cur_sheet_name:
            sheet = w
    if sheet is None:
        sheet = gfile.add_worksheet(title=cur_sheet_name, rows="200", cols="20")

    return sheet

def add_collaborators_to_ss(sheet, collaborators):
    not_pana_collaborators = gfile.sheet1.col_values(1)
    # 1行目はタイトルなので飛ばす
    not_pana_collaborators = not_pana_collaborators[1:]

    sheet.update_acell('A1', 'パナソニックのコラボレータアカウント一覧')
    sheet.update_acell('B1', 'それ以外のコラボレータアカウント一覧')

    not_pana_count = 0
    pana_count = 0
    for user in collaborators:
        if user in not_pana_collaborators:
            sheet.update_acell('B{}'.format(not_pana_count+2), user)
            not_pana_count += 1
        else:
            sheet.update_acell('A{}'.format(pana_count+2), user)
            pana_count += 1

    sheet.update_acell('C2', '請求すべきアカウント数(basedataのシートが正しいことを確認してね)')
    sheet.update_acell('C3', '=COUNTA(A2:A999)')

#    cells = sheet.range('A2:A{}'.format(len(collaborators)+1))
#    for i, cell in enumerate(cells):
#        cell.value = collaborators[i]
#    sheet.update_cells(cells)

if __name__ == '__main__':
    sheet = get_or_create_worksheet(gfile)
    add_collaborators_to_ss(sheet, outside_colloaborators.get_collaborators())
