; SPDX-License-Identifier: GPL-3.0-or-later
; Owned adverse ABI probe for the exact production callback bridges.
option casemap:none
EXTERN d5ar_callback_bridge:PROC
EXTERN d5ar_area_callback_bridge:PROC
EXTERN d5ar_area_entry_bridge:PROC
EXTERN d5ar_selection_release_bridge:PROC
EXTERN d5ar_source_free_bridge:PROC
EXTERN observed:BYTE
EXTERN observed_simd:BYTE
EXTERN captured_arguments:BYTE
EXTERN fixture_capture_c:PROC
PUBLIC probe_bridge
PUBLIC original_sink
PUBLIC d5ar_capture_callback
PUBLIC d5ar_capture_area_callback
PUBLIC d5ar_area_entry
PUBLIC d5ar_capture_selection
PUBLIC d5ar_capture_source_free
.const
pattern BYTE 11h,22h,33h,44h,55h,66h,77h,88h,99h,0aah,0bbh,0cch,0ddh,0eeh,0ffh,10h
.code
probe_bridge PROC FRAME
 push rbx
 .pushreg rbx
 push rbp
 .pushreg rbp
 push r15
 .pushreg r15
 push r14
 .pushreg r14
 sub rsp,48h
 .allocstack 48h
 .endprolog
 lea rax,d5ar_callback_bridge
 test ecx,ecx
 jz selected
 lea rax,d5ar_area_callback_bridge
 cmp ecx,1
 je selected
 lea rax,d5ar_area_entry_bridge
 cmp ecx,2
 je selected
 lea rax,d5ar_selection_release_bridge
 cmp ecx,3
 je selected
 lea rax,d5ar_source_free_bridge
selected:
 mov [rsp+38h],rax
 mov QWORD PTR [rsp+20h],0a5h
 mov rbp,8888h
 mov r15,9999h
 mov r14,0aaaah
 mov rcx,1111h
 mov rdx,2222h
 mov r8,3333h
 mov r9,4444h
 mov rax,5555h
 mov r10,6666h
 mov r11,7777h
 movdqu xmm0,XMMWORD PTR pattern
 movdqu xmm1,XMMWORD PTR pattern
 movdqu xmm2,XMMWORD PTR pattern
 movdqu xmm3,XMMWORD PTR pattern
 movdqu xmm4,XMMWORD PTR pattern
 movdqu xmm5,XMMWORD PTR pattern
 cmp rax,rax
 call QWORD PTR [rsp+38h]
 add rsp,48h
 pop r14
 pop r15
 pop rbp
 pop rbx
 ret
probe_bridge ENDP
original_sink PROC
 pushfq
 pop QWORD PTR [observed+72]
 mov QWORD PTR [observed],rax
 mov QWORD PTR [observed+8],rcx
 mov QWORD PTR [observed+16],rdx
 mov QWORD PTR [observed+24],r8
 mov QWORD PTR [observed+32],r9
 mov QWORD PTR [observed+40],r10
 mov QWORD PTR [observed+48],r11
 mov QWORD PTR [observed+56],rbp
 mov QWORD PTR [observed+64],r15
 mov rax,[rsp+28h]
 mov QWORD PTR [observed+80],rax
 mov rax,rsp
 mov QWORD PTR [observed+88],rax
 movdqu XMMWORD PTR [observed_simd],xmm0
 movdqu XMMWORD PTR [observed_simd+16],xmm1
 movdqu XMMWORD PTR [observed_simd+32],xmm2
 movdqu XMMWORD PTR [observed_simd+48],xmm3
 movdqu XMMWORD PTR [observed_simd+64],xmm4
 movdqu XMMWORD PTR [observed_simd+80],xmm5
 mov eax,1
 ret
original_sink ENDP
d5ar_capture_callback PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
 mov QWORD PTR [captured_arguments],rcx
 mov QWORD PTR [captured_arguments+8],rdx
 mov QWORD PTR [captured_arguments+16],r8
 mov QWORD PTR [captured_arguments+24],r9
 call fixture_capture_c
 mov rax,0badh
 mov rcx,0badh
 mov rdx,0badh
 mov r8,0badh
 mov r9,0badh
 mov r10,0badh
 mov r11,0badh
 pxor xmm0,xmm0
 pxor xmm1,xmm1
 pxor xmm2,xmm2
 pxor xmm3,xmm3
 pxor xmm4,xmm4
 pxor xmm5,xmm5
 stc
 lea rsp,[rsp+28h]
 ret
d5ar_capture_callback ENDP
d5ar_capture_area_callback PROC FRAME
 .endprolog
 jmp d5ar_capture_callback
d5ar_capture_area_callback ENDP
d5ar_area_entry PROC FRAME
 .endprolog
 mov eax,DWORD PTR [rsp+28h]
 mov QWORD PTR [captured_arguments+32],rax
 mov eax,DWORD PTR [rsp+30h]
 mov QWORD PTR [captured_arguments+40],rax
 jmp d5ar_capture_callback
d5ar_area_entry ENDP
d5ar_capture_selection PROC FRAME
 .endprolog
 jmp d5ar_capture_callback
d5ar_capture_selection ENDP
d5ar_capture_source_free PROC FRAME
 .endprolog
 jmp d5ar_capture_callback
d5ar_capture_source_free ENDP
END
