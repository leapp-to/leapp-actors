#!/usr/bin/env python
import requests
import sys

import json

from subprocess import Popen, PIPE
import shlex


class DetectionFailed(Exception):
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

    return (process.returncode, out, err)


def detect_satellite5():
    # TODO: get this information from rpm actor (input rpm)
    verif_code, verif_out, _ = execute_cmd("rpm -q satellite-schema --qf %{VERSION}")

    if not verif_code:
        result = dict(
            satellite_detected=True,
        )

        # Version
        extract_version(verif_out, result)

        # Services
        services_code, serv_out, _ = execute_cmd(
            cmd='rhn-satellite list | grep -e \":on\" -e \":off\" | awk \'{print $1}\'',
            shell=True)

        if services_code or serv_out is None:
            raise DetectionFailed("Satellite services could not be detected")

        result["satellite_services"] = serv_out.split("\n")

        # Optional services
        # TODO: get this information from chkconfig actor (input chkconfig)
        services_code, _, _ = execute_cmd("chkconfig --list dhcpd | grep on", shell=True)
        if not services_code:
            result["satellite_services"].append("dhcp")

        services_code, _, _ = execute_cmd("chkconfig --list --type xinetd tftp | grep on", shell=True)
        if not services_code:
            result["satellite_services"].append("tftp")

        return result

    return None


def detect_satellite6():
    # TODO: get this information from rpm actor (input rpm)
    verif_code, verif_out, _ = execute_cmd("rpm -q satellite --qf %{VERSION}")

    if not verif_code:
        result = dict(
            satellite_detected=True,
        )

        extract_version(verif_out, result)

        services_code, serv_out, _ = execute_cmd(
            cmd="echo -n $(katello-service list | sed -e 's/^\\([^[:space:]]\\+\\).*/\\1/g' -e 's/\\.service$//')",
            shell=True)

        if services_code or serv_out is None:
            raise DetectionFailed("Satellite services could not be detected")

        result["satellite_services"] = serv_out.split(" ")
        features = []

        try:
            features = list(requests.get("https://localhost:9090/features", verify=False).json())
        except Exception:
            raise DetectionFailed("Capsule features could not be detected")

        result["satellite_services"] = list(set(result["satellite_services"] + features))
        return result

    return None


def detect_satellite():
    sat5_detection = detect_satellite5()
    if sat5_detection is not None:
        return sat5_detection

    sat6_detection = detect_satellite6()
    if sat6_detection is not None:
        return sat6_detection

    return {"satellite_detected": False}


if __name__ == '__main__':
    print(json.dumps({"app_satellite_detection": [detect_satellite()]}))
