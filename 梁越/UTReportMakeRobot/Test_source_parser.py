import logging
from transformer import SectionTransformer  # 假设 transformer 模块中定义了 SectionTransformer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_file(file_path):
    try:
        # 读取文件内容
        with open(file_path, "r", encoding="Shift-JIS") as file:
            content = file.read()

        # 调用 parse_source 方法解析内容
        logger.info("开始解析文件内容...")
        transformer = SectionTransformer()  # 创建 SectionTransformer 实例
        transformer.parse_source(content)
        logger.info("解析完成！")

        # 获取一览表和详细表
        summary_table = transformer.get_summary_table()  # 获取一览表
        detail_table = transformer.get_detail_table()    # 获取详细表

        # 打印一览表内容以调试
        logger.info(f"一览表内容: {summary_table}")

        # 遍历并打印一览表
        logger.info("一览表:")
        if isinstance(summary_table, dict):  # 如果是一览表是字典
            for section_id, summary in summary_table.items():
                print(f"Section ID: {section_id}, Summary: {summary}")
        else:
            logger.warning("一览表不是字典，无法解析")

        # 遍历并打印详细表
        logger.info("详细表:")
        if isinstance(detail_table, dict):  # 如果详细表是字典
            for section_id, details in detail_table.items():
                conditions = details.get("conditions", [])
                processes = details.get("processes", [])
                print(f"Section ID: {section_id}")
                print(f"Conditions: {conditions}")
                print(f"Processes: {processes}")
        else:
            logger.warning("详细表不是字典，无法解析")

        # 返回解析结果
        return summary_table, detail_table

    except Exception as e:
        logger.error(f"解析文件时发生错误: {e}")
        return None, None  # 返回空值以避免解包错误

def main():
    # 文件路径写死在程序中
    file_path = r"C:\Users\9512601\Desktop\0920\IPOソース参照\MAQR6200.ipo"  # 替换为实际路径

    # 调用解析函数
    summary_table, detail_table = parse_file(file_path)
if __name__ == "__main__":
    main()