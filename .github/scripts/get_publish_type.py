import argparse

def get_tagname():
    parser = argparse.ArgumentParser(description='Replace version in setup.cfg with the created git tag')
    parser.add_argument('--tagname', help='tag name', required=True)
    args = parser.parse_args()
    return args.tagname

tagname = get_tagname()
# check if tag is valid
assert tagname[0] == "v", "tagname must start with 'v'"
version_numbers = tagname[1:].split(".")
version_number_count = len(version_numbers)
assert version_number_count == 3 or version_number_count == 4, \
    "version must contain 3 (for prod publish) or 4 (for test publish) numbers"

if version_number_count == 3:
    publish_type = "prod"
else:
    publish_type = "dev"
print(f"::set-output name=publish_type::{publish_type}")