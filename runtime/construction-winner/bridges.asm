; SPDX-License-Identifier: GPL-3.0-or-later
; CALL-entered inline observers retain a real return PC in the original native
; frame. RBP anchors the bridge frame for Windows virtual unwind, including the
; temporary flags restore push. The epilogue preserves native flags.
; Upper YMM lanes are not live at the pinned provider/constructor sites; no
; general vector compatibility follows from preserving the six volatile XMMs.
EXTERN visited_capture:PROC
EXTERN selected_capture:PROC
EXTERN birth_capture:PROC
EXTERN published_capture:PROC
EXTERN stored_capture:PROC
.const
PUBLIC bridge_pc_table_begin
bridge_pc_table_begin LABEL QWORD
.code
; Each table entry labels an actual instruction boundary for independent
; RtlVirtualUnwind context controls. It adds no executed instruction.
pc MACRO
 LOCAL position
 .const
 DQ position
 .code
position:
ENDM
save MACRO
 pc
 push rbp
 .pushreg rbp
 pc
 pushfq
 .allocstack 8
 pc
 push rax
 .allocstack 8
 pc
 push rcx
 .allocstack 8
 pc
 push rdx
 .allocstack 8
 pc
 push r8
 .allocstack 8
 pc
 push r9
 .allocstack 8
 pc
 push r10
 .allocstack 8
 pc
 push r11
 .allocstack 8
 pc
 sub rsp,128
 .allocstack 128
 pc
 mov rbp,rsp
 .setframe rbp,0
 .endprolog
 pc
 movdqu [rsp+32],xmm0
 pc
 movdqu [rsp+48],xmm1
 pc
 movdqu [rsp+64],xmm2
 pc
 movdqu [rsp+80],xmm3
 pc
 movdqu [rsp+96],xmm4
 pc
 movdqu [rsp+112],xmm5
ENDM
restore MACRO
 pc
 movdqu xmm0,[rsp+32]
 pc
 movdqu xmm1,[rsp+48]
 pc
 movdqu xmm2,[rsp+64]
 pc
 movdqu xmm3,[rsp+80]
 pc
 movdqu xmm4,[rsp+96]
 pc
 movdqu xmm5,[rsp+112]
 pc
 push QWORD PTR [rsp+184]
 pc
 popfq
 pc
 mov r11,[rsp+128]
 pc
 mov r10,[rsp+136]
 pc
 mov r9,[rsp+144]
 pc
 mov r8,[rsp+152]
 pc
 mov rdx,[rsp+160]
 pc
 mov rcx,[rsp+168]
 pc
 mov rax,[rsp+176]
ENDM
finish MACRO
 pc
 lea rsp,[rbp+192]
 pc
 pop rbp
 pc
 ret
ENDM
selected_bridge PROC FRAME
 pc
 mov rdx,[rdx]
 pc
 mov [rsp+40h],rdx
 save
 pc
 mov r8,rdx
 pc
 lea rcx,[rbp+208]
 pc
 mov rdx,r13
 pc
 call selected_capture
 restore
 finish
selected_bridge ENDP
visited_bridge PROC FRAME
 save
 pc
 lea rcx,[rbp+208]
 pc
 mov rdx,r13
 pc
 mov r8,rsi
 pc
 mov r9,rdi
 pc
 call visited_capture
 pc
 test sil,sil
 pc
 jz visited_fallthrough
 pc
 jmp visited_restore
visited_fallthrough:
 ; The widened native site also displaced this ordinary stack-slot store.
 ; RBP here is the bridge anchor; its saved value is the native frame pointer.
 pc
 mov rax,[rbp+192]
 pc
 mov [rax+10h],rbx
visited_restore:
 restore
 pc
 test sil,sil
 finish
visited_bridge ENDP
birth_bridge PROC FRAME
 save
 pc
 mov rcx,r14
 pc
 lea rdx,[r12-10h]
 pc
 mov r8,rdi
 pc
 call birth_capture
 restore
 pc
 lea rcx,[r14+70h]
 pc
 lea rdx,[rbp+352]
 finish
birth_bridge ENDP
published_bridge PROC FRAME
 pc
 mov ecx,eax
 pc
 mov rax,[r12+8]
 pc
 mov [rax+rcx*8],r14
 save
 pc
 mov r9,rcx
 pc
 lea r8,[rax+rcx*8]
 pc
 mov rcx,r14
 pc
 lea rdx,[r12-10h]
 pc
 call published_capture
 restore
 finish
published_bridge ENDP
stored_bridge PROC FRAME
 pc
 mov ecx,eax
 pc
 mov rax,[r12+8]
 pc
 mov [rax+rcx*8],rdi
 save
 pc
 mov r9,rdi
 pc
 lea r8,[rax+rcx*8]
 pc
 mov rdx,r13
 pc
 lea rcx,[rbp+208]
 pc
 call stored_capture
 restore
 finish
stored_bridge ENDP
.const
PUBLIC bridge_pc_table_end
bridge_pc_table_end LABEL QWORD
END
