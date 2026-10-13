; SPDX-License-Identifier: GPL-3.0-or-later
.code
EXTERN route_native_0:PROC
PUBLIC route_entry_0
PUBLIC route_call_0
route_entry_0 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_0 LABEL BYTE
 call route_native_0
 add rsp,58h
 ret
route_entry_0 ENDP
EXTERN route_native_1:PROC
PUBLIC route_entry_1
PUBLIC route_call_1
route_entry_1 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_1 LABEL BYTE
 call route_native_1
 add rsp,58h
 ret
route_entry_1 ENDP
EXTERN route_native_2:PROC
PUBLIC route_entry_2
PUBLIC route_call_2
route_entry_2 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_2 LABEL BYTE
 call route_native_2
 add rsp,58h
 ret
route_entry_2 ENDP
EXTERN route_native_3:PROC
PUBLIC route_entry_3
PUBLIC route_call_3
route_entry_3 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_3 LABEL BYTE
 call route_native_3
 add rsp,58h
 ret
route_entry_3 ENDP
EXTERN route_native_4:PROC
PUBLIC route_entry_4
PUBLIC route_call_4
route_entry_4 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_4 LABEL BYTE
 call route_native_4
 add rsp,58h
 ret
route_entry_4 ENDP
EXTERN route_native_5:PROC
PUBLIC route_entry_5
PUBLIC route_call_5
route_entry_5 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_5 LABEL BYTE
 call route_native_5
 add rsp,58h
 ret
route_entry_5 ENDP
EXTERN route_native_6:PROC
PUBLIC route_entry_6
PUBLIC route_call_6
route_entry_6 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_6 LABEL BYTE
 call route_native_6
 add rsp,58h
 ret
route_entry_6 ENDP
EXTERN route_native_7:PROC
PUBLIC route_entry_7
PUBLIC route_call_7
route_entry_7 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_7 LABEL BYTE
 call route_native_7
 add rsp,58h
 ret
route_entry_7 ENDP
EXTERN route_native_8:PROC
PUBLIC route_entry_8
PUBLIC route_call_8
route_entry_8 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_8 LABEL BYTE
 call route_native_8
 add rsp,58h
 ret
route_entry_8 ENDP
EXTERN route_native_9:PROC
PUBLIC route_entry_9
PUBLIC route_call_9
route_entry_9 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_9 LABEL BYTE
 call route_native_9
 add rsp,58h
 ret
route_entry_9 ENDP
EXTERN route_native_10:PROC
PUBLIC route_entry_10
PUBLIC route_call_10
route_entry_10 PROC FRAME
 sub rsp,58h
 .allocstack 58h
 .endprolog
 mov rax,[rsp+80h]
 mov [rsp+20h],rax
 mov rax,[rsp+88h]
 mov [rsp+28h],rax
 mov rax,[rsp+90h]
 mov [rsp+30h],rax
route_call_10 LABEL BYTE
 call route_native_10
 add rsp,58h
 ret
route_entry_10 ENDP

EXTERN producer_bridge:PROC
PUBLIC test_producer_entry
test_producer_entry PROC FRAME
 push rdi
 .pushreg rdi
 push rsi
 .pushreg rsi
 sub rsp,38h
 .allocstack 38h
 .endprolog
 mov rdi,[rsp+70h]
 mov rsi,[rsp+78h]
 call producer_bridge
 add rsp,38h
 pop rsi
 pop rdi
 ret
test_producer_entry ENDP
PUBLIC route_fp_mutate
route_fp_mutate PROC
 fnclex
 fldcw WORD PTR [rcx]
 fld1
 fldz
 fdivp st(1),st(0)
 fstp st(0)
 ret
route_fp_mutate ENDP
END
