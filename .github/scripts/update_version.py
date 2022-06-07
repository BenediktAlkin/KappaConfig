import argparse

def get_tagname():
    parser = argparse.ArgumentParser(description='Replace version in setup.cfg with the created git tag')
    parser.add_argument('--tagname', help='tag name', required=True)
    args = parser.parse_args()
    return args.tagname.replace("v", "")

with open("setup.cfg") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].startswith("version"):
        print(f"old version line: {lines[i]}")
        lines[i] = f"version = {get_tagname()}"
        print(f"new version line: {lines[i]}")

with open("setup.cfg", "w") as f:
    f.writelines(lines)