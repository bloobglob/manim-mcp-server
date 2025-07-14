import os

custom_docs_dir = "custom_docs"

for fname in os.listdir(custom_docs_dir):
    if fname.endswith(".txt"):
        path = os.path.join(custom_docs_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) >= 3:
                # Remove leading '#' and whitespace from first line
                name = lines[0].lstrip("#").strip()
                desc = lines[2].strip()
                print(f"{name}: {desc}")