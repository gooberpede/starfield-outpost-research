; SPDX-License-Identifier: GPL-3.0-or-later
; Independent caller and deliberately clobbering callback for the exact candidate
; object. It changes only this disposable executable's registers and memory.
option casemap:none
EXTERN d5ai_area_complete:PROC
EXTERN d5ai_area_preunlock:PROC
.code
d5ai_clobber PROC
 mov rax,1
 mov rcx,2
 mov rdx,3
 mov r8,4
 mov r9,5
 mov r10,6
 mov r11,7
 pxor xmm0,xmm0
 pxor xmm1,xmm1
 pxor xmm2,xmm2
 pxor xmm3,xmm3
 pxor xmm4,xmm4
 pxor xmm5,xmm5
 clc
 ret
d5ai_clobber ENDP
probe MACRO name,target
name PROC FRAME
 push rbp
 .pushreg rbp
 push rbx
 .pushreg rbx
 push rsi
 .pushreg rsi
 push rdi
 .pushreg rdi
 push r12
 .pushreg r12
 push r13
 .pushreg r13
 push r14
 .pushreg r14
 push r15
 .pushreg r15
 sub rsp,188h
 .allocstack 188h
 mov rbp,rsp
 .setframe rbp,0
 .endprolog
 mov r15,rcx
 mov [r15+224],rbp
 mov [r15+232],rsp
 mov QWORD PTR [rsp+70h],7777h
 mov rax,101h
 mov rcx,102h
 mov rdx,103h
 mov r8,108h
 mov r9,109h
 mov r10,110h
 mov r11,111h
 mov rbx,7000h
 mov rsi,6161h
 mov rdi,9090h
 mov r12,1212h
 mov r13,1313h
 mov r14,1414h
 pcmpeqd xmm0,xmm0
 pcmpeqd xmm1,xmm1
 pcmpeqd xmm2,xmm2
 pcmpeqd xmm3,xmm3
 pcmpeqd xmm4,xmm4
 pcmpeqd xmm5,xmm5
 stc
 call target
 mov [r15],rax
 mov [r15+8],rcx
 mov [r15+16],rdx
 mov [r15+24],r8
 mov [r15+32],r9
 mov [r15+40],r10
 mov [r15+48],r11
 mov [r15+56],rbx
 mov [r15+64],rdi
 mov [r15+72],r12
 mov [r15+80],r13
 mov [r15+88],r14
 mov [r15+96],r15
 mov [r15+104],rbp
 pushfq
 pop rax
 mov [r15+112],rax
 movdqu [r15+128],xmm0
 movdqu [r15+144],xmm1
 movdqu [r15+160],xmm2
 movdqu [r15+176],xmm3
 movdqu [r15+192],xmm4
 movdqu [r15+208],xmm5
 mov [r15+240],rsp
 mov [r15+248],rsi
 lea rsp,[rbp+188h]
 pop r15
 pop r14
 pop r13
 pop r12
 pop rdi
 pop rsi
 pop rbx
 pop rbp
 ret
name ENDP
ENDM
probe d5ai_probe_complete,d5ai_area_complete
probe d5ai_probe_preunlock,d5ai_area_preunlock
END
