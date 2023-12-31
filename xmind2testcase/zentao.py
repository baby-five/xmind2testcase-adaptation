#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import csv
import logging
import openpyxl
from xmind2testcase.utils import get_xmind_testcase_list, get_absolute_path

"""
Convert XMind fie to Zentao testcase csv file 

Zentao official document about import CSV testcase file: https://www.zentao.net/book/zentaopmshelp/243.mhtml 
"""


def xmind_to_zentao_csv_file(xmind_file):
    """Convert XMind file to a zentao csv file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to zentao file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)

    fileheader = ["所属模块", "用例标题", "前置条件", "步骤", "预期", "关键词", "优先级", "用例类型", "适用阶段"]
    zentao_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        zentao_testcase_rows.append(row)

    zentao_file = xmind_file[:-6] + '.csv'
    if os.path.exists(zentao_file):
        os.remove(zentao_file)
        logging.info('The zentao csv file already exists, return it directly: %s', zentao_file)

    with open(zentao_file, 'w', encoding='utf8', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(zentao_testcase_rows)
        logging.info('Convert XMind file(%s) to a zentao csv file(%s) successfully!', xmind_file, zentao_file)
    return zentao_file


def xmind_to_excel_file(xmind_file):
    """写入excel文件.xlsx格式"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to excel file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)

    fileheader = ["所属模块", "用例标题", "前置条件", "步骤", "预期", "关键词", "优先级", "用例类型", "适用阶段"]
    zentao_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        zentao_testcase_rows.append(row)

    excel_file = xmind_file[:-6] + '.xlsx'
    if os.path.exists(excel_file):
        os.remove(excel_file)
        logging.info('The excel file already exists, return it directly: %s', excel_file)

    workbook = openpyxl.workbook.Workbook()
    ws = workbook.active
    # print(f"sheetname: {xmind_file.split(os.sep)[-1][:-6]}")
    ws.title = xmind_file.split(os.sep)[-1][:-6]
    line = 1
    for data in zentao_testcase_rows:
        for col in range(1, len(data)+1):
            ws.cell(row=line, column=col).value = data[col - 1]
        line += 1
    workbook.save(excel_file)
    workbook.close()

    logging.info('Convert XMind file(%s) to a excel file(%s) successfully!', xmind_file, excel_file)
    return excel_file


def gen_a_testcase_row(testcase_dict):
    case_module = gen_case_module(testcase_dict['suite'])
    case_title = testcase_dict['name']
    case_precontion = testcase_dict['preconditions']
    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])
    case_keyword = ''
    case_priority = gen_case_priority(testcase_dict['importance'])
    case_type = gen_case_type(testcase_dict['execution_type'])
    case_apply_phase = '功能测试阶段'
    row = [case_module, case_title, case_precontion, case_step, case_expected_result, case_keyword, case_priority, case_type, case_apply_phase]
    return row


def gen_case_module(module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'
    return module_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    case_expected_result = ''

    for step_dict in steps:
        case_step += str(step_dict['step_number']) + '. ' + step_dict['actions'].replace('\n', '').strip() + '\n'
        case_expected_result += str(step_dict['step_number']) + '. ' + \
            step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
            if step_dict.get('expectedresults', '') else ''

    return case_step, case_expected_result


def gen_case_priority(priority):
    mapping = {1: '1', 2: '2', 3: '3', 4: '4'}
    if priority in mapping.keys():
        return mapping[priority]
    else:
        return '2'


def gen_case_type(case_type):
    mapping = {1: '功能测试', 2: '性能测试', 3: '配置相关', 4: '安装部署', 5: '安全相关', 6: '接口测试', 7: '单元测试', 8:'其他'}
    if case_type in mapping.keys():
        return mapping[case_type]
    else:
        return '功能测试'


if __name__ == '__main__':
    xmind_file = '../docs/zentao_testcase_template.xmind'
    zentao_csv_file = xmind_to_zentao_csv_file(xmind_file)
    print('Conver the xmind file to a zentao csv file succssfully: %s', zentao_csv_file)