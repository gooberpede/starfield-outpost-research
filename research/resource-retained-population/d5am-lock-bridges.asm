; SPDX-License-Identifier: GPL-3.0-or-later
; Source-informed adaptation of the owned bridges.asm save/restore method.
; Original native atomic executes exactly once before capture. These bridges
; are for private native-copy qualification only; there is no retail installer.
EXTERN D5AM_collect:PROC
.code
save_state MACRO
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
ENDM
restore_state MACRO
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
 lea rsp,[rbp+192]
 pop rbp
 ret
ENDM
PUBLIC D5AM_pending_bridge
D5AM_pending_bridge PROC FRAME
 lock xadd DWORD PTR [r14+4],eax
 save_state
 mov rcx,r14
 mov edx,DWORD PTR [rsp+176]
 mov r8d,1
 call D5AM_collect
 restore_state
D5AM_pending_bridge ENDP
PUBLIC D5AM_acquired_bridge
D5AM_acquired_bridge PROC FRAME
 mov DWORD PTR [r14],ebp
 mfence
 save_state
 mov rcx,r14
 mov edx,DWORD PTR [rsp+176]
 mov r8d,2
 call D5AM_collect
 restore_state
D5AM_acquired_bridge ENDP
END
