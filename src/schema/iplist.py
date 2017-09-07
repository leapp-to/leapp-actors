import jsl


class IPList(jsl.Document):
    ips = jsl.ArrayField(jsl.IPv4Field())
