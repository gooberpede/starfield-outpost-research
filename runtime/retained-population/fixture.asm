; SPDX-License-Identifier: GPL-3.0-or-later
EXTERN fixture_driver:PROC
EXTERN fixture_grid:QWORD
EXTERN native_lookup:PROC
EXTERN native_query:PROC
EXTERN native_generate:PROC
EXTERN native_mask:PROC
EXTERN native_copy:PROC
.code
fixture_provider PROC FRAME
 push rsi
 .pushreg rsi
 push r13
 .pushreg r13
 sub rsp,3f8h
 .allocstack 3f8h
 .endprolog
 mov [rsp+38h],rcx
 mov [rsp+3d0h],rdx
 mov [rsp+3d8h],r8
 mov rax,fixture_grid
 mov [rsp+100h],rax
 mov r13,rdx
 mov rsi,r9
PUBLIC at_visited
at_visited::
 test sil,sil
 jnz NEAR PTR bypass
PUBLIC after_visited
after_visited::
 mov rcx,rsp
 mov rdx,r13
 call fixture_driver
 jmp finish
PUBLIC bypass
bypass::
 mov eax,1
finish:
 add rsp,3f8h
 pop r13
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
stub invoke_query,at_query,native_query
stub invoke_mask,at_mask,native_mask
stub invoke_copy,at_copy,native_copy
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
fence MACRO name
name PROC
 mov [rsp+10h],rbx
 mov rax,rcx
 ret
name ENDP
ENDM
fence fixture_reset
fence fixture_destroy
fixture_erase PROC
 db 40h,53h
 push rsi
 push rdi
 sub rsp,30h
 mov rax,rcx
 add rsp,30h
 pop rdi
 pop rsi
 pop rbx
 ret
fixture_erase ENDP
fence fixture_clear
fence fixture_retire
END
