; SPDX-License-Identifier: GPL-3.0-or-later
; Disposable native entry shapes; no game instructions beyond the guarded sites.
EXTERN fixture_cursor:PROC
EXTERN fixture_driver:PROC
EXTERN native_lookup:PROC
EXTERN native_descriptor:PROC
EXTERN native_normalizer:PROC
EXTERN native_generate:PROC
EXTERN native_sample:PROC
EXTERN native_cold:PROC
EXTERN native_reserve:PROC
EXTERN fixture_bridge_check:PROC
EXTERN fixture_after_token:PROC
EXTERN fixture_publication_decision:PROC
seed MACRO
 mov rax,0101010101010101h
 movq xmm0,rax
 punpcklqdq xmm0,xmm0
 mov rax,0202020202020202h
 movq xmm1,rax
 punpcklqdq xmm1,xmm1
 mov rax,0303030303030303h
 movq xmm2,rax
 punpcklqdq xmm2,xmm2
 mov rax,0404040404040404h
 movq xmm3,rax
 punpcklqdq xmm3,xmm3
 mov rax,0505050505050505h
 movq xmm4,rax
 punpcklqdq xmm4,xmm4
 mov rax,0606060606060606h
 movq xmm5,rax
 punpcklqdq xmm5,xmm5
 xor eax,eax
 mov rax,01111111111111111h
 mov rcx,02222222222222222h
 mov r8,03333333333333333h
 mov r9,04444444444444444h
 mov r10,05555555555555555h
 mov r11,06666666666666666h
ENDM
capture MACRO phase
 mov [rsp+80h],rax
 mov [rsp+88h],rcx
 mov [rsp+90h],r8
 mov [rsp+98h],r9
 mov [rsp+0a0h],r10
 mov [rsp+0a8h],r11
 mov [rsp+0b0h],rdx
 pushfq
 pop rax
 mov [rsp+0b8h],rax
 movdqu [rsp+0c0h],xmm0
 movdqu [rsp+0d0h],xmm1
 movdqu [rsp+0e0h],xmm2
 movdqu [rsp+0f0h],xmm3
 movdqu [rsp+100h],xmm4
 movdqu [rsp+110h],xmm5
 lea rcx,[rsp+80h]
 mov edx,phase
 call fixture_bridge_check
ENDM
.code
fixture_provider PROC FRAME
 mov rax,rsp
 mov [rax+18h],r8
 mov [rax+10h],rdx
 mov [rax+8],rcx
 push rsi
 .pushreg rsi
 push rdi
 .pushreg rdi
 push r12
 .pushreg r12
 push r13
 .pushreg r13
 sub rsp,3d8h
 .allocstack 3d8h
 .endprolog
 mov r13,rcx
 lea r12,[rcx+48h]
 mov rsi,r9
next_source:
 call fixture_cursor
 test rax,rax
 jz finish
 mov rdx,rax
 seed
PUBLIC at_selected
at_selected::
 mov rdx,[rdx]
 mov [rsp+38h],rdx
 capture 0
 ; A selection with no BIOM intentionally stops before visited.
 cmp rsi,2
 je finish
 mov rdx,[rsp+38h]
 seed
 ; The bad-source control tests observer refusal, not an engine dereference.
 cmp rdx,10000h
 jb substituted_token
 mov rdi,[rdx+68h]
 jmp token_ready
substituted_token:
 xor edi,edi
token_ready:
 mov rcx,[rsp+38h]
 call fixture_after_token
 mov rdx,[rsp+38h]
 seed
PUBLIC at_visited
at_visited::
 test sil,sil
 jnz NEAR PTR bypass_check
 capture 1
 mov rcx,rsp
 mov rdx,r13
 call fixture_driver
 cmp eax,-1
 je next_source
PUBLIC at_stored
at_stored::
 mov ecx,eax
 mov rax,[r12+8]
 mov [rax+rcx*8],rdi
 jmp next_source
bypass_check:
 capture 1
finish:
 mov eax,12345h
 add rsp,3d8h
 pop r13
 pop r12
 pop rdi
 pop rsi
 ret
fixture_provider ENDP
stub MACRO name,site,callee
name PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
PUBLIC site
site::
 call callee
 add rsp,28h
 ret
name ENDP
ENDM
stub invoke_lookup,at_lookup,native_lookup
stub invoke_descriptor,at_descriptor,native_descriptor
stub invoke_normalizer,at_normalizer,native_normalizer
stub invoke_sample,at_sample,native_sample
stub invoke_cold,at_cold,native_cold
stub invoke_reserve,at_reserve,native_reserve
invoke_generate PROC FRAME
 sub rsp,38h
 .allocstack 38h
 .endprolog
 mov rax,[rsp+60h]
 mov [rsp+20h],rax
 mov rax,[rsp+68h]
 mov [rsp+28h],rax
PUBLIC at_generate
at_generate::
 call native_generate
 add rsp,38h
 ret
invoke_generate ENDP
EXTERN reset_body:PROC
fixture_reset PROC FRAME
 mov [rsp+10h],rbx
 push rbx
 .pushreg rbx
 sub rsp,20h
 .allocstack 20h
 .endprolog
 call reset_body
 add rsp,20h
 pop rbx
 ret
fixture_reset ENDP
fence MACRO name
name PROC
 mov [rsp+10h],rbx
 mov rax,rcx
 ret
name ENDP
ENDM
fence fixture_destroy
fixture_erase PROC FRAME
 db 40h,53h
 .pushreg rbx
 push rsi
 .pushreg rsi
 push rdi
 .pushreg rdi
 sub rsp,30h
 .allocstack 30h
 .endprolog
 mov rax,rcx
 add rsp,30h
 pop rdi
 pop rsi
 pop rbx
 ret
fixture_erase ENDP
fence fixture_clear
fence fixture_retire
fixture_birth PROC FRAME
 push rdi
 .pushreg rdi
 push r12
 .pushreg r12
 push r14
 .pushreg r14
 sub rsp,0b0h
 .allocstack 0b0h
 .endprolog
 mov r14,rcx
 lea r12,[rdx+10h]
 mov rdi,r8
 mov [rsp+80h],r9
PUBLIC at_birth
at_birth::
 lea rcx,[r14+70h]
 lea rdx,[rsp+90h]
 ; Controlled host outcomes; the actual constructor cleanup is proved separately.
 mov rcx,[rsp+80h]
 call fixture_publication_decision
 test eax,eax
 jnz unpublished
 ; Fixture publication has one preallocated cell. EAX is the native index.
 xor eax,eax
PUBLIC at_published
at_published::
 mov ecx,eax
 mov rax,[r12+8]
 mov [rax+rcx*8],r14
unpublished:
 add rsp,0b0h
 pop r14
 pop r12
 pop rdi
 ret
fixture_birth ENDP
END
