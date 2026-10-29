; SPDX-License-Identifier: GPL-3.0-or-later
; Inline branch witness. Preserve all volatile GPRs, XMM0..5 and flags.
; Provider working RSP is 16-byte aligned; no original instructions relocate.
EXTERN visited_capture:PROC
EXTERN visited_fall:QWORD
EXTERN visited_taken:QWORD
.code
visited_bridge PROC
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
 lea rcx,[rsp+192]
 mov rdx,r13
 mov r8,rsi
 call visited_capture
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
 test sil,sil
 jnz taken
 jmp QWORD PTR [visited_fall]
taken:
 jmp QWORD PTR [visited_taken]
visited_bridge ENDP
END
