import os
import json

# 可选：限定扩展名，如只生成 .mp4 文件名
EXTENSION = ".mp4"   # 设置为 None 表示不过滤

OUTPUT_FILE = "file_list.json"

def main():
    if EXTENSION:
        files = sorted(f for f in os.listdir(".") if (f.lower().endswith(EXTENSION) or f.lower().endswith(".MOV")) and os.path.isfile(f))
    else:
        files = sorted(f for f in os.listdir(".") if os.path.isfile(f))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(files, f, ensure_ascii=False)

    print(f"✅ JSON 写入成功，共 {len(files)} 个文件 → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

