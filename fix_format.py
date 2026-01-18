import re

# 读取学生姓名列表
students_file = '/Users/hk/Downloads/六2学生作文/students.md'
with open(students_file, 'r', encoding='utf-8') as f:
    students = [line.strip() for line in f if line.strip()]

# 读取要处理的文件
file_path = '/Users/hk/Downloads/六2学生作文/原始/我得到了——（14无）.md'
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

print('处理完成！')
