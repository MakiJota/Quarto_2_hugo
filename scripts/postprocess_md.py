import os
import re

print("=== Python postprocessor STARTED ===")

# Path to the content folder maybe need to change
content_dir = "content/"

# Find the first .md file (alphabetically), also inside subfolders
md_files = []
for root, dirs, files in os.walk(content_dir):
    for f in files:
        if f.endswith(".md"):
            md_files.append(os.path.relpath(os.path.join(root, f), content_dir))

md_files = sorted(md_files)
print(md_files)

if not md_files:
    raise FileNotFoundError("No .md files found in content/")

input_file = os.path.join(content_dir, md_files[0])
print("Processing first Markdown file:", input_file)
# Read Markdown
with open(input_file, "r", encoding="utf-8") as f:
    md = f.read()

# ---------- Wrap <figure> blocks ----------
def wrap_figure(match):
    figure_html = match.group(0)
    figure_html = re.sub(r'data-fig\.[^=]+="[^"]*"', '', figure_html)
    figure_html = re.sub(r'aria-hidden="true"', '', figure_html)
    return f'<div class="blog-content">\n{figure_html}\n</div>'

md = re.sub(r'<figure.*?>.*?</figure>', wrap_figure, md, flags=re.DOTALL)
print("Figures wrapped")

# ---------- Wrap table1 ----------
def wrap_table1(match):
    content = match.group(1).strip()
    return f"""
<div id="table1" style="display: flex; gap: 50px; flex-wrap: wrap; justify-content: center; text-align: center;">
  <div>
{content}
  </div>
</div>
"""

pattern_table1 = re.compile(
    r"<!--\s*table1:start\s*-->\s*(.*?)\s*<!--\s*table1:end\s*-->",
    re.DOTALL,
)
md = pattern_table1.sub(wrap_table1, md)
print("table1 wrapped")

# ---------- Wrap table2 ----------
def wrap_table2(match):
    content = match.group(1).strip()

    # Split each section by level-3 heading (###)
    sections = re.split(r"^###\s+", content, flags=re.MULTILINE)
    html_sections = []

    for sec in sections:
        if not sec.strip():
            continue
        lines = sec.split("\n")
        heading = lines[0].strip()  # first line after ###
        body = "\n".join(lines[1:]).rstrip()
        html_sections.append(f"""
  <div>
    <h5>{heading}</h5>
{body}
  </div>
""")

    # Wrap all sections in one flex container
    return f"""
<div id="table2" style="display: flex; gap: 50px; flex-wrap: wrap; justify-content: center; text-align: center;">
{''.join(html_sections)}
</div>
"""

pattern_table2 = re.compile(
    r"<!--\s*table2:start\s*-->\s*(.*?)\s*<!--\s*table2:end\s*-->",
    re.DOTALL,
)
md = pattern_table2.sub(wrap_table2, md)
print("table2 wrapped")

# Overwrite the same file
with open(input_file, "w", encoding="utf-8") as f:
    f.write(md)

print("Cleaned Markdown saved:", input_file)
print("=== Python postprocessor FINISHED ===")
