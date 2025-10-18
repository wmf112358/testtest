import re
from commond import extract_program_header
from lark import Lark, UnexpectedInput

# Lark 语法定义
dd_grammar = r"""
    start: (open_stmt)*
    open_stmt: "オープン" _WS ("入力"|"出力") _WS DDNAME _WS* "."
    DDNAME: /[A-Z0-9]+[RW]/
    _WS: /[ \u3000\t\n]+/
    %ignore /[ \u3000\t\n]+/
"""

dd_parser = Lark(dd_grammar, parser="lalr", maybe_placeholders=False)

def extract_dd_names_with_lark(content):
    input_dd = []
    output_dd = []
    # 只保留オープン语句的行
    open_lines = []
    for line in content.splitlines():
        line = line.strip()
        if "オープン" in line and ("入力" in line or "出力" in line):
            open_lines.append(line)
    
    if not open_lines:
        return input_dd, output_dd
        
    # 将所有オープン语句拼接成一个字符串
    open_content = "\n".join(open_lines)
    
    try:
        tree = dd_parser.parse(open_content)
        # 调试用
        print("解析的内容:", open_content)
        print("解析树:", tree.pretty())
        
        for stmt in tree.children:
            # 从解析树结构可以看出，DDNAME 是唯一的 Token
            ddname = str(stmt.children[0])
            # 根据原始行判断是入力还是出力
            for line in open_lines:
                if ddname in line:
                    if "入力" in line:
                        input_dd.append(ddname)
                    elif "出力" in line:
                        output_dd.append(ddname)
                    break
                    
    except UnexpectedInput as e:
        print(f"Lark解析失败：{str(e)}")
        print(f"待解析内容:\n{open_content}")
    
    return input_dd, output_dd

def analyze_program(file_path, pgm_id):
    """
    1. 调用commond获取程序id和模板类型
    2. 获取程序入出力dd名
    3. 判断模板类型等于66666时，返回指定结构的字典
    """
    # 1. 获取程序头部信息
    result = extract_program_header(file_path, pgm_id)
    program_id = result.program_id
    pattern_id = result.pattern_id

    # 2. 读取文件内容
    with open(file_path, "r", encoding="shift_jis") as f:
        content = f.read()

    # 3. 提取入力和出力DD名
    input_dd = []
    output_dd = []
    input_dd, output_dd = extract_dd_names_with_lark(content)

    # 4. 判断模板类型
    result_dict = {}
    if pattern_id == 'UZ0Q06':
        # value1: a = b; a > b; a < b
        conds = []
        conds.append("MASTER-KEY  =  TRANS-KEY,マスタ：トラン  =  1:1")
        conds.append("MASTER-KEY  <  TRANS-KEY,マスタ：トラン  =  1:0")
        conds.append("MASTER-KEY  >  TRANS-KEY,マスタ：トラン  =  0:1")
        # value2s: pgm_id+zzzzzzzzz；每个出力dd名+aaaaaaaaaaaaa
        value2s = [f"{pgm_id}が正常終了することを確認する。"]
        value2s.extend([f"{dd}に出力されていることを確認する。" for dd in output_dd])
        result_dict = {
            "正常系": {
                "value1": ";".join(conds),
                "value2": "；".join(value2s)
            }
        }
    
    # 5. 增加新的返回结果
    dd_result_key = f"テストケース番号・名称：xxx   下位モジュール【VQAP02】の実行結果がエラーの場合、{pgm_id}が正常終了して、メッセージ出力することを確認する。"
    dd_result_value1 = []
    # 添加入力DD名
    dd_result_value1.extend([f"{dd}" for dd in input_dd])
    # 添加出力DD名
    dd_result_value1.extend([f"{dd}" for dd in output_dd])
    # 添加共通部分
    dd_result_value1.extend(["共通＿ジョブログ出力機能(VQAP02)，正常終了", "共通＿ジョブログ出力機能(VQAP02)，異常終了"])

    result_dict[dd_result_key] = {
        "value1": "；".join(dd_result_value1),
        "value2": f"{pgm_id}が正常終了して、エラーメッセージ出力することを確認する。(コンソールメッセージＩＤ：F000013)"  # 新增value2
    }

    # 6. 增加模板类型ffff的返回结果
    if pattern_id == 'UZ0Q06':
        # 确保有至少两个入力DD和一个出力DD
        if len(input_dd) >= 2 and len(output_dd) >= 1:
            input1 = input_dd[0]
            input2 = input_dd[1]
            output = output_dd[0]
            
            lines = []
            # 第一行
            lines.append(f"{input1}，{input2}の入力件数が0件の場合、{pgm_id}が正常終了、{output}に出力されていないことを確認する。")
            # 第二到四行
            lines.append(f"{input1}の入力件数が0件以外、{input2}の入力件数が0件の場合、{pgm_id}fが正常終了、{output}に出力されていないことを確認する。")
            lines.append(f"{input1}の入力件数が0件、{input2}の入力件数が0件以外の場合、{pgm_id}fが正常終了、{output}に出力されていないことを確認する。")
            lines.append(f"{input1}，{input2}の入力件数が0件以外の場合、{pgm_id}が正常終了、{output}に出力結果が正しく反映されていることを確認する。")
            # 最后一行
            lines.append(f"下位モジュール【VQAP02】の実行結果がエラーの場合、{pgm_id}が正常終了して、メッセージ出力することを確認する。")
            
            result_dict["ＩＴａ１一覧表"] = {
                "value": "；\n".join(lines)
            }

    return result_dict