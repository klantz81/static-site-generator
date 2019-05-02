from pathlib import Path
import markdown
import re

base_path = Path(__file__).resolve().parent
base_template = base_path / "templates/base.html"
site_folder = base_path / "site"
output_folder = base_path / "output"

def process_file(file, template, output):
    f = file.read_text()
    t = template.read_text()
    content = markdown.markdown(f)
    res = t.replace("{{content}}", content)
    output.write_text(res)

def rm(f):
    if f.is_dir():
        sub = f.glob("*")
        for d in sub:
            rm(d)
        f.rmdir()
    elif f.is_file():
        f.unlink()

rm(output_folder)

input_files = sorted(site_folder.glob('**/*'))
for input_file in input_files:
    if input_file.is_file():
        output_file_str = str(input_file).replace(str(site_folder), str(output_folder), 1)
        output_file = Path(output_file_str).with_suffix(".html")
        output_file.parent.mkdir(parents = True, exist_ok = True)
        print("processing "+str(input_file))
        process_file(input_file, base_template, output_file)
