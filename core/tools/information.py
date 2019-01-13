str = """Computer        : JOHNDOE-PC
OS              : Windows 7 (Build 7601, Service Pack 1).
Architecture    : x64
System Language : fr_FR
Domain          : WORKGROUP
Logged On Users : 2
Meterpreter     : x64/windows"""

import time


def get_sysinfo(shell):
    shell.write('sysinfo\n')
    result = ''
    result = shell.read()
    lines = result.split("\n")

    # Only keep the string after ":" (the right part)
    infos = []

    for l in lines:
        if ":" in l:
            infos.append(l.split(":", 1)[1].strip())

    res = {
        "Computer": infos[0],
        "OS": infos[1],
        "Architecture": infos[2],
        "System language": infos[3],
        "Domain": infos[4],
        "Logged On Users": infos[5],
        "Meterpreter": infos[6]
        }

    return res


