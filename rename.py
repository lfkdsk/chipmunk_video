#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量重命名脚本 - 删除文件名中的 "2-XP01-_2025-" 前缀
如果重命名后有重复，自动添加 _1, _2 等后缀
适用于所有操作系统 (Windows/Mac/Linux)
"""

import os
import re
from pathlib import Path

def remove_prefix_and_handle_duplicates(directory_path=".", prefix_pattern="2-XP01-_2025-"):
    """
    删除指定目录下所有文件名中的前缀，处理重复文件名

    Args:
        directory_path: 目标目录路径，默认为当前目录
        prefix_pattern: 要删除的前缀模式
    """

    # 创建 Path 对象
    directory = Path(directory_path)

    if not directory.exists():
        print(f"错误：目录 '{directory_path}' 不存在！")
        return

    renamed_count = 0

    # 遍历目录中的所有文件
    for file_path in directory.iterdir():
        if file_path.is_file():
            old_name = file_path.name

            # 检查文件名是否以指定前缀开头
            if old_name.startswith(prefix_pattern):
                # 删除前缀
                base_new_name = old_name[len(prefix_pattern):]

                # 如果删除前缀后文件名为空，跳过
                if not base_new_name:
                    print(f"警告：删除前缀后文件名为空，跳过 '{old_name}'")
                    continue

                # 处理重复文件名
                new_name = get_unique_filename(directory, base_new_name)
                new_path = directory / new_name

                try:
                    # 重命名文件
                    file_path.rename(new_path)
                    print(f"✓ 重命名：'{old_name}' -> '{new_name}'")
                    renamed_count += 1
                except Exception as e:
                    print(f"错误：无法重命名 '{old_name}' - {e}")

    print(f"\n完成！共重命名了 {renamed_count} 个文件。")

def get_unique_filename(directory, base_name):
    """
    获取唯一的文件名，如果存在重复则添加数字后缀

    Args:
        directory: 目录路径
        base_name: 基础文件名

    Returns:
        唯一的文件名
    """
    # 分离文件名和扩展名
    name_parts = base_name.rsplit('.', 1)
    if len(name_parts) == 2:
        name_without_ext, extension = name_parts
        extension = '.' + extension
    else:
        name_without_ext = base_name
        extension = ''

    # 检查基础文件名是否存在
    test_path = directory / base_name
    if not test_path.exists():
        return base_name

    # 如果存在，尝试添加数字后缀
    counter = 1
    while True:
        new_name = f"{name_without_ext}_{counter}{extension}"
        test_path = directory / new_name
        if not test_path.exists():
            return new_name
        counter += 1

def preview_changes(directory_path=".", prefix_pattern="2-XP01-_2025-"):
    """
    预览将要进行的重命名操作，不实际执行
    """
    directory = Path(directory_path)

    if not directory.exists():
        print(f"错误：目录 '{directory_path}' 不存在！")
        return

    changes = []
    used_names = set()

    for file_path in directory.iterdir():
        if file_path.is_file():
            old_name = file_path.name
            if old_name.startswith(prefix_pattern):
                base_new_name = old_name[len(prefix_pattern):]

                if not base_new_name:
                    continue

                # 模拟获取唯一文件名的过程
                new_name = simulate_unique_filename(used_names, base_new_name)
                used_names.add(new_name)
                changes.append((old_name, new_name))

    if changes:
        print("预览重命名操作：")
        print("-" * 80)
        for old, new in changes:
            print(f"'{old}' -> '{new}'")
        print("-" * 80)
        print(f"总共 {len(changes)} 个文件将被重命名")
    else:
        print(f"没有找到以 '{prefix_pattern}' 开头的文件。")

def simulate_unique_filename(used_names, base_name):
    """
    模拟获取唯一文件名的过程（用于预览）
    """
    # 分离文件名和扩展名
    name_parts = base_name.rsplit('.', 1)
    if len(name_parts) == 2:
        name_without_ext, extension = name_parts
        extension = '.' + extension
    else:
        name_without_ext = base_name
        extension = ''

    # 检查基础文件名是否已被使用
    if base_name not in used_names:
        return base_name

    # 添加数字后缀
    counter = 1
    while True:
        new_name = f"{name_without_ext}_{counter}{extension}"
        if new_name not in used_names:
            return new_name
        counter += 1

def custom_prefix_mode():
    """
    自定义前缀模式
    """
    print("当前默认前缀：2-XP01-_2025-")
    custom = input("请输入要删除的前缀（回车使用默认值）: ").strip()
    return custom if custom else "2-XP01-_2025-"

if __name__ == "__main__":
    import sys

    # 获取目标目录
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."

    print("批量重命名工具 - 删除文件名前缀")
    print("=" * 50)

    # 让用户选择前缀
    prefix_to_remove = custom_prefix_mode()
    print(f"将删除前缀：'{prefix_to_remove}'")

    # 首先预览更改
    print(f"\n1. 预览将要进行的更改...")
    preview_changes(target_dir, prefix_to_remove)

    # 询问用户确认
    confirm = input("\n确定要执行重命名操作吗？(y/N): ").lower().strip()

    if confirm in ['y', 'yes', '是']:
        print("\n2. 开始重命名...")
        remove_prefix_and_handle_duplicates(target_dir, prefix_to_remove)
    else:
        print("操作已取消。")

# 使用示例：
# 1. 在当前目录运行：python script.py
# 2. 指定目录运行：python script.py /path/to/your/files
#
# 重命名规则：
# - 删除指定前缀
# - 如果重命名后有重复，自动添加 _1, _2, _3... 后缀
# - 保持文件扩展名不变