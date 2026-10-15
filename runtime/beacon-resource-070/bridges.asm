; SPDX-License-Identifier: GPL-3.0-or-later
; Row CALLs have integer ABI. Preserve their RDI resource and RSI payload as
; explicit additional observer arguments; original four channels are forwarded.
.code
EXTERN row_fast:PROC
EXTERN row_grow:PROC
EXTERN preview_producer:PROC
PUBLIC row_fast_bridge
PUBLIC row_grow_bridge
PUBLIC producer_preview_bridge
producer_preview_bridge PROC FRAME
 sub rsp,38h
 .allocstack 38h
 .endprolog
 mov [rsp+20h],rbx
 call preview_producer
 add rsp,38h
 ret
producer_preview_bridge ENDP
row_fast_bridge PROC FRAME
 sub rsp,38h
 .allocstack 38h
 .endprolog
 mov [rsp+20h],rdi
 mov [rsp+28h],rsi
 call row_fast
 add rsp,38h
 ret
row_fast_bridge ENDP
row_grow_bridge PROC FRAME
 sub rsp,38h
 .allocstack 38h
 .endprolog
 mov [rsp+20h],rdi
 mov [rsp+28h],rsi
 call row_grow
 add rsp,38h
 ret
row_grow_bridge ENDP
END
