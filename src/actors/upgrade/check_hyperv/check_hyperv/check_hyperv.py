#!/usr/bin/env python

import json
import os
import re


keys = {
    'hypervisor': 'vendor',
    'report': 'check_output'
}


def check_hyperv():
    lscpu = os.popen('lscpu').read()
    line = re.search(r"(Hypervisor\s+vendor):\s+(.*)$", lscpu,
                     flags=re.MULTILINE)
    if line:
        vendor = line.group(2)
        if 'Microsoft' in vendor:
            summary = "The system is running as a Hyper-V" \
                      " guest on Microsoft Windows host"
            status = 'FAIL'

        else:
            summary = "The system is running as a virtualized guest"
            status = 'PASS'
    else:
        summary = "System is not virtualized"
        status = 'PASS'
        vendor = ''
    vendor = [vendor]
    result = [{
        'check_actor': 'check_hyperv',
        'status': status,
        'summary': summary,
        'params': vendor
    }]
    report = [{'checks': result}]
    print(json.dumps({keys['report']: report}))


check_hyperv()
