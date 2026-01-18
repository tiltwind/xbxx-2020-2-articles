#!/usr/bin/env python3
import os
import re

def fix_newlines_in_file(file_path):
    """将文件中连续超过3个的换行符替换为2个换行符"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 将连续超过3个的换行符替换为2个换行符
        # 处理所有类型的换行符，并处理包含空白字符的空行
        # 1. 先将\r\n转换为\n
        content = content.replace('\r\n', '\n')
        # 2. 将包含空格或制表符的空行转换为纯换行符
        content = re.sub(r'\n[ \t]+\n', '\n\n', content)
        # 3. 将连续3个或更多的换行符替换为2个换行符
        fixed_content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 只有当内容确实发生变化时才保存文件
        if content != fixed_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"已修复: {os.path.basename(file_path)}")
        else:
            print(f"无需修复: {os.path.basename(file_path)}")
            
    except Exception as e:
        print(f"处理文件 {os.path.basename(file_path)} 时出错: {e}")

def main():
    """主函数"""
    markdown_dir = '/Users/hk/Downloads/六2学生作文/markdown'
    
    # 检查目录是否存在
    if not os.path.exists(markdown_dir):
        print(f"目录不存在: {markdown_dir}")
        return
    
    # 遍历目录下的所有.md文件
    for filename in os.listdir(markdown_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(markdown_dir, filename)
            fix_newlines_in_file(file_path)
    
    print("\n所有文件处理完成!")

if __name__ == "__main__":
    main()