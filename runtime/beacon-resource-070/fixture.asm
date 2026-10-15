; SPDX-License-Identifier: GPL-3.0-or-later
; Disposable ABI drivers. No game image or native code loaded.
.code
EXTERN producer_preview_bridge:PROC
EXTERN row_fast_bridge:PROC
EXTERN row_grow_bridge:PROC
PUBLIC invoke_preview
PUBLIC invoke_fast
PUBLIC invoke_grow
invoke_preview PROC FRAME
 push rbx
 .pushreg rbx
 sub rsp,20h
 .allocstack 20h
 .endprolog
 mov rbx,[rsp+50h]
 call producer_preview_bridge
 add rsp,20h
 pop rbx
 ret
invoke_preview ENDP
invoke_fast PROC FRAME
 push rdi
 .pushreg rdi
 push rsi
 .pushreg rsi
 sub rsp,28h
 .allocstack 28h
 .endprolog
 mov rdi,[rsp+60h]
 mov rsi,[rsp+68h]
 call row_fast_bridge
 add rsp,28h
 pop rsi
 pop rdi
 ret
invoke_fast ENDP
invoke_grow PROC FRAME
 push rdi
 .pushreg rdi
 push rsi
 .pushreg rsi
 sub rsp,28h
 .allocstack 28h
 .endprolog
 mov rdi,[rsp+60h]
 mov rsi,[rsp+68h]
 call row_grow_bridge
 add rsp,28h
 pop rsi
 pop rdi
 ret
invoke_grow ENDP
END
