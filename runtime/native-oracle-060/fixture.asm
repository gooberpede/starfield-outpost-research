; SPDX-License-Identifier: GPL-3.0-or-later
; Owned 050 ABI probe adapted; original disposable call fixture.
EXTERN fixture_writer:PROC
PUBLIC fixture_call
PUBLIC fixture_call_site
.code
fixture_call PROC FRAME
 sub rsp,28h
 .allocstack 28h
 .endprolog
fixture_call_site LABEL BYTE
 call fixture_writer
 add rsp,28h
 ret
fixture_call ENDP
PUBLIC abi_probe
.const
ALIGN 16
probe_pattern BYTE 16 DUP (05ah)
.code
abi_probe PROC FRAME
    push rbx
    .pushreg rbx
    push rbp
    .pushreg rbp
    push rsi
    .pushreg rsi
    push rdi
    .pushreg rdi
    push r12
    .pushreg r12
    push r13
    .pushreg r13
    push r14
    .pushreg r14
    push r15
    .pushreg r15
    sub rsp,0e8h
    .allocstack 0e8h
    movdqa [rsp+40h],xmm6
    .savexmm128 xmm6,40h
    movdqa [rsp+50h],xmm7
    .savexmm128 xmm7,50h
    movdqa [rsp+60h],xmm8
    .savexmm128 xmm8,60h
    movdqa [rsp+70h],xmm9
    .savexmm128 xmm9,70h
    movdqa [rsp+80h],xmm10
    .savexmm128 xmm10,80h
    movdqa [rsp+90h],xmm11
    .savexmm128 xmm11,90h
    movdqa [rsp+0a0h],xmm12
    .savexmm128 xmm12,0a0h
    movdqa [rsp+0b0h],xmm13
    .savexmm128 xmm13,0b0h
    movdqa [rsp+0c0h],xmm14
    .savexmm128 xmm14,0c0h
    movdqa [rsp+0d0h],xmm15
    .savexmm128 xmm15,0d0h
    .endprolog
    mov [rsp+20h],rcx
    mov [rsp+28h],rdx
    mov [rsp+30h],r8
    mov rbx,12340000h
    mov rbp,12340001h
    mov rsi,12340002h
    mov rdi,12340003h
    mov r12,12340004h
    mov r13,12340005h
    mov r14,12340006h
    mov r15,12340007h
    movdqa xmm6,XMMWORD PTR probe_pattern
    movdqa xmm7,XMMWORD PTR probe_pattern
    movdqa xmm8,XMMWORD PTR probe_pattern
    movdqa xmm9,XMMWORD PTR probe_pattern
    movdqa xmm10,XMMWORD PTR probe_pattern
    movdqa xmm11,XMMWORD PTR probe_pattern
    movdqa xmm12,XMMWORD PTR probe_pattern
    movdqa xmm13,XMMWORD PTR probe_pattern
    movdqa xmm14,XMMWORD PTR probe_pattern
    movdqa xmm15,XMMWORD PTR probe_pattern
    mov rcx,[rsp+28h]
    mov rdx,[rsp+30h]
    xor r8d,r8d
    call QWORD PTR [rsp+20h]
    xor r10d,r10d
    cmp rbx,12340000h
    je ok_gpr_0
    or r10d,1h
ok_gpr_0:
    cmp rbp,12340001h
    je ok_gpr_1
    or r10d,2h
ok_gpr_1:
    cmp rsi,12340002h
    je ok_gpr_2
    or r10d,4h
ok_gpr_2:
    cmp rdi,12340003h
    je ok_gpr_3
    or r10d,8h
ok_gpr_3:
    cmp r12,12340004h
    je ok_gpr_4
    or r10d,10h
ok_gpr_4:
    cmp r13,12340005h
    je ok_gpr_5
    or r10d,20h
ok_gpr_5:
    cmp r14,12340006h
    je ok_gpr_6
    or r10d,40h
ok_gpr_6:
    cmp r15,12340007h
    je ok_gpr_7
    or r10d,80h
ok_gpr_7:
    movdqa xmm0,xmm6
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_0
    or r10d,100h
ok_xmm_0:
    movdqa xmm0,xmm7
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_1
    or r10d,200h
ok_xmm_1:
    movdqa xmm0,xmm8
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_2
    or r10d,400h
ok_xmm_2:
    movdqa xmm0,xmm9
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_3
    or r10d,800h
ok_xmm_3:
    movdqa xmm0,xmm10
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_4
    or r10d,1000h
ok_xmm_4:
    movdqa xmm0,xmm11
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_5
    or r10d,2000h
ok_xmm_5:
    movdqa xmm0,xmm12
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_6
    or r10d,4000h
ok_xmm_6:
    movdqa xmm0,xmm13
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_7
    or r10d,8000h
ok_xmm_7:
    movdqa xmm0,xmm14
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_8
    or r10d,10000h
ok_xmm_8:
    movdqa xmm0,xmm15
    pcmpeqb xmm0,XMMWORD PTR probe_pattern
    pmovmskb eax,xmm0
    cmp eax,0ffffh
    je ok_xmm_9
    or r10d,20000h
ok_xmm_9:
    movdqa xmm6,[rsp+40h]
    movdqa xmm7,[rsp+50h]
    movdqa xmm8,[rsp+60h]
    movdqa xmm9,[rsp+70h]
    movdqa xmm10,[rsp+80h]
    movdqa xmm11,[rsp+90h]
    movdqa xmm12,[rsp+0a0h]
    movdqa xmm13,[rsp+0b0h]
    movdqa xmm14,[rsp+0c0h]
    movdqa xmm15,[rsp+0d0h]
    mov eax,r10d
    add rsp,0e8h
    pop r15
    pop r14
    pop r13
    pop r12
    pop rdi
    pop rsi
    pop rbp
    pop rbx
    ret
abi_probe ENDP
END
