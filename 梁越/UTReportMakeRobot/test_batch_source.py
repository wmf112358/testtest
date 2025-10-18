from Batch_source import analyze_program

def main():
    file_path = r'C:\Users\9512601\Desktop\0920\IPOソース参照\MAQR5600.ipo'
    pgm_id = 'MAQR5600'
    result = analyze_program(file_path, pgm_id)
    
    # 格式化打印结果
    print("\n返回结果:")
    for key, value in result.items():
        print(f"\n{key}:")
        for k, v in value.items():
            print(f"  {k}: {v}")

if __name__ == "__main__":
    main()