import os
import re

def get_title(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    return os.path.basename(file_path)

def update_index():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(base_dir, 'index.html')
    
    html_files = [f for f in os.listdir(base_dir) if f.endswith('.html') and f != 'index.html']
    html_files.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)
    
    links_html = ""
    for file in html_files:
        title = get_title(os.path.join(base_dir, file))
        # Optional: categorize or style -client files differently
        badge = ""
        if file.endswith('-client.html'):
            badge = " <span class='badge'>Client View</span>"
        
        links_html += f"        <li><a href=\"{file}\">{title}{badge}</a></li>\n"

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the ul tag and replace its content
    pattern = re.compile(r'(<ul>)(.*?)(</ul>)', re.DOTALL)
    new_content = pattern.sub(f'\\1\n{links_html}    \\3', content)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    update_index()
