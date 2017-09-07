import jsl
from osversion import OSVersion
from hostnameinfo import HostnameInfo
from iplist import IPList
from rpmlist import RPMPackages


class MachineInfo(jsl.Document):
    osversion = jsl.DocumentField(OSVersion(), as_ref=True)
    hostnameinfo = jsl.DocumentField(HostnameInfo(), as_ref=True)
    iplist = jsl.DocumentField(IPList(), as_ref=True)
    rpm_packages = jsl.DocumentField(RPMPackages(), as_ref=True)
