import logging
from section_extractor import (
    extract_section_ids_from_file,
    extract_section_details_from_file,
    batch_extract_section_ids,
    SectionIdExtractor
)

# 日志配置
LOG_FILE = "test_section_extractor.log"
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

def print_and_log(msg):
    # print(msg)  # 注释掉或删除这一行
    logger.info(msg)

def print_section_results(section_ids, pgm_id):
    msg = f"\n📋 {pgm_id} 的SECTION ID列表:\n" + "=" * 50
    print_and_log(msg)
    if not section_ids:
        print_and_log("   ❌ 未找到任何SECTION ID")
        return
    for i, section_id in enumerate(section_ids, 1):
        print_and_log(f"   {i:2d}. {section_id}")
    print_and_log(f"\n✅ 总计: {len(section_ids)} 个SECTION ID")

def print_section_details(section_details, pgm_id):
    msg = f"\n📋 {pgm_id} 的SECTION详细信息:\n" + "=" * 70
    print_and_log(msg)
    if not section_details:
        print_and_log("   ❌ 未找到任何SECTION")
        return
    for i, detail in enumerate(section_details, 1):
        print_and_log(f"   {i:2d}. SECTION ID: {detail['section_id']}")
        print_and_log(f"       行号: {detail['line_number']}")
        print_and_log(f"       内容: {detail['line_content']}\n")
    print_and_log(f"✅ 总计: {len(section_details)} 个SECTION")

def main(test_file=None, test_pgm_id=None):
    print_and_log("🧪 SECTION ID 提取器测试")
    print_and_log("=" * 60)
    if test_file is None:
        test_file = r'C:\Users\9512601\Desktop\0920\IPOソース参照\MAQP2300.ipo'
    if test_pgm_id is None:
        test_pgm_id = "MAQP2300"
    try:
        print_and_log("\n📝 测试1: 基本SECTION ID提取")
        section_ids = extract_section_ids_from_file(test_file, test_pgm_id)
        print_section_results(section_ids, test_pgm_id)

        print_and_log("\n📝 测试2: SECTION详细信息提取")
        section_details = extract_section_details_from_file(test_file, test_pgm_id)
        print_section_details(section_details, test_pgm_id)

        print_and_log(f"\n🎯 返回给调用函数的数组格式:")
        print_and_log(f"   类型: {type(section_ids)}")
        print_and_log(f"   内容: {section_ids}")
        print_and_log(f"   长度: {len(section_ids)}")
        # 控制台打印返回的数组内容
        print("\n【extract_section_ids_from_file 返回内容】")
        print(section_ids)

        print_and_log(f"\n📝 测试4: 批量处理示例")
        file_list = [(test_file, test_pgm_id)]
        batch_results = batch_extract_section_ids(file_list)
        for pgm_id, sections in batch_results.items():
            print_and_log(f"   {pgm_id}: {sections}")
        # 控制台打印批量处理结果
        print("\n【batch_extract_section_ids 返回内容】")
        print(batch_results)

    except FileNotFoundError:
        print_and_log(f"⚠️ 测试文件不存在: {test_file}")
        print_and_log("请修改测试文件路径")
        print_and_log(f"\n📝 创建示例测试数据:")
        sample_lines = [
            "       IDENTIFICATION DIVISION.",
            "       PROGRAM-ID. MAQR8700.",
            "       ",
            "       PROCEDURE DIVISION.",
            "       MAIN-PROCESS SECTION.",
            "           DISPLAY 'MAIN PROCESS'.",
            "       ",
            "       FILE-PROCESS SECTION.",
            "           DISPLAY 'FILE PROCESS'.",
            "       ",
            "       CALC-SECTION SECTION.",
            "           DISPLAY 'CALCULATION'.",
            "       ",
            "       END-PROCESS SECTION.",
            "           DISPLAY 'END PROCESS'."
        ]
        extractor = SectionIdExtractor()
        sample_sections = extractor._extract_section_ids_from_lines(sample_lines)
        print_section_results(sample_sections, "SAMPLE")
        # 控制台打印示例数组
        print("\n【extract_section_ids_from_file 返回内容】")
        print(sample_sections)
    except Exception as e:
        print_and_log(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    main(
        test_file=r'C:\Users\9512601\Desktop\smartTOOL\IPOソース参照\MAQR8700.ipo',
        test_pgm_id='MAQR8700'
    )