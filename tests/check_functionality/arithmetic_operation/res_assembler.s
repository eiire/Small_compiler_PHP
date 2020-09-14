.intel_syntax noprefix
.global main
.LC0:
.string "%d\n"
main:
push rbp
mov rbp, rsp
mov DWORD PTR [rbp-4], 10 
mov DWORD PTR [rbp-8], 20 
mov edx, DWORD PTR [rbp-4]
mov eax, DWORD PTR [rbp-8]
sub edx, eax
mov DWORD PTR [rbp-12], edx
mov eax, DWORD PTR [rbp-12]
mov esi, eax
mov edi, OFFSET FLAT:.LC0
mov eax, 0
call printf
mov eax, 0
mov DWORD PTR [rbp-16], 10 
mov DWORD PTR [rbp-8], 40 
mov edx, DWORD PTR [rbp-16]
mov eax, DWORD PTR [rbp-8]
add edx, eax
mov DWORD PTR [rbp-20], edx
mov eax, DWORD PTR [rbp-20]
mov esi, eax
mov edi, OFFSET FLAT:.LC0
mov eax, 0
call printf
mov eax, 0
mov DWORD PTR [rbp-4], 10 
mov DWORD PTR [rbp-8], 2 
mov eax, DWORD PTR [rbp-4]
cdq
idiv DWORD PTR [rbp-8]
mov DWORD PTR [rbp-12], eax
mov eax, DWORD PTR [rbp-12]
mov esi, eax
mov edi, OFFSET FLAT:.LC0
mov eax, 0
call printf
mov eax, 0
mov DWORD PTR [rbp-4], 10 
mov DWORD PTR [rbp-8], 20 
mov eax, DWORD PTR [rbp-4]
cdq
idiv DWORD PTR [rbp-8]
mov DWORD PTR [rbp-12], edx
mov eax, DWORD PTR [rbp-12]
mov esi, eax
mov edi, OFFSET FLAT:.LC0
mov eax, 0
call printf
mov eax, 0
mov DWORD PTR [rbp-4], 10 
mov DWORD PTR [rbp-8], 20 
mov edx, DWORD PTR [rbp-4]
mov eax, DWORD PTR [rbp-8]
imul edx, eax
mov DWORD PTR [rbp-12], edx
mov eax, DWORD PTR [rbp-12]
mov esi, eax
mov edi, OFFSET FLAT:.LC0
mov eax, 0
call printf
mov eax, 0
nop
pop     rbp 
ret
