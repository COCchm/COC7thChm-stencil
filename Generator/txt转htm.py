# 硬编码路径
DEFAULT_INPUT_DIR = "../克苏鲁神话原著"

import os
import sys

# 程序路径
PROGRAM_PATH = os.path.dirname(os.path.abspath(__file__))

def convert_txt_to_html(folder_path):
    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                txt_path = os.path.join(root, file)
                htm_path = os.path.splitext(txt_path)[0] + '.htm'
                
                # 检测文件编码并读取
                import chardet
                with open(txt_path, 'rb') as f:
                    raw_data = f.read()
                    encoding = chardet.detect(raw_data)['encoding']
                try:
                    with open(txt_path, 'r', encoding=encoding) as f:
                        lines = f.readlines()
                except:
                    # 如果自动检测失败，尝试常见编码
                    encodings = ['utf-8', 'gbk', 'gb18030', 'big5']
                    for enc in encodings:
                        try:
                            with open(txt_path, 'r', encoding=enc) as f:
                                lines = f.readlines()
                            break
                        except:
                            continue
                    
                # 生成HTML内容
                if lines:
                    title = lines[0].strip()
                    # 将每行内容包裹在<p>标签中
                    content = ''.join([f'<p>{line.strip()}</p>\n' for line in lines[1:]])
                    
                    htm_content = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>{title}</title>
<meta name="GENERATOR" content="WinCHM">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="d:\coc不全书\coc7thchm\style.css">
<style></style>
</head>
<body>
<P><STRONG><FONT color=#800000 size=6>{title}</FONT></STRONG></P>
{content}
</body>
</html>"""
                    
                    # 写入HTM文件
                    with open(htm_path, 'w', encoding='utf-8') as f:
                        f.write(htm_content)
                    print(f'Converted: {txt_path} -> {htm_path}')
                    
                    # 删除原始TXT文件
                    try:
                        os.remove(txt_path)
                        print(f'Deleted: {txt_path}')
                    except Exception as e:
                        print(f'Error deleting {txt_path}: {str(e)}')

if __name__ == '__main__':
    # 如果没有提供参数，使用默认路径
    if len(sys.argv) == 1:
        folder_path = DEFAULT_INPUT_DIR
    elif len(sys.argv) == 2:
        folder_path = sys.argv[1]
    else:
        print('Usage: python txt转htm.py [folder_path]')
        sys.exit(1)
        
    if os.path.isdir(folder_path):
        convert_txt_to_html(folder_path)
    else:
        print(f'Error: {folder_path} is not a valid directory')
