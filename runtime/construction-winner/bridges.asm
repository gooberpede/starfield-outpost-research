; SPDX-License-Identifier: GPL-3.0-or-later
; Adapted from owned R1 visited bridge. Upper YMM lanes are not live at the
; checked provider and constructor sites. Later miss allocation uses YMM0 then VZEROUPPER before the
; next selected-source iteration. General vector/unwind compatibility is unproven.
EXTERN visited_capture:PROC
EXTERN selected_capture:PROC
EXTERN birth_capture:PROC
EXTERN published_capture:PROC
EXTERN stored_capture:PROC
EXTERN birth_fall:QWORD
EXTERN published_fall:QWORD
EXTERN stored_fall:QWORD
EXTERN visited_fall:QWORD
EXTERN visited_taken:QWORD
EXTERN selected_fall:QWORD
.code
save MACRO
 pushfq
 push rax
 push rcx
 push rdx
 push r8
 push r9
 push r10
 push r11
 sub rsp,128
 movdqu [rsp+32],xmm0
 movdqu [rsp+48],xmm1
 movdqu [rsp+64],xmm2
 movdqu [rsp+80],xmm3
 movdqu [rsp+96],xmm4
 movdqu [rsp+112],xmm5
ENDM
restore MACRO
 movdqu xmm0,[rsp+32]
 movdqu xmm1,[rsp+48]
 movdqu xmm2,[rsp+64]
 movdqu xmm3,[rsp+80]
 movdqu xmm4,[rsp+96]
 movdqu xmm5,[rsp+112]
 add rsp,128
 pop r11
 pop r10
 pop r9
 pop r8
 pop rdx
 pop rcx
 pop rax
 popfq
ENDM
selected_bridge PROC
 mov rdx,[rdx]
 mov [rsp+38h],rdx
 save
 mov r8,rdx
 lea rcx,[rsp+192]
 mov rdx,r13
 call selected_capture
 restore
 jmp QWORD PTR [selected_fall]
selected_bridge ENDP
visited_bridge PROC
 save
 lea rcx,[rsp+192]
 mov rdx,r13
 mov r8,rsi
 mov r9,rdi
 call visited_capture
 restore
 test sil,sil
 jnz taken
 jmp QWORD PTR [visited_fall]
taken:
 jmp QWORD PTR [visited_taken]
visited_bridge ENDP
birth_bridge PROC
 save
 mov rcx,r14
 lea rdx,[r12-10h]
 mov r8,rdi
 call birth_capture
 restore
 lea rcx,[r14+70h]
 lea rdx,[rsp+90h]
 jmp QWORD PTR [birth_fall]
birth_bridge ENDP
published_bridge PROC
 mov ecx,eax
 mov rax,[r12+8]
 mov [rax+rcx*8],r14
 save
 mov r9,rcx
 lea r8,[rax+rcx*8]
 mov rcx,r14
 lea rdx,[r12-10h]
 call published_capture
 restore
 jmp QWORD PTR [published_fall]
published_bridge ENDP
stored_bridge PROC
 mov ecx,eax
 mov rax,[r12+8]
 mov [rax+rcx*8],rdi
 save
 mov r9,rdi
 lea r8,[rax+rcx*8]
 mov rdx,r13
 lea rcx,[rsp+192]
 call stored_capture
 restore
 jmp QWORD PTR [stored_fall]
stored_bridge ENDP
END
