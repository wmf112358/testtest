from getInfo import CobolSelector
from getInfo import FileCopyFinder

file_path = r'C:\Users\9512601\Desktop\0920\IPOソース参照/MAQP2300.ipo'
with open(file_path, "r", encoding="Shift_JIS") as f:
    content = f.read()

# 1. 查找所有 SELECT/ASSIGN
selector = CobolSelector(content)
selects = selector.find_select_assign()
print("SELECT/ASSIGN结果：")
for s in selects:
    print(s)

# 2. 查找 copy 句
finder = FileCopyFinder(content)
print("\n各文件的copy句：")
for file_name, _ in selects:
    copy_name = finder.find_copy_for(file_name)
    print(f"{file_name} 的 copy 句为: {copy_name}")