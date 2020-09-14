.intel_syntax noprefix
.global main
.LC0:
.string "%d\n"
main:
push rbp
mov rbp, rsp
mov DWORD PTR [rbp-4], 35 
.L1:
mov edx, DWORD PTR[rbp-4]
mov eax, 4
cmp edx, eax
je .L2
mov edx, DWORD PTR [rbp-4]
mov eax, 1
sub edx, eax
mov DWORD PTR [rbp-4], edx
jmp .L1
.L2:
mov eax, DWORD PTR [rbp-4]
mov esi, eax
mov edi, OFFSET FLAT:.LC0
mov eax, 0
call printf
mov eax, 0
nop
pop     rbp 
ret
