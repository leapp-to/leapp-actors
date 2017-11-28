import json
import sys
import re


facts = json.load(sys.stdin)["source_ansible_setup"][0]["ansible_facts"]
interface_pattern = re.compile('^ansible_(wl|e(th|n|m))')
ips = []
for interface in facts.keys():
    if interface_pattern.search(interface):
        ipv4 = facts[interface].get("ipv4", {})
        if not isinstance(ipv4, list):
            ipv4 = (ipv4,)
        for item in ipv4:
            ip = item.get("address")
            if ip:
                ips.append(ip)
result = {
    "ip_list": [{"ips": ips}],
    "hostnameinfo": [{"hostname": facts["ansible_hostname"]}],
    "osversion": [{
        "name": facts["ansible_distribution"],
        "version": facts["ansible_distribution_version"]}]}
sys.stdout.write(json.dumps(result))
