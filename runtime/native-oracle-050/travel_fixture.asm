; SPDX-License-Identifier: GPL-3.0-or-later
.code
EXTERN travel_producer_bridge:PROC
EXTERN travel_command_bridge:PROC
PUBLIC test_travel_producer
PUBLIC test_travel_command
FIXTURE MACRO bridge
 push rbp
 .pushreg rbp
 push rbx
 .pushreg rbx
 push rsi
 .pushreg rsi
 push r12
 .pushreg r12
 push r13
 .pushreg r13
 push r14
 .pushreg r14
 push r15
 .pushreg r15
 sub rsp,100h
 .allocstack 100h
 .endprolog
 mov r11,[rsp+160h]
 lea rbp,[rsp+50h]
 mov rax,[r11]
 mov [rbp+68h],rax
 mov r14,[r11+10h]
 mov rbx,[r11+18h]
 mov r13,[r11+20h]
 mov rsi,[r11+28h]
 mov r15,[r11+30h]
 mov r12,[r11+38h]
 mov rax,[r11+40h]
 mov [rbp+90h],al
 mov rax,[r11+48h]
 mov [rbp+98h],eax
 mov rax,[r11+50h]
 mov [rsp+40h],rax
 call bridge
 add rsp,100h
 pop r15
 pop r14
 pop r13
 pop r12
 pop rsi
 pop rbx
 pop rbp
 ret
ENDM
test_travel_producer PROC FRAME
 FIXTURE travel_producer_bridge
test_travel_producer ENDP
test_travel_command PROC FRAME
 FIXTURE travel_command_bridge
test_travel_command ENDP
PUBLIC travel_fp_mutate
travel_fp_mutate PROC
 fnclex
 fldcw WORD PTR [rcx]
 fld1
 fldz
 fdivp st(1),st(0)
 fstp st(0)
 ret
travel_fp_mutate ENDP
END
