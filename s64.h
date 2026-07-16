#include <stdint.h>
#include <stdio.h>
#include <inttypes.h>

// #define __S64_LANGUAGE__(size, address) (*(uint32_t*)(uintptr_t)(address) = (uint32_t)(size))

/*
    library ini lahir karena 1 hal, yaitu kesulitan dalam membuat bahasa.
    awalnya ini adalah sebuah bahasa bernama S64 dengan structure [nama variable] [memory allocation] [memory location].
    tapi karena menurut saya terlalu sulit, jadi saya turunkan menjadi string manipulation aja.
    tapi karena masih sulit menurut saya, akhir saya jadikan ada library, tapi tanpa menghilangkan fungsi utama nya.
    fungsi utama nya yaitu memory mapping.
*/

/*
    fungsi :
        __S64_LANGUAGE__() : mencetak memory size ke memory location
        __translation__() : mencetak memory size dan memory location di file .s (assembly)
*/

int __translation__(uint32_t size, uintptr_t address, const char *filename) {
    FILE *file = fopen(filename, "w");
    if(!file) return 1;

    // executable header
    fprintf(file, "section .text\n");
    fprintf(file, "    global _start\n");

    // program
    fprintf(file, "_start:\n");
    fprintf(file, "    mov dword [0x%" PRIXPTR "], %" PRIu32 "\n", address, size);

    // close/exit
    fprintf(file, "    mov eax, 60\n");
    fprintf(file, "    xor edi, edi\n");
    fprintf(file, "    syscall\n");

    fclose(file);
    return 0;
}