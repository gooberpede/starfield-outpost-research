; SPDX-License-Identifier: GPL-3.0-or-later
; Complete CALL replacements, no entry detour. Native functions take integer
; channels only; all nonvolatile registers preserved by the normal Win64 ABI.
; These exact RBP offsets apply ONLY to pinned17DEC70 at its two CALLs.
.code
EXTERN travel_producer_hook:PROC
EXTERN travel_command_hook:PROC
PUBLIC travel_producer_bridge
PUBLIC travel_command_bridge
OBSERVE MACRO hook
 sub rsp,0b8h
 .allocstack 0b8h
 .endprolog
 lea rax,[rsp+30h]
 mov [rsp+20h],rax
 mov rax,[rbp+68h]
 mov [rsp+30h],rax
 mov [rsp+38h],rbp
 movzx eax,r14b
 mov [rsp+40h],rax
 mov [rsp+48h],rbx
 mov [rsp+50h],r13
 mov [rsp+58h],rsi
 mov [rsp+60h],r15
 mov [rsp+68h],r12
 movzx eax,BYTE PTR [rbp+90h]
 mov [rsp+70h],rax
 mov eax,[rbp+98h]
 mov [rsp+78h],rax
 ; original caller RSP is entry RSP+8, then +40h local.
 mov rax,[rsp+100h]
 mov [rsp+80h],rax
 mov rax,[rsp+0b8h]
 mov [rsp+88h],rax
 call hook
 add rsp,0b8h
 ret
ENDM
travel_producer_bridge PROC FRAME
 OBSERVE travel_producer_hook
travel_producer_bridge ENDP
travel_command_bridge PROC FRAME
 OBSERVE travel_command_hook
travel_command_bridge ENDP
END
