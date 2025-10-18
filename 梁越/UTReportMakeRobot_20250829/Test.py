__package__ ="Test"
from lark import Lark,Transformer
from grammar import grammar
from transformer import IPOTransformer
import re

class ProgramAnalyzer:
    def __init__(self): 
        self.inputs = set()  # 入力
        self.outputs = set()  # 出力
        self.called_programs = set()  # 调用的程序
        self.file_operations = {}  # 文件操作
        self.variables = set()  # 变量
        self.sections = set()  # 段落
        self.statements = []  # 语句列表
        
    def analyze_content(self, content):
        """分析COBOL内容，提取入力、出力和调用的程序"""
        lines = content.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            original_line = line
            line = line.strip()
            if not line or line.startswith('*'):
                continue
                
            try:
                # 记录语句
                self.statements.append({
                    'line_num': line_num,
                    'content': line,
                    'type': self._classify_statement(line)
                })
                
                # 检查段落定义
                self._extract_sections(line)
                
                # 检查文件操作
                self._extract_file_operations(line)
                
                # 检查程序调用
                self._extract_program_calls(line)
                
                # 检查数据操作
                self._extract_data_operations(line)
                
                # 提取变量名
                self._extract_variables(line)
                
            except Exception as e:
                print(f"Warning: Error processing line {line_num}: {line[:50]}... - {e}")
    
    def _classify_statement(self, line):
        """分类语句类型"""
        line_upper = line.upper()
        if 'オープン' in line or 'OPEN' in line_upper:
            return 'FILE_OPEN'
        elif 'クローズ' in line or 'CLOSE' in line_upper:
            return 'FILE_CLOSE'
        elif 'リード' in line or 'READ' in line_upper:
            return 'FILE_READ'
        elif 'ライト' in line or 'WRITE' in line_upper:
            return 'FILE_WRITE'
        elif 'CALL' in line_upper:
            return 'PROGRAM_CALL'
        elif 'PERFORM' in line_upper or '実行' in line:
            return 'PERFORM'
        elif '→' in line or 'MOVE' in line_upper:
            return 'DATA_MOVE'
        elif 'もし' in line or 'IF' in line_upper:
            return 'CONDITIONAL'
        elif 'SECTION' in line_upper:
            return 'SECTION_DEF'
        elif line.endswith('.'):
            return 'STATEMENT'
        else:
            return 'UNKNOWN'
    
    def _extract_sections(self, line):
        """提取段落定义"""
        section_match = re.search(r'([A-Z0-9\-]+)\s+SECTION', line, re.IGNORECASE)
        if section_match:
            section_name = section_match.group(1)
            self.sections.add(section_name)
    
    def _extract_file_operations(self, line):
        """提取文件操作"""
        # オープン文 (打开文件)
        open_patterns = [
            r'([A-Z0-9\-]+)\s*を\s*オープン',
            r'OPEN\s+INPUT\s+([A-Z0-9\-]+)',
            r'OPEN\s+OUTPUT\s+([A-Z0-9\-]+)',
            r'OPEN\s+([A-Z0-9\-]+)'
        ]
        
        for pattern in open_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                file_name = match.group(1)
                if 'INPUT' in line.upper():
                    self.inputs.add(file_name)
                    self.file_operations[file_name] = 'INPUT'
                elif 'OUTPUT' in line.upper():
                    self.outputs.add(file_name)
                    self.file_operations[file_name] = 'OUTPUT'
                else:
                    # 根据文件名推测类型
                    if file_name.endswith('R') or 'read' in line.upper():
                        self.inputs.add(file_name)
                        self.file_operations[file_name] = 'INPUT'
                    elif file_name.endswith('W') or 'write' in line.upper():
                        self.outputs.add(file_name)
                        self.file_operations[file_name] = 'OUTPUT'
                    else:
                        self.file_operations[file_name] = 'UNKNOWN'
        
        # リード文 (读取文件)
        read_patterns = [
            r'([A-Z0-9\-]+)\s*から\s*([A-Z0-9\-]+)\s*を\s*リード',
            r'READ\s+([A-Z0-9\-]+)',
            r'([A-Z0-9\-]+)\s*を\s*リード'
        ]
        
        for pattern in read_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                file_name = match.group(1)
                self.inputs.add(file_name)
                self.file_operations[file_name] = 'INPUT'
        
        # ライト文 (写入文件)
        write_patterns = [
            r'([A-Z0-9\-]+)\s*を\s*([A-Z0-9\-]+)\s*に\s*ライト',
            r'WRITE\s+([A-Z0-9\-]+)',
            r'([A-Z0-9\-]+)\s*を\s*ライト'
        ]
        
        for pattern in write_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                if len(match.groups()) > 1:
                    file_name = match.group(2)
                else:
                    file_name = match.group(1)
                self.outputs.add(file_name)
                self.file_operations[file_name] = 'OUTPUT'
    
    def _extract_program_calls(self, line):
        """提取程序调用"""
        # CALL文
        call_patterns = [
            r'CALL\s+["\']([A-Z0-9]+)["\']',
            r'CALL\s+([A-Z0-9]+)'
        ]
        
        for pattern in call_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                program_name = match.group(1)
                self.called_programs.add(program_name)
        
        # PERFORM文
        perform_patterns = [
            r'PERFORM\s+([A-Z0-9\-]+)',
            r'([A-Z0-9\-]+)\s*を\s*実行'
        ]
        
        for pattern in perform_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                section_name = match.group(1)
                # 区分内部段落和外部程序
                if not section_name.endswith('-SECTION') and len(section_name) >= 6:
                    self.called_programs.add(section_name)
    
    def _extract_data_operations(self, line):
        """提取数据操作"""
        # → 操作符 (赋值)
        arrow_match = re.search(r'([A-Z0-9\-]+)\s*→\s*([A-Z0-9\-]+)', line)
        if arrow_match:
            source = arrow_match.group(1)
            target = arrow_match.group(2)
            self.variables.add(target)
            if source not in ['SPACE', 'ZERO', 'HIGH-VALUE', 'LOW-VALUE']:
                self.variables.add(source)
        
        # MOVE文
        move_match = re.search(r'MOVE\s+([A-Z0-9\-]+)\s+TO\s+([A-Z0-9\-]+)', line, re.IGNORECASE)
        if move_match:
            source = move_match.group(1)
            target = move_match.group(2)
            self.variables.add(target)
            if source not in ['SPACE', 'ZERO', 'HIGH-VALUE', 'LOW-VALUE']:
                self.variables.add(source)
    
    def _extract_variables(self, line):
        """提取变量名"""
        # 匹配COBOL风格的变量名 (通常包含字母、数字、连字符)
        var_pattern = r'\b([A-Z][A-Z0-9\-]*[A-Z0-9])\b'
        matches = re.findall(var_pattern, line)
        
        # 过滤掉关键字
        keywords = {
            'PROCEDURE', 'DIVISION', 'SECTION', 'PERFORM', 'CALL', 'MOVE', 
            'READ', 'WRITE', 'OPEN', 'CLOSE', 'IF', 'ELSE', 'END-IF',
            'SPACE', 'ZERO', 'HIGH-VALUE', 'LOW-VALUE', 'LENGTH'
        }
        
        for match in matches:
            if match not in keywords and len(match) >= 3:
                self.variables.add(match)
    
    def get_statement_statistics(self):
        """获取语句统计"""
        stats = {}
        for stmt in self.statements:
            stmt_type = stmt['type']
            stats[stmt_type] = stats.get(stmt_type, 0) + 1
        return stats
    
    def print_results(self):
        """输出分析结果"""
        print("\n" + "=" * 80)
        print("プログラム解析結果 (Program Analysis Results)")
        print("=" * 80)
        
        # 基本统计
        stats = self.get_statement_statistics()
        print(f"\n【基本統計】:")
        print(f"  総行数: {len(self.statements)}")
        print(f"  セクション数: {len(self.sections)}")
        print(f"  変数数: {len(self.variables)}")
        
        print(f"\n【文タイプ別統計】:")
        for stmt_type, count in sorted(stats.items()):
            print(f"  {stmt_type}: {count}")
        
        # 文件操作
        print(f"\n【入力ファイル】:")
        if self.inputs:
            for inp in sorted(self.inputs):
                file_type = self.file_operations.get(inp, 'UNKNOWN')
                print(f"  - {inp} ({file_type})")
        else:
            print("  なし")
        
        print(f"\n【出力ファイル】:")
        if self.outputs:
            for out in sorted(self.outputs):
                file_type = self.file_operations.get(out, 'UNKNOWN')
                print(f"  - {out} ({file_type})")
        else:
            print("  なし")
        
        # 程序调用
        print(f"\n【呼び出しプログラム】:")
        if self.called_programs:
            for prog in sorted(self.called_programs):
                print(f"  - {prog}")
        else:
            print("  なし")
        
        # 段落
        print(f"\n【セクション】:")
        if self.sections:
            for section in sorted(self.sections):
                print(f"  - {section}")
        else:
            print("  なし")
        
        # 主要变量
        print(f"\n【主要変数】: (前30個)")
        if self.variables:
            sorted_vars = sorted(list(self.variables))[:30]
            for i, var in enumerate(sorted_vars):
                if i % 3 == 0:
                    print(f"\n  ", end="")
                print(f"{var:<20}", end="")
            print()
            if len(self.variables) > 30:
                print(f"\n  ... 他 {len(self.variables) - 30} 個")
        else:
            print("  なし")

