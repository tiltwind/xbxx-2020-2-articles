import re
import os

# 读取学生姓名列表
students_file = '/Users/hk/Downloads/六2学生作文/students.md'
with open(students_file, 'r', encoding='utf-8') as f:
    students = [line.strip() for line in f if line.strip()]

# 获取原始目录下所有的Markdown文件
raw_dir = '/Users/hk/Downloads/六2学生作文/原始'
md_files = [os.path.join(raw_dir, file) for file in os.listdir(raw_dir) if file.endswith('.md')]

# 处理每个文件
for file_path in md_files:
    print(f'处理文件: {os.path.basename(file_path)}')
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 构建正则表达式模式
    # 匹配：标题行 + 空行 + 学生姓名行
    pattern = r'^([^\s]+)$\n\n^(' + '|'.join(re.escape(s) for s in students) + r')$'
    
    # 使用多行模式进行替换
    new_content = re.sub(pattern, r'\1 \2', content, flags=re.MULTILINE)
    
    # 保存修改后的内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

print('所有文件处理完成！')
