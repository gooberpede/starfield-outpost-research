; SPDX-License-Identifier: GPL-3.0-or-later
; Four installed context bridges plus an offline point prototype. Adjacent
; flags-tail ranges describe the partially deallocated stack at POPFQ.
option casemap:none
EXTERN d5ar_callback_original:QWORD
EXTERN d5ar_capture_callback:PROC
EXTERN d5ar_area_callback_original:QWORD
EXTERN d5ar_capture_area_callback:PROC
EXTERN d5ar_area_dispatch:QWORD
EXTERN d5ar_area_entry:PROC
EXTERN d5ar_selection_release_original:QWORD
EXTERN d5ar_capture_selection:PROC
PUBLIC d5ar_selection_release_bridge
PUBLIC d5ar_selection_release_bridge_deallocate
PUBLIC d5ar_selection_release_bridge_flags
PUBLIC d5ar_callback_bridge
PUBLIC d5ar_callback_bridge_deallocate
PUBLIC d5ar_callback_bridge_flags
PUBLIC d5ar_area_callback_bridge
PUBLIC d5ar_area_callback_bridge_deallocate
PUBLIC d5ar_area_callback_bridge_flags
PUBLIC d5ar_area_entry_bridge
PUBLIC d5ar_area_entry_bridge_deallocate
PUBLIC d5ar_area_entry_bridge_flags
EXTERN d5ar_source_free_original:QWORD
EXTERN d5ar_capture_source_free:PROC
PUBLIC d5ar_source_free_bridge
PUBLIC d5ar_source_free_bridge_deallocate
PUBLIC d5ar_source_free_bridge_flags
.code
d5ar_callback_bridge PROC FRAME
 pushfq
 .allocstack 8
 sub rsp,0e0h
 .allocstack 0e0h
 .endprolog
 mov [rsp+30h],rcx
 mov [rsp+38h],rdx
 mov [rsp+40h],r8
 mov [rsp+48h],r9
 mov [rsp+50h],rax
 mov [rsp+58h],r10
 mov [rsp+60h],r11
 movdqu [rsp+70h],xmm0
 movdqu [rsp+80h],xmm1
 movdqu [rsp+90h],xmm2
 movdqu [rsp+0a0h],xmm3
 movdqu [rsp+0b0h],xmm4
 movdqu [rsp+0c0h],xmm5
 mov r8,rbp
 mov r9,[rsp+0e8h]
 call d5ar_capture_callback
 mov rcx,[rsp+30h]
 mov rdx,[rsp+38h]
 mov r8,[rsp+40h]
 mov r9,[rsp+48h]
 mov rax,[rsp+50h]
 mov r10,[rsp+58h]
 mov r11,[rsp+60h]
 movdqu xmm0,[rsp+70h]
 movdqu xmm1,[rsp+80h]
 movdqu xmm2,[rsp+90h]
 movdqu xmm3,[rsp+0a0h]
 movdqu xmm4,[rsp+0b0h]
 movdqu xmm5,[rsp+0c0h]
d5ar_callback_bridge_deallocate::
 add rsp,0e0h
d5ar_callback_bridge ENDP
d5ar_callback_bridge_flags PROC FRAME
 .allocstack 8
 .endprolog
 popfq
 jmp qword ptr [d5ar_callback_original]
d5ar_callback_bridge_flags ENDP
d5ar_area_callback_bridge PROC FRAME
 pushfq
 .allocstack 8
 sub rsp,0e0h
 .allocstack 0e0h
 .endprolog
 mov [rsp+30h],rcx
 mov [rsp+38h],rdx
 mov [rsp+40h],r8
 mov [rsp+48h],r9
 mov [rsp+50h],rax
 mov [rsp+58h],r10
 mov [rsp+60h],r11
 movdqu [rsp+70h],xmm0
 movdqu [rsp+80h],xmm1
 movdqu [rsp+90h],xmm2
 movdqu [rsp+0a0h],xmm3
 movdqu [rsp+0b0h],xmm4
 movdqu [rsp+0c0h],xmm5
 mov rdx,rcx
 mov rcx,r8
 mov r8,r15
 mov r9,[rsp+0e8h]
 call d5ar_capture_area_callback
 mov rcx,[rsp+30h]
 mov rdx,[rsp+38h]
 mov r8,[rsp+40h]
 mov r9,[rsp+48h]
 mov rax,[rsp+50h]
 mov r10,[rsp+58h]
 mov r11,[rsp+60h]
 movdqu xmm0,[rsp+70h]
 movdqu xmm1,[rsp+80h]
 movdqu xmm2,[rsp+90h]
 movdqu xmm3,[rsp+0a0h]
 movdqu xmm4,[rsp+0b0h]
 movdqu xmm5,[rsp+0c0h]
d5ar_area_callback_bridge_deallocate::
 add rsp,0e0h
d5ar_area_callback_bridge ENDP
d5ar_area_callback_bridge_flags PROC FRAME
 .allocstack 8
 .endprolog
 popfq
 jmp qword ptr [d5ar_area_callback_original]