def parse_with_error_recovery(parser, content, chunk_size=5):
    """带错误恢复的解析函数"""
    lines = content.split('\n')
    successful_parses = []
    failed_chunks = []
    
    print(f"\n=== 分段解析 (每{chunk_size}行) ===")
    
    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i+chunk_size]
        chunk_content = '\n'.join(chunk_lines).strip()
        
        if not chunk_content:
            continue
            
        print(f"\n--- 行 {i+1}-{i+len(chunk_lines)} ---")
        print(f"内容: {chunk_content[:100]}{'...' if len(chunk_content) > 100 else ''}")
        
        try:
            result = parser.parse(chunk_content)
            print(f"✓ 解析成功")
            successful_parses.append({
                'lines': (i+1, i+len(chunk_lines)),
                'content': chunk_content,
                'result': result
            })
        except Exception as e:
            print(f"✗ 解析失败: {str(e)[:100]}...")
            failed_chunks.append({
                'lines': (i+1, i+len(chunk_lines)),
                'content': chunk_content,
                'error': str(e)
            })
    
    print(f"\n=== 解析結果サマリー ===")
    print(f"成功: {len(successful_parses)} 個のチャンク")
    print(f"失敗: {len(failed_chunks)} 個のチャンク")
    
    if failed_chunks:
        print(f"\n【失敗したチャンク】:")
        for chunk in failed_chunks[:5]:  # 只显示前5个失败的
            print(f"  行 {chunk['lines'][0]}-{chunk['lines'][1]}: {chunk['error'][:50]}...")
    
    return successful_parses, failed_chunks

