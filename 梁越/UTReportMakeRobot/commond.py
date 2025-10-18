"""
程序头部信息提取器
用于从COBOL程序文件中提取PROGRAM-ID、PROGRAM-NAME、PATTERN-ID信息
"""

import os
import logging
from pathlib import Path
from typing import Tuple, Optional, NamedTuple
from lark import Lark, UnexpectedInput
import re

# 日志配置
LOG_FILE = os.path.join(os.path.dirname(__file__), "commond.log")
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

class ProgramInfo(NamedTuple):
    """程序信息数据结构"""
    program_id: str
    program_name: str
    pattern_id: str
    file_path: str
    pgm_id: str

class ProgramHeaderExtractor:
    """程序头部信息提取器"""

    def __init__(self):
        """初始化提取器"""
        self.encoding = "Shift_JIS"  # COBOL文件默认编码

        # Lark语法定义，直接匹配整行
        self.program_id_grammar = r"""
            start: /PROGRAM-ID\s*:\s*(.+)/
        """
        self.program_name_grammar = r"""
            start: /PROGRAM-NAME\s*:\s*(.+)/
        """
        self.pattern_id_grammar = r"""
            start: /PATTERN-ID\s*:\s*(.+)/
        """
        self.program_id_parser = Lark(self.program_id_grammar, parser='lalr', maybe_placeholders=False)
        self.program_name_parser = Lark(self.program_name_grammar, parser='lalr', maybe_placeholders=False)
        self.pattern_id_parser = Lark(self.pattern_id_grammar, parser='lalr', maybe_placeholders=False)

    def extract_program_info(self, file_path: str, pgm_id: str) -> ProgramInfo:
        """
        从指定文件提取程序信息
        """
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            raise FileNotFoundError(f"文件不存在: {file_path}")

        logger.info(f"🔍 开始解析文件: {Path(file_path).name}")
        logger.info(f"📋 程序ID: {pgm_id}")

        try:
            lines = self._read_first_lines(file_path, 15)
            program_id = self._extract_program_id(lines)
            program_name = self._extract_program_name(lines)
            pattern_id = self._extract_pattern_id(lines)

            result = ProgramInfo(
                program_id=program_id,
                program_name=program_name,
                pattern_id=pattern_id,
                file_path=file_path,
                pgm_id=pgm_id
            )

            logger.info(f"✅ 提取成功:")
            logger.info(f"   PROGRAM-ID: {program_id}")
            logger.info(f"   PROGRAM-NAME: {program_name}")
            logger.info(f"   PATTERN-ID: {pattern_id}")

            return result

        except Exception as e:
            logger.error(f"❌ 提取失败: {str(e)}")
            raise ValueError(f"无法提取程序信息: {str(e)}")

    def _read_first_lines(self, file_path: str, line_count: int = 15) -> list:
        lines = []
        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                for i in range(line_count):
                    line = f.readline()
                    if not line:
                        break
                    lines.append(line.rstrip('\n\r'))
            logger.info(f"📖 成功读取 {len(lines)} 行")
            return lines
        except UnicodeDecodeError:
            logger.warning(f"⚠️ Shift_JIS编码失败，尝试UTF-8")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for i in range(line_count):
                        line = f.readline()
                        if not line:
                            break
                        lines.append(line.rstrip('\n\r'))
                return lines
            except:
                logger.error(f"无法读取文件，编码格式不支持")
                raise ValueError(f"无法读取文件，编码格式不支持")

    def _extract_program_id(self, lines: list) -> str:
        for line in lines:
            m = re.search(r'PROGRAM-ID\s*:\s*(.+)', line)
            if m:
                program_id = m.group(1).strip()
                logger.info(f"🎯 找到PROGRAM-ID: {program_id}")
                return program_id
        logger.warning(f"⚠️ 未找到PROGRAM-ID")
        return ""

    def _extract_program_name(self, lines: list) -> str:
        for line in lines:
            m = re.search(r'PROGRAM-NAME\s*:\s*(.+)', line)
            if m:
                program_name = m.group(1).strip()
                logger.info(f"🎯 找到PROGRAM-NAME: {program_name}")
                return program_name
        logger.warning(f"⚠️ 未找到PROGRAM-NAME")
        return ""

    def _extract_pattern_id(self, lines: list) -> str:
        for line in lines:
            m = re.search(r'PATTERN-ID\s*:\s*(.+)', line)
            if m:
                pattern_id = m.group(1).strip()
                logger.info(f"🎯 找到PATTERN-ID: {pattern_id}")
                return pattern_id
        logger.warning(f"⚠️ 未找到PATTERN-ID")
        return ""

    def extract_multiple_programs(self, file_list: list) -> list:
        results = []
        logger.info(f"🚀 开始批量提取 {len(file_list)} 个程序信息")
        logger.info("=" * 60)
        for i, (file_path, pgm_id) in enumerate(file_list, 1):
            logger.info(f"\n[{i}/{len(file_list)}] 处理进度")
            try:
                result = self.extract_program_info(file_path, pgm_id)
                results.append(result)
                logger.info(f"✅ 第{i}个程序处理成功")
            except Exception as e:
                logger.error(f"❌ 第{i}个程序处理失败: {e}")
                failed_result = ProgramInfo(
                    program_id="",
                    program_name="",
                    pattern_id="",
                    file_path=file_path,
                    pgm_id=pgm_id
                )
                results.append(failed_result)
        logger.info(f"\n📊 批量提取完成:")
        success_count = sum(1 for r in results if r.program_id)
        logger.info(f"   成功: {success_count}/{len(file_list)}")
        logger.info(f"   失败: {len(file_list) - success_count}/{len(file_list)}")
        return results

    def print_program_info(self, info: ProgramInfo):
        logger.info(f"\n📄 程序信息详情")
        logger.info("=" * 50)
        logger.info(f"文件路径:     {info.file_path}")
        logger.info(f"输入PGM-ID:   {info.pgm_id}")
        logger.info(f"PROGRAM-ID:   {info.program_id}")
        logger.info(f"PROGRAM-NAME: {info.program_name}")
        logger.info(f"PATTERN-ID:   {info.pattern_id}")
        logger.info("=" * 50)

    def export_to_dict(self, info: ProgramInfo) -> dict:
        return {
            'program_id': info.program_id,
            'program_name': info.program_name,
            'pattern_id': info.pattern_id,
            'file_path': info.file_path,
            'pgm_id': info.pgm_id
        }

# 便捷函数
def extract_program_header(file_path: str, pgm_id: str) -> ProgramInfo:
    extractor = ProgramHeaderExtractor()
    return extractor.extract_program_info(file_path, pgm_id)

def batch_extract_headers(file_list: list) -> list:
    extractor = ProgramHeaderExtractor()
    return extractor.extract_multiple_programs(file_list)