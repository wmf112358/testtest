__package__ ="Test"
from lark import Lark,Transformer
from grammar import grammar
from transformer import IPOTransformer
import re


file_path = 'C:/Users/9511554/Desktop/LHL/01_jishudasai/IPOソース参照/MAET8600.ipo'
# 读取文件内容，假设文件编码为Shift_JIS
# 如果文件编码不同，请根据实际情况修改
with open(file_path, "r", encoding="Shift_JIS") as f:
    content = f.read()
# 使用正则表达式提取 PROCEDURE DIVISION 段落，PROCEDURE 和 DIVISION 中间任意数量的空格
match = re.search(r'PROCEDURE\s+DIVISION(.*)', content, re.DOTALL | re.IGNORECASE)

if match:
    procedure_content = match.group(1)
    # 按行分割并筛选出不以 '*' 开头的行    
    non_comment_lines = [line for line in procedure_content.splitlines() if not line.strip().startswith('*')]
    # 将非注释行重新组合成一个字符串
    procedure_content_filter = '\n'.join(non_comment_lines).strip()
    #print(procedure_content_filter)
else:
    procedure_content_filter = ""
    print("未找到 PROCEDURE DIVISION 段落")

# code 变量现在包含了文件的全部内容
# 解析器实例化
# 这里的 parser 参数可以根据需要调整
parser=Lark(grammar,parser="lalr",transformer=IPOTransformer())

#print(grammar)
#tokens = list(parser.lex(procedure_content_filter))
#for t in tokens:
    #print(t, [hex(ord(c)) for c in t.value])
    #print(t)

parseTree=parser.parse(procedure_content_filter)
print(parseTree) 