.intel_syntax noprefix
.global main
.LC0:
.string "%d\n"
main:
push rbp
mov rbp, rsp
mov DWORD PTR [rbp-4], 35 
mov DWORD PTR [rbp-8], 49 
.L1:
mov edx, DWORD PTR[rbp-4]
mov eax, 0
cmp edx, eax
je .L2
mov edx, DWORD PTR[rbp-8]
mov eax, 0
cmp edx, eax
jne .L3
jmp .L2
.L3:
mov edx, DWORD PTR[rbp-4]
mov eax, DWORD PTR[rbp-8]
cmp edx, eax
jle .L4
mov eax, DWORD PTR [rbp-4]
cdq
idiv DWORD PTR [rbp-8]
mov DWORD PTR [rbp-4], edx
.L4:
mov edx, DWORD PTR[rbp-4]
mov eax, 0
cmp edx, eax
jne .L5
jmp .L2
.L5:
mov edx, DWORD PTR[rbp-4]
mov eax, DWORD PTR[rbp-8]
cmp edx, eax
jge .L6
mov eax, DWORD PTR [rbp-8]
cdq
idiv DWORD PTR [rbp-4]
mov DWORD PTR [rbp-8], edx
.L6:
jmp .L1
.L2:
mov edx, DWORD PTR [rbp-4]
mov eax, DWORD PTR [rbp-8]
add eax, edx
mov DWORD PTR [rbp-16], eax
mov eax, DWORD PTR [rbp-16]
mov esi, eax
mov edi, OFFSET FLAT:.LC0
mov eax, 0
call printf
mov eax, 0
nop
pop     rbp 
ret
