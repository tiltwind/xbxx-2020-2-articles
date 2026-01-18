import os
import re
from pathlib import Path

def main():
    # 读取学生名单
    students_path = "/Users/hk/Downloads/六2学生作文/students.md"
    students = set()
    with open(students_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                # 提取姓名（去掉行号）
                name = line.split('→')[-1].strip()
                students.add(name)
    
    print(f"读取到 {len(students)} 名学生")
    
    # 创建输出目录并清空
    output_dir = "/Users/hk/Downloads/六2学生作文/markdown"
    os.makedirs(output_dir, exist_ok=True)
    
    # 清空输出目录中的所有文件
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # 遍历原始目录下的所有.md文件
    raw_dir = "/Users/hk/Downloads/六2学生作文/原始"
    # 调整正则表达式，确保只匹配标题+空格+姓名的格式
    # 改进：使用更精确的匹配，确保姓名部分是学生名单中的名字
    
    # 构建姓名的正则表达式部分，使用|连接所有学生姓名
    name_pattern = '|'.join(re.escape(name) for name in students)
    # 构建完整的文章标题行正则表达式
    article_pattern = re.compile(rf'^(.*?)(\s{{2,}})({name_pattern})$')
    
    for filename in os.listdir(raw_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(raw_dir, filename)
            print(f"处理文件: {filename}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 分割文件内容为行
            lines = content.split('\n')
            current_title = None
            current_author = None
            current_article = []
            
            for line in lines:
                line = line.rstrip('\r\n')
                
                # 尝试匹配文章标题行
                # 先使用更宽松的模式检测文章标题行
                # 修改正则表达式，匹配一个或多个空格
                title_line_pattern = re.compile(r'^(.*?)(\s+)([^\s]+)$')
                loose_match = title_line_pattern.match(line)
                
                if loose_match:
                    # 新文章开始，不管作者是谁，都保存当前文章
                    if current_title and current_author:
                        save_article(output_dir, current_author, current_title, current_article)
                    
                    # 提取信息
                    title = loose_match.group(1).strip()
                    spaces = loose_match.group(2)
                    author = loose_match.group(3).strip()
                    
                    # 检查作者是否在学生名单中
                    if author in students:
                        current_title = title
                        current_author = author
                        # 为标题行添加一级标题标记
                        current_article = [f"# {title}{spaces}{author}"]
                    else:
                        # 作者不在名单中，跳过
                        current_title = None
                        current_author = None
                        current_article = []
                elif current_title and current_author:
                    # 文章内容行
                    current_article.append(line)
            
            # 保存最后一篇文章
            if current_title and current_author:
                save_article(output_dir, current_author, current_title, current_article)
    
    print("\n处理完成！")

def save_article(output_dir, author, title, article_lines):
    # 创建学生文件路径
    output_path = os.path.join(output_dir, f"{author}.md")
    
    # 写入新文章
    with open(output_path, 'a', encoding='utf-8') as f:
        # 写入文章内容
        for line in article_lines:
            f.write(line + '\n')
    
    print(f"  保存文章: {title}  - {author}")

if __name__ == "__main__":
    main()