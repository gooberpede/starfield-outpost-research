; SPDX-License-Identifier: GPL-3.0-or-later
; CALL-entered area-reader wrapper. R13/R14 and XMM6/XMM7 are live native
; nonvolatile query/consumer/radius/upper operands at the pinned acquire site.
option casemap:none
EXTERN d5ai_acquire_original:QWORD
EXTERN d5ai_area_capture:PROC
EXTERN d5ai_native_acquire:PROC
EXTERN d5ai_complete_capture:PROC
EXTERN d5ai_preunlock_capture:PROC
PUBLIC d5ai_at_preunlock
PUBLIC d5ai_at_acquire
PUBLIC d5ai_at_complete
.code
d5ai_area_acquire PROC FRAME
 push rbp
 .pushreg rbp
 sub rsp,50h
 .allocstack 50h
 lea rbp,[rsp+50h]
 .setframe rbp,50h
 .endprolog
 mov [rsp+30h],rcx
 call qword ptr [d5ai_acquire_original]
 mov [rsp+38h],rax
 mov rcx,[rsp+30h]
 sub rcx,40h
 mov rdx,r13
 mov r8,r14
 movd r9d,xmm7
 movd eax,xmm6
 mov [rsp+20h],eax
 call d5ai_area_capture
 mov rax,[rsp+38h]
 lea rsp,[rbp]
 pop rbp
 ret
d5ai_area_acquire ENDP
d5ai_area_complete PROC FRAME
 push rbp
 .pushreg rbp
 pushfq
 .allocstack 8
 push rax
 .allocstack 8
 push rcx
 .allocstack 8
 push rdx
 .allocstack 8
 push r8
 .allocstack 8
 push r9
 .allocstack 8
 push r10
 .allocstack 8
 push r11
 .allocstack 8
 sub rsp,128
 .allocstack 128
 mov rbp,rsp
 .setframe rbp,0
 .endprolog
 movdqu [rsp+32],xmm0
 movdqu [rsp+48],xmm1
 movdqu [rsp+64],xmm2
 movdqu [rsp+80],xmm3
 movdqu [rsp+96],xmm4
 movdqu [rsp+112],xmm5
 mov rcx,rdi
 mov rdx,r12
 mov r8d,[rsp+160]
 call d5ai_complete_capture
 movdqu xmm0,[rsp+32]
 movdqu xmm1,[rsp+48]
 movdqu xmm2,[rsp+64]
 movdqu xmm3,[rsp+80]
 movdqu xmm4,[rsp+96]
 movdqu xmm5,[rsp+112]
 push QWORD PTR [rsp+184]
 popfq
 mov r11,[rsp+128]
 mov r10,[rsp+136]
 mov r9,[rsp+144]
 mov r8,[rsp+152]
 mov rdx,[rsp+160]
 mov rcx,[rsp+168]
 mov rax,[rsp+176]
 mov rdi,[rbp+320]
 lea rsp,[rbp+192]
 pop rbp
 ret
d5ai_area_complete ENDP
d5ai_area_preunlock PROC FRAME
 push rbp
 .pushreg rbp
 pushfq
 .allocstack 8
 push rax
 .allocstack 8
 push rcx
 .allocstack 8
 push rdx
 .allocstack 8
 push r8
 .allocstack 8
 push r9
 .allocstack 8
 push r10
 .allocstack 8
 push r11
 .allocstack 8
 sub rsp,128
 .allocstack 128
 mov rbp,rsp
 .setframe rbp,0
 .endprolog
 movdqu [rsp+32],xmm0
 movdqu [rsp+48],xmm1
 movdqu [rsp+64],xmm2
 movdqu [rsp+80],xmm3
 movdqu [rsp+96],xmm4
 movdqu [rsp+112],xmm5
 mov ecx,[rsp+160]
 call d5ai_preunlock_capture
 movdqu xmm0,[rsp+32]
 movdqu xmm1,[rsp+48]
 movdqu xmm2,[rsp+64]
 movdqu xmm3,[rsp+80]
 movdqu xmm4,[rsp+96]
 movdqu xmm5,[rsp+112]
 push QWORD PTR [rsp+184]
 popfq
 mov r11,[rsp+128]
 mov r10,[rsp+136]
 mov r9,[rsp+144]
 mov r8,[rsp+152]
 mov rdx,[rsp+160]
 mov rcx,[rsp+168]
 mov rax,[rsp+176]
 lea rcx,[rbx+4]
 mov edx,-1
 lea rsp,[rbp+192]
 pop rbp
 ret
d5ai_area_preunlock ENDP
d5ai_invoke PROC FRAME
 push rbp
 .pushreg rbp
 push r13
 .pushreg r13
 push r14
 .pushreg r14
 sub rsp,60h
 .allocstack 60h
 movdqu [rsp+30h],xmm6
 .savexmm128 xmm6,30h
 movdqu [rsp+40h],xmm7
 .savexmm128 xmm7,40h
 .endprolog
 mov r13,rdx
 mov r14,r8
 movd xmm7,r9d
 mov eax,[rsp+0A0h]
 movd xmm6,eax
d5ai_at_acquire LABEL BYTE
 call d5ai_native_acquire
 movdqu xmm6,[rsp+30h]
 movdqu xmm7,[rsp+40h]
 add rsp,60h
 pop r14
 pop r13
 pop rbp
 ret
d5ai_invoke ENDP
d5ai_complete_invoke PROC FRAME
 push rdi
 .pushreg rdi
 push r12
 .pushreg r12
 sub rsp,88h
 .allocstack 88h
 .endprolog
 mov rdi,rcx
 mov r12,rdx
 mov edx,r8d
 mov QWORD PTR [rsp+70h],12345678h
d5ai_at_complete LABEL BYTE
 mov rdi,[rsp+70h]
 mov rax,rdi
 add rsp,88h
 pop r12
 pop rdi
 ret
d5ai_complete_invoke ENDP
d5ai_preunlock_invoke PROC FRAME
 push rbx
 .pushreg rbx
 sub rsp,20h
 .allocstack 20h
 .endprolog
 mov edx,ecx
 mov ebx,1000h
d5ai_at_preunlock LABEL BYTE
 lea rcx,[rbx+4]
 mov edx,-1
 mov eax,edx
 add rsp,20h
 pop rbx
 ret
d5ai_preunlock_invoke ENDP
END
