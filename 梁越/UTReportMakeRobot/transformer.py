import logging
import re

logger = logging.getLogger(__name__)

class SectionTransformer:
    def __init__(self):
        self.source = {}  # 存储解析后的数据，假设是一个字典
        self.sections = []  # 存储所有的 section 信息
        self.summary_table = {}  # 一览表字典
        self.detail_table = {}  # 详细表字典

    def parse_source(self, content):
        """
        解析源文件内容，将内容分割为多个 section 并存储。
        """
        try:
            sections = content.split("*+LABEL-NAME")  # 假设以此标记分割
            for section in sections:
                if "セクションの終わり" in section:
                    section_id = self.extract_section_id(section)
                    self.source[section_id] = section.strip()
                    self.sections.append({"id": section_id, "content": section.strip()})
                else:
                    logger.warning("无效的 section，缺少结束标记: セクションの終わり.")
            self.process_sections()
        except Exception as e:
            logger.error(f"解析源文件时发生错误: {e}")

    def extract_section_id(self, section):
        """
        提取 section 的 ID，假设 ID 在 section 的第一行。
        """
        lines = section.splitlines()
        if lines:
            return lines[0].strip()  # 假设第一行是 ID
        return "Unknown"

    def process_sections(self):
        """
        遍历 source，解析 value 内容，提取子程序 ID，生成一览表和详细表。
        """
        for section_id, content in self.source.items():
            # 跳过以 "S" 或 "E" 开头的 section_id
            if section_id.startswith("S") or section_id.startswith("E"):
                continue

            # 提取子程序 ID
            subprogram_id = self.extract_subprogram_id(content)
            # if "QAJ03" in subprogram_id:
            #    continue
            # else:
            if subprogram_id:
                   # 一览表：key 为 section_id，value 为子程序 ID 加固定字符串
                   self.summary_table[section_id] = f"V{subprogram_id}_を行い、処理結果コードが異常の場合、が異常終了し、エラーメッセージが正しく編集されていることを確認する。"

                   # 详细表：key 为 section_id，value 为条件数组和处理数组
                   conditions = self.extract_conditions(content, f"V_{subprogram_id}")
                   processes = self.extract_processes(content)
                   self.detail_table[section_id] = {"conditions": conditions, "processes": processes}

    def extract_subprogram_id(self, content):
        """
        提取子程序 ID：当前 section 中存在带有 #N 开头的语句，则为解析对象，# 后面为子程序 ID。
        """
        match = re.search(r"#N(\w+)", content)
        if match:
            return match.group(1)
        return None

    def extract_conditions(self, content, subprogram_id):
        """
        提取条件数组：分析当前 section 的逻辑判断语句，提取【被判断项目，可能等于的值】。
        """
        conditions = []

        # 提取逻辑判断语句，假设格式为 "IF 被判断项目 = 值 THEN"
        matches = re.findall(r"IF\s+(\w+)\s*=\s*(\w+)\s*THEN", content)
        for condition in matches:
            conditions.append([condition[0], condition[1]])

        # 添加固定条件
        conditions.append([subprogram_id, "出力结果=正常"])
        conditions.append([subprogram_id, "处理结果=异常"])

        return conditions

    def extract_processes(self, content):
        """
        提取处理数组：插入“处理继续”，提取异常 code 和 msgcode 拼成字符串。
        """
        processes = ["处理继续"]

        # 提取异常 code，假设格式为 "xxx-yyy-code"
        exception_matches = re.findall(r"(\w+)-\w+-code", content)
        for exception in exception_matches:
            processes.append(f"{exception}-异常code")

        # 提取 msgcode，假设格式为 "xxx-yyy-msgcode"
        msgcode_matches = re.findall(r"(\w+)-\w+-msgcode", content)
        for msgcode in msgcode_matches:
            processes.append(f"{msgcode}-msgcode")

        return processes

    def get_summary_table(self):
        """
        返回一览表字典。
        """
        return self.summary_table

    def get_detail_table(self):
        """
        返回详细表字典。
        """
        return self.detail_table