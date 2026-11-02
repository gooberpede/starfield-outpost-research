; SPDX-License-Identifier: GPL-3.0-or-later
; Native host entries with the exact five displaced original instructions.
; Bodies deliberately supply owned context state rather than execute retail.
option casemap:none
EXTERN d5ai_native_owner:PROC
EXTERN d5ai_native_context_reset:PROC
EXTERN d5ai_native_life_holder:PROC
EXTERN d5ai_native_life_collection:PROC
EXTERN d5ai_native_life_mutation:PROC
.code
d5ai_fixture_owner PROC FRAME
 mov [rsp+8],rbx
 .savereg rbx,8
 .endprolog
 jmp d5ai_native_owner
d5ai_fixture_owner ENDP
db 64 dup (90h)
d5ai_fixture_context_reset PROC FRAME
 db 40h
 push rbx
 .pushreg rbx
 push rbp
 .pushreg rbp
 push rsi
 .pushreg rsi
 push rdi
 .pushreg rdi
 .endprolog
 pop rdi
 pop rsi
 pop rbp
 pop rbx
 jmp d5ai_native_context_reset
d5ai_fixture_context_reset ENDP
db 64 dup (90h)
d5ai_fixture_life_holder PROC FRAME
 mov [rsp+8],rbx
 .savereg rbx,8
 .endprolog
 jmp d5ai_native_life_holder
d5ai_fixture_life_holder ENDP
db 64 dup (90h)
d5ai_fixture_life_collection PROC FRAME
 mov [rsp+8],rbx
 .savereg rbx,8
 .endprolog
 jmp d5ai_native_life_collection
d5ai_fixture_life_collection ENDP
db 64 dup (90h)
d5ai_fixture_life_mutation PROC FRAME
 mov [rsp+16],rbx
 .savereg rbx,16
 .endprolog
 jmp d5ai_native_life_mutation
d5ai_fixture_life_mutation ENDP
db 64 dup (90h)
END
