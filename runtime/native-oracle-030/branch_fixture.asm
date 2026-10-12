; SPDX-License-Identifier: GPL-3.0-or-later
; Original synthetic complete CALL sites, compiler-contract arguments only.
.code
EXTERN branch_native_0:PROC
PUBLIC branch_entry_0
PUBLIC branch_call_0
branch_entry_0 PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
branch_call_0 LABEL BYTE
 call branch_native_0
 add rsp,28h
 ret
branch_entry_0 ENDP
EXTERN branch_native_1:PROC
PUBLIC branch_entry_1
PUBLIC branch_call_1
branch_entry_1 PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
branch_call_1 LABEL BYTE
 call branch_native_1
 add rsp,28h
 ret
branch_entry_1 ENDP
EXTERN branch_native_2:PROC
PUBLIC branch_entry_2
PUBLIC branch_call_2
branch_entry_2 PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
branch_call_2 LABEL BYTE
 call branch_native_2
 add rsp,28h
 ret
branch_entry_2 ENDP
EXTERN branch_native_3:PROC
PUBLIC branch_entry_3
PUBLIC branch_call_3
branch_entry_3 PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
branch_call_3 LABEL BYTE
 call branch_native_3
 add rsp,28h
 ret
branch_entry_3 ENDP
EXTERN branch_native_4:PROC
PUBLIC branch_entry_4
PUBLIC branch_call_4
branch_entry_4 PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
branch_call_4 LABEL BYTE
 call branch_native_4
 add rsp,28h
 ret
branch_entry_4 ENDP
EXTERN branch_native_5:PROC
PUBLIC branch_entry_5
PUBLIC branch_call_5
branch_entry_5 PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
branch_call_5 LABEL BYTE
 call branch_native_5
 add rsp,28h
 ret
branch_entry_5 ENDP
EXTERN branch_native_6:PROC
PUBLIC branch_entry_6
PUBLIC branch_call_6
branch_entry_6 PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
branch_call_6 LABEL BYTE
 call branch_native_6
 add rsp,28h
 ret
branch_entry_6 ENDP
PUBLIC branch_fp_mutate
branch_fp_mutate PROC
 fnclex
 fldcw WORD PTR [rcx]
 fld1
 fldz
 fdivp st(1),st(0)
 fstp st(0)
 ret
branch_fp_mutate ENDP
END
