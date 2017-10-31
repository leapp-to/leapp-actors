import json
import sys
data = json.load(sys.stdin)
sys.stderr.write("\nREAD DATA: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" +
                 json.dumps(data) + "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
data = data["rpm_packages"][0]
data["packages"] = [p for p in data["packages"] if p["name"].find(sys.argv[1]) != -1]
sys.stdout.write(json.dumps({"filtered_packages": [data]}) + '\n')
