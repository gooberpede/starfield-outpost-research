; SPDX-License-Identifier: GPL-3.0-or-later
; Owned synthetic caller for the actual integrated production dispatch bridge.
; It supplies a private watched node/server and the native function-entry stack.
EXTERN D5AM_sched_dispatch:PROC
.code
PUBLIC D5AN_dispatch_fall
D5AN_dispatch_fall PROC
 ret
D5AN_dispatch_fall ENDP
PUBLIC D5AN_dispatch_node
D5AN_dispatch_node PROC FRAME
 sub rsp,40
 .allocstack 40
 .endprolog
 mov rax,rcx
 mov rcx,rdx
 mov rdx,rax
 call D5AM_sched_dispatch
 add rsp,40
 ret
D5AN_dispatch_node ENDP
END
