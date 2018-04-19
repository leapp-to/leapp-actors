import json
import os
import subprocess


pkgs = ["NetworkManager-gnome", "control-center", "gdm",
        "gdm-user-switch-applet", "gnome-panel", "gnome-power-manager",
        "gnome-screensaver", "gnome-session", "gnome-terminal", "gvfs-archive",
        "gvfs-fuse", "gvfs-smb", "metacity", "nautilus", "notification-daemon",
        "polkit-gnome", "xdg-user-dirs-gtk", "yelp", "control-center-extra",
        "eog", "gdm-plugin-fingerprint", "gnome-applets", "gnome-media",
        "gnome-packagekit", "gnome-vfs2-smb", "gok", "orca", "vino"]


def gnome_session_exists():
    return os.path.exists("/usr/share/xsessions/gnome.desktop")


def gnome_pkgs_installed():
    devnull = open(os.devnull, 'w')
    for pkg in pkgs:
        retcode = subprocess.call(["rpm", "-q", pkg],
                                  stdout=devnull, stderr=devnull)
        if retcode != 0:
            return True
    return False

def construct_report_msg(session_exists, pkgs_installed):
    status = "PASS"
    summary = "You don't have GNOME desktop environment installed."

    if session_exists or pkgs_installed:
        status = "FAIL"
        summary = "You have the GNOME desktop environment installed. Its new" \
                  " version is not backwards compatible with the currently" \
                  " installed one. Continuing with the upgrade would leave" \
                  " the system without a functional GNOME desktop environment."

    check_result = {
        "check_actor": "gnome",
        "status": status,
        "summary": summary,
        "params": [""]
    }
    return {"check_output": [{"checks": [check_result]}]}


def publish_output(output_msg):
    print(json.dumps(output_msg))


session_exists = gnome_session_exists()
pkgs_installed = gnome_pkgs_installed()
output_msg = construct_report_msg(session_exists, pkgs_installed)
publish_output(output_msg)