d5ar_area_callback_bridge_flags ENDP
d5ar_area_entry_bridge PROC FRAME
 pushfq
 .allocstack 8
 sub rsp,0e0h
 .allocstack 0e0h
 .endprolog
 mov [rsp+30h],rcx
 mov [rsp+38h],rdx
 mov [rsp+40h],r8
 mov [rsp+48h],r9
 mov [rsp+50h],rax
 mov [rsp+58h],r10
 mov [rsp+60h],r11
 movdqu [rsp+70h],xmm0
 movdqu [rsp+80h],xmm1
 movdqu [rsp+90h],xmm2
 movdqu [rsp+0a0h],xmm3
 movdqu [rsp+0b0h],xmm4
 movdqu [rsp+0c0h],xmm5
 mov r8,r14
 mov r9,[rsp+0e8h]
 movd eax,xmm2
 mov [rsp+20h],eax
 movd eax,xmm3
 mov [rsp+28h],eax
 call d5ar_area_entry
 mov rcx,[rsp+30h]
 mov rdx,[rsp+38h]
 mov r8,[rsp+40h]
 mov r9,[rsp+48h]
 mov rax,[rsp+50h]
 mov r10,[rsp+58h]
 mov r11,[rsp+60h]
 movdqu xmm0,[rsp+70h]
 movdqu xmm1,[rsp+80h]
 movdqu xmm2,[rsp+90h]
 movdqu xmm3,[rsp+0a0h]
 movdqu xmm4,[rsp+0b0h]
 movdqu xmm5,[rsp+0c0h]
d5ar_area_entry_bridge_deallocate::
 add rsp,0e0h
d5ar_area_entry_bridge ENDP
d5ar_area_entry_bridge_flags PROC FRAME
 .allocstack 8
 .endprolog
 popfq
 jmp qword ptr [d5ar_area_dispatch]
d5ar_area_entry_bridge_flags ENDP
d5ar_selection_release_bridge PROC FRAME
 pushfq
 .allocstack 8
 sub rsp,0e0h
 .allocstack 0e0h
 .endprolog
 mov [rsp+30h],rcx
 mov [rsp+38h],rdx
 mov [rsp+40h],r8
 mov [rsp+48h],r9
 mov [rsp+50h],rax
 mov [rsp+58h],r10
 mov [rsp+60h],r11
 movdqu [rsp+70h],xmm0
 movdqu [rsp+80h],xmm1
 movdqu [rsp+90h],xmm2
 movdqu [rsp+0a0h],xmm3
 movdqu [rsp+0b0h],xmm4
 movdqu [rsp+0c0h],xmm5
 mov rdx,[rsp+0e8h]
 lea r8,[rsp+178h]
 lea r9,[rsp+0e8h]
 call d5ar_capture_selection
 mov rcx,[rsp+30h]
 mov rdx,[rsp+38h]
 mov r8,[rsp+40h]
 mov r9,[rsp+48h]
 mov rax,[rsp+50h]
 mov r10,[rsp+58h]
 mov r11,[rsp+60h]
 movdqu xmm0,[rsp+70h]
 movdqu xmm1,[rsp+80h]
 movdqu xmm2,[rsp+90h]
 movdqu xmm3,[rsp+0a0h]
 movdqu xmm4,[rsp+0b0h]
 movdqu xmm5,[rsp+0c0h]
d5ar_selection_release_bridge_deallocate::
 add rsp,0e0h
d5ar_selection_release_bridge ENDP
d5ar_selection_release_bridge_flags PROC FRAME
 .allocstack 8
 .endprolog
 popfq
 jmp qword ptr [d5ar_selection_release_original]
d5ar_selection_release_bridge_flags ENDP
d5ar_source_free_bridge PROC FRAME
 pushfq
 .allocstack 8
 sub rsp,0e0h
 .allocstack 0e0h
 .endprolog
 mov [rsp+30h],rcx
 mov [rsp+38h],rdx
 mov [rsp+40h],r8
 mov [rsp+48h],r9
 mov [rsp+50h],rax
 mov [rsp+58h],r10
 mov [rsp+60h],r11
 movdqu [rsp+70h],xmm0
 movdqu [rsp+80h],xmm1
 movdqu [rsp+90h],xmm2
 movdqu [rsp+0a0h],xmm3
 movdqu [rsp+0b0h],xmm4
 movdqu [rsp+0c0h],xmm5
 mov r8,[rsp+0e8h]
 lea r9,[rsp+0e8h]
 call d5ar_capture_source_free
 mov rcx,[rsp+30h]
 mov rdx,[rsp+38h]
 mov r8,[rsp+40h]
 mov r9,[rsp+48h]
 mov rax,[rsp+50h]
 mov r10,[rsp+58h]
 mov r11,[rsp+60h]
 movdqu xmm0,[rsp+70h]
 movdqu xmm1,[rsp+80h]
 movdqu xmm2,[rsp+90h]
 movdqu xmm3,[rsp+0a0h]
 movdqu xmm4,[rsp+0b0h]
 movdqu xmm5,[rsp+0c0h]
d5ar_source_free_bridge_deallocate::
 add rsp,0e0h
d5ar_source_free_bridge ENDP
d5ar_source_free_bridge_flags PROC FRAME
 .allocstack 8
 .endprolog
 popfq
 jmp qword ptr [d5ar_source_free_original]
d5ar_source_free_bridge_flags ENDP
END
