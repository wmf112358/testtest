"""
SECTION ID 解析器
根据给定的路径和PGMID解析出section id
规则：在程序中，xxxxxxxx SECTION.xxxxxxxx为section id
"""

import os
from typing import List, Tuple
from pathlib import Path
import logging
from lark import Lark, UnexpectedInput
from PyQt5.QtCore import QThread, pyqtSignal

# 日志配置
LOG_FILE = os.path.join(os.path.dirname(__file__), "section_extractor.log")
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

class SectionExtractThread(QThread):
    finished = pyqtSignal(list, object)  # section_ids, error

    def __init__(self, file_path, pgm_id):
        super().__init__()
        self.file_path = file_path
        self.pgm_id = pgm_id

    def run(self):
        try:
            section_ids = extract_section_ids_from_file(self.file_path, self.pgm_id)
            self.finished.emit(section_ids, None)
        except Exception as e:
            self.finished.emit([], e)

class SectionIdExtractor:
    """SECTION ID提取器"""

    def __init__(self):
        self.encoding = "Shift_JIS"
        # Lark语法定义：支持全角、半角、日文、中文、下划线、连字符
        self.section_grammar = r"""
            start: section_id WS "SECTION" "." 
            section_id: /[^\s]+/
            WS: /\s+/
        """
        self.section_parser = Lark(self.section_grammar, parser='lalr', maybe_placeholders=False)

    def extract_section_ids(self, file_path: str, pgm_id: str) -> List[str]:
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            raise FileNotFoundError(f"文件不存在: {file_path}")

        logger.info(f"开始解析SECTION ID - 文件: {Path(file_path).name} 程序ID: {pgm_id}")
        try:
            lines = self._read_file_content(file_path)
            section_ids = self._extract_section_ids_from_lines(lines)
            logger.info(f"成功提取 {len(section_ids)} 个SECTION ID")
            return section_ids
        except Exception as e:
            logger.error(f"提取失败: {str(e)}")
            raise ValueError(f"无法提取SECTION ID: {str(e)}")

    def _read_file_content(self, file_path: str) -> List[str]:
        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                lines = [line.rstrip('\n\r') for line in f.readlines()]
            logger.info(f"成功读取 {len(lines)} 行")
            return lines
        except UnicodeDecodeError:
            logger.warning(f"Shift_JIS编码失败，尝试UTF-8: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = [line.rstrip('\n\r') for line in f.readlines()]
                logger.info(f"UTF-8读取成功，共 {len(lines)} 行")
                return lines
            except Exception as e:
                logger.error(f"无法读取文件，编码格式不支持: {file_path}")
                raise ValueError(f"无法读取文件，编码格式不支持")

    def _extract_section_ids_from_lines(self, lines: List[str]) -> List[str]:
        section_ids = []
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('*'):
                continue
            try:
                tree = self.section_parser.parse(line.strip())
                section_id = tree.children[0].children[0].strip()
                section_ids.append(section_id)
                logger.info(f"找到SECTION ID: {section_id} (行 {line_num})")
            except UnexpectedInput:
                continue
        # 去重并保持顺序
        unique_section_ids = []
        seen = set()
        for section_id in section_ids:
            if section_id not in seen:
                unique_section_ids.append(section_id)
                seen.add(section_id)
            else:
                logger.warning(f"重复的SECTION ID: {section_id}")
        # 过滤掉指定的SECTION
        exclude_sections = {
            "CONFIGURATION", "INPUT-OUTPUT", "FILE", "WORKING-STORAGE", "LINKAGE"
        }
        filtered_section_ids = [
            sid for sid in unique_section_ids
            if sid.upper() not in exclude_sections
        ]
        return filtered_section_ids

    def _extract_section_details_from_lines(self, lines: List[str]) -> List[dict]:
        section_details = []
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('*'):
                continue
            try:
                tree = self.section_parser.parse(line.strip())
                section_id = tree.children[0].children[0].strip()
                section_info = {
                    'section_id': section_id,
                    'line_number': line_num,
                    'line_content': line.strip(),
                    'original_line': line
                }
                section_details.append(section_info)
                logger.info(f"找到SECTION: {section_id} (行 {line_num})")
            except UnexpectedInput:
                continue
        # 过滤掉指定的SECTION
        exclude_sections = {
            "CONFIGURATION", "INPUT-OUTPUT", "FILE", "WORKING-STORAGE", "LINKAGE"
        }
        filtered_section_details = [
            info for info in section_details
            if info['section_id'].upper() not in exclude_sections
        ]
        return filtered_section_details

def extract_section_ids_from_file(file_path: str, pgm_id: str) -> List[str]:
    extractor = SectionIdExtractor()
    return extractor.extract_section_ids(file_path, pgm_id)

def extract_section_details_from_file(file_path: str, pgm_id: str) -> List[dict]:
    extractor = SectionIdExtractor()
    return extractor.extract_section_details(file_path, pgm_id)

def batch_extract_section_ids(file_list: List[Tuple[str, str]]) -> dict:
    extractor = SectionIdExtractor()
    results = {}
    logger.info(f"开始批量提取 {len(file_list)} 个文件的SECTION ID")
    for i, (file_path, pgm_id) in enumerate(file_list, 1):
        logger.info(f"[{i}/{len(file_list)}] 处理文件: {Path(file_path).name}")
        try:
            section_ids = extractor.extract_section_ids(file_path, pgm_id)
            results[pgm_id] = section_ids
            logger.info(f"{pgm_id}: 找到 {len(section_ids)} 个SECTION")
        except Exception as e:
            logger.error(f"{pgm_id}: 提取失败 - {e}")
            results[pgm_id] = []
    total_sections = sum(len(sections) for sections in results.values())
    successful_files = sum(1 for sections in results.values() if sections)
    logger.info(f"批量提取完成: 处理文件: {len(file_list)}, 成功文件: {successful_files}, 总SECTION数: {total_sections}")
    return results

