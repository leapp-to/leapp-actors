from json import load, dumps
import sys

inputs = load(sys.stdin)["string_list"]["value"]
output_str = ""


for item in inputs:
    if len(output_str):
        output_str += ", "
    output_str += str(item)

print(dumps({"csv_string": {"value": output_str}}))
