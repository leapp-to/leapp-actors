from json import load, dumps
import sys

keys = {
    "in": "string_list",
    "out": "csv_string"
}

for arg in sys.argv[1:]:
    try:
        key, value = arg.split('=')
        keys[key] = value
    except ValueError:
        pass

inputs = load(sys.stdin)[keys["in"]][0]["value"]
output_str = ""


for item in inputs:
    if len(output_str):
        output_str += ", "
    output_str += str(item)

print(dumps({keys["out"]: [{"value": output_str}]}))
