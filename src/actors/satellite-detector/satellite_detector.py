#!/usr/bin/env python

import requests
import shlex

from subprocess import Popen, PIPE

from ansible.module_utils.basic import AnsibleModule


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
}

DOCUMENTATION = '''
---
module: satellite_detector

short_description: This module will detect satellite installation and its services


description:
    - "This module will detect satellite 5 or 6 installation and its respective services services"
    - Output example:
        10.10.10.21 | SUCCESS => {
            "changed": false,
            "failed": false,
            "satellite_detected": true,
            "satellite_services": [
                "rh-postgresql95-postgresql",
                "jabberd",
                "tomcat6",
                "httpd",
                "osa-dispatcher",
                "rhn-search",
                "cobblerd",
                "taskomatic"
            ],
            "satellite_version_bugfix": "0.31",
            "satellite_version_major": "5",
            "satellite_version_minor": "8"
        }                                                                                                }
    - Marcel Gazdik
'''

EXAMPLES = '''
- name: Detect satellite installation
  satellite_detector: ""
  register: detection_result
'''

RETURN = '''
satellite_detected:
    description: A flag determining whether a satellite installation was detecgted
    type: boolean

satellite_services:
    description: An array holding lost of services if satellite was found. This field is not
                 not provided, if there is no satellite detected.
    type: array of strings

satellite_version_major:
    description: An major version of found satellite instance. This field is not
                 not provided, if there is no satellite detected.
    type: string

satellite_version_minor:
    description: An minor version of found satellite instance. This field is not
                 not provided, if there is no satellite detected.
    type: string

satellite_version_bugfix:
    description: An bugfix version of found satellite instance. This field is not
                 not provided, if there is no satellite detected.
    type: string
'''


class DetectionFailed(RuntimeError):
    pass


def extract_version(version_string, result):
    version_sep = version_string.split(".")
    result["satellite_version_major"] = version_sep[0]
    result["satellite_version_minor"] = version_sep[1]
    result["satellite_version_bugfix"] = ".".join(version_sep[2:])


def execute_cmd(cmd, shell=False):
    if not shell:
        cmd = shlex.split(cmd)

    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=shell)
    out, err = process.communicate()

    return (process, out, err)


def detect_satellite5():
    verif_process, verif_out, _ = execute_cmd("rpm -q satellite-schema --qf %{VERSION}")

    if not verif_process.returncode:
        result = dict(
            satellite_detected=True,
        )

        # Version
        extract_version(verif_out, result)

        # Services
        services_process, serv_out, _ = execute_cmd(
            cmd='eval \"$('
                'sed -e \"s/exit/:/\" -e \"s/\$0/\$PWD)/g\" $('
                'which rhn-satellite))\" 2>&1 > /dev/null; echo -n $SERVICES',
            shell=True)

        if services_process.returncode:
            raise DetectionFailed()

        if serv_out is not None:
            result["satellite_services"] = serv_out.split(" ")

            # Optional services
            services_process, _, _ = execute_cmd("chkconfig --list dhcpd | grep on", shell=True)
            if not services_process.returncode:
                result["satellite_services"].append("dhcp")

            services_process, _, _ = execute_cmd("chkconfig --list --type xinetd tftp | grep on", shell=True)
            if not services_process.returncode:
                result["satellite_services"].append("tftp")

            return result

    return None


def detect_satellite6():
    verif_process, verif_out, _ = execute_cmd("rpm -q satellite --qf %{VERSION}")

    if not verif_process.returncode:
        result = dict(
            satellite_detected=True,
        )

        extract_version(verif_out, result)

        services_process, serv_out, _ = execute_cmd(
            cmd="echo -n $(katello-service list | sed -e 's/^\\([^[:space:]]\\+\\).*/\\1/g' -e 's/\\.service$//')",
            shell=True)

        if services_process.returncode:
            raise DetectionFailed()

        if serv_out is not None:
            result["satellite_services"] = serv_out.split(" ")
            features = []

            try:
                features = requests.get("https://localhost:9090/features", verify=False).json()
            except Exception:
                raise DetectionFailed()

            result["satellite_services"] = set(result["satellite_services"] + features)
            return result
        else:
            raise DetectionFailed()

    return None


def detect_satellite():
    sat5_detection = detect_satellite5()
    if sat5_detection is not None:
        return sat5_detection

    sat6_detection = detect_satellite6()
    if sat6_detection is not None:
        return sat6_detection

    return None


def run_module():
    result = dict(
        satellite_detected=False,
        satellite_version_major=None,
        satellite_version_minor=None,
        satellite_version_bugfix=None,
        satellite_services=[]
    )

    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    detected = detect_satellite()

    if detected is not None:
        module.exit_json(**detected)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