def main():
    """主函数"""
    file_path = r'C:\Users\9512601\Desktop\smartTOOL\IPOソース参照\MAQR8700.ipo'
    
    # 1. 读取文件
    print("=" * 80)
    print("ファイル読み込み")
    print("=" * 80)
    
    try:
        with open(file_path, "r", encoding="Shift_JIS") as f:
            content = f.read()
        print(f"✓ ファイル読み込み成功: {len(content)} 文字")
    except Exception as e:
        print(f"✗ ファイル読み込み失敗: {e}")
        return
    
    # 2. 提取PROCEDURE DIVISION
    match = re.search(r'PROCEDURE\s+DIVISION(.*)', content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        print("✗ PROCEDURE DIVISION が見つかりません")
        return
    
    procedure_content = match.group(1)
    non_comment_lines = [line for line in procedure_content.splitlines() 
                        if not line.strip().startswith('*')]
    procedure_content_filter = '\n'.join(non_comment_lines).strip()
    
    print(f"✓ PROCEDURE DIVISION 抽出成功")
    print(f"  総行数: {len(procedure_content.splitlines())}")
    print(f"  非コメント行数: {len(non_comment_lines)}")
    
    # 3. 程序分析
    print("\n" + "=" * 80)
    print("プログラム解析実行中...")
    print("=" * 80)
    
    analyzer = ProgramAnalyzer()
    analyzer.analyze_content(procedure_content_filter)
    analyzer.print_results()
    
    # 4. 语法解析测试
    print("\n" + "=" * 80)
    print("文法解析テスト")
    print("=" * 80)
    
    try:
        parser = Lark(grammar, parser="lalr", transformer=IPOTransformer())
        print("✓ Parser 初期化成功")
    except Exception as e:
        print(f"✗ Parser 初期化失敗: {e}")
        return
    
    # 简单测试用例
    test_cases = [
        ("IF文", "もし (A = B) ならば\n  C → D\n終わり."),
        ("代入文", "SPACE → WK001-AREA.\nZERO → WK002-COUNT."),
        ("関数呼び出し", "LENGTH OF WK005-DATA."),
        ("ファイル操作", "HAEW21R を オープン.\nHAEW24R を オープン.")
    ]
    
    print(f"\n--- 基本テストケース ---")
    for name, code in test_cases:
        print(f"\n{name}:")
        try:
            result = parser.parse(code.strip())
            print(f"  ✓ 成功: {str(result)[:50]}...")
        except Exception as e:
            print(f"  ✗ 失敗: {str(e)[:50]}...")
    
    # 5. 实际内容解析
    print(f"\n--- 実際のコード解析 ---")
    successful_parses, failed_chunks = parse_with_error_recovery(
        parser, procedure_content_filter, chunk_size=3
    )
    
    # 6. 显示前几个成功解析的结果
    if successful_parses:
        print(f"\n【成功解析例】:")
        for i, parse in enumerate(successful_parses[:3]):
            print(f"\n例 {i+1} (行 {parse['lines'][0]}-{parse['lines'][1]}):")
            print(f"  内容: {parse['content'][:80]}...")
            print(f"  結果: {str(parse['result'])[:80]}...")

    print(f"\n" + "=" * 80)
    print("解析完了")
    print("=" * 80)

# 原有的兼容代码保持不变
if __name__ == "__main__":
    main()
else:
    # 保持原有的执行流程以确保兼容性
    file_path = r'C:\Users\9512601\Desktop\smartTOOL\IPOソース参照\MAQR8700.ipo'
    
    with open(file_path, "r", encoding="Shift_JIS") as f:
        content = f.read()
    
    match = re.search(r'PROCEDURE\s+DIVISION(.*)', content, re.DOTALL | re.IGNORECASE)
    
    if match:
        procedure_content = match.group(1)
        non_comment_lines = [line for line in procedure_content.splitlines() if not line.strip().startswith('*')]
        procedure_content_filter = '\n'.join(non_comment_lines).strip()
        print("=== PROCEDURE CONTENT ===")
        print(procedure_content_filter[:2000])
        print("=== END PROCEDURE CONTENT ===")
    else:
        procedure_content_filter = ""
        print("未找到 PROCEDURE DIVISION 段落")
    
    # 解析器实例化
    parser=Lark(grammar,parser="lalr",transformer=IPOTransformer())
    
    # 测试用例
    test_simple = """
もし (A = B) ならば
  C → D
終わり.
"""
    print("=== TESTING SIMPLE CASE ===")
    try:
        simple_parse = parser.parse(test_simple.strip())
        print("Simple parse successful:", simple_parse)
    except Exception as e:
        print("Simple parse failed:", e)
    
    test_constant = """
SPACE → WK001-AREA.
ZERO → WK002-COUNT.
"""
    print("=== TESTING CONSTANT ASSIGNMENT ===")
    try:
        constant_parse = parser.parse(test_constant.strip())
        print("Constant parse successful:", constant_parse)
    except Exception as e:
        print("Constant parse failed:", e)
    
    test_function = """
LENGTH OF WK005-DATA.
"""
    print("=== TESTING FUNCTION CALL ===")
    try:
        function_parse = parser.parse(test_function.strip())
        print("Function parse successful:", function_parse)
    except Exception as e:
        print("Function parse failed:", e)