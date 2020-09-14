.intel_syntax noprefix
.global main
.LC0:
.string "%d\n"
main:
push rbp
mov rbp, rsp
mov DWORD PTR [rbp-4], 10 
mov DWORD PTR [rbp-8], 20 
.L1:
mov edx, DWORD PTR[rbp-4]
mov eax, DWORD PTR[rbp-8]
cmp edx, eax
jge .L2
mov edx, DWORD PTR [rbp-8]
mov eax, 1
sub edx, eax
mov DWORD PTR [rbp-8], edx
mov edx, DWORD PTR[rbp-8]
mov eax, 15
cmp edx, eax
jne .L3
jmp .L2
.L3:
jmp .L1
.L2:
mov eax, DWORD PTR [rbp-8]
mov esi, eax
mov edi, OFFSET FLAT:.LC0
mov eax, 0
call printf
mov eax, 0
nop
pop     rbp 
ret
