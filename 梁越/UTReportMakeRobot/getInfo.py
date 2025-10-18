__package__ = "getInfo"
import re

class CobolSelector:
    def __init__(self, cobol_code):
        # 去除注释行（以*开头）
        self.cobol_code = '\n'.join(
            line for line in cobol_code.splitlines() if not line.strip().startswith('*')
        )

    def find_select_assign(self):
        pattern = re.compile(r'SELECT\s+(\S+)\s+ASSIGN\s+TO\s+(\S+)\.', re.IGNORECASE)
        return pattern.findall(self.cobol_code)

class FileCopyFinder:
    def __init__(self, cobol_code):
        # 去除注释行（以*开头）
        self.cobol_code = '\n'.join(
            line for line in cobol_code.splitlines() if not line.strip().startswith('*')
        )

    def find_copy_for(self, file_name):
        fd_pattern = re.compile(
            rf'FD\s+{re.escape(file_name)}.*?01\s+{re.escape(file_name)}-REC\s+COPY\s+(\S+)', 
            re.IGNORECASE | re.DOTALL
        )
        match = fd_pattern.search(self.cobol_code)
        if match:
            return match.group(1)
        return None