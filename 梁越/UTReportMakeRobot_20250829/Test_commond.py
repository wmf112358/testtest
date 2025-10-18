import logging
from commond import extract_program_header

# 日志配置
LOG_FILE = "test_commond.log"
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

def log_only(msg):
    logger.info(msg)

def main(file_path, pgm_id):
    try:
        log_only(f"调用commond，路径: {file_path}，程序ID: {pgm_id}")
        result = extract_program_header(file_path, pgm_id)
        arr = [result.program_id, result.program_name, result.pattern_id]
        print("即将输出数组：")
        print(arr)  # 只打印返回的数组到控制台
        log_only(f"返回数组: {arr}")
    except Exception as e:
        log_only(f"❌ commond调用失败: {e}")

if __name__ == "__main__":
    # 这里直接指定测试文件路径和PGMID
    file_path = r'C:\Users\9512601\Desktop\smartTOOL\IPOソース参照\MAQR8700.ipo'
    pgm_id = 'MAQR8700'
    main(file_path, pgm_id)