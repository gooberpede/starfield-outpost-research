; SPDX-License-Identifier: GPL-3.0-or-later
; Original fixture only. Reproduces ABI/stack shapes, not retail implementation.
extern CenterBody:proc
extern GridBody:proc
public CenterEntry, CenterExit, GridEntry, GridX, GridY, GridResult, GridExit, CheckState
.const
Scale real4 0.01
.code
CenterEntry proc frame
    mov [rsp+8],rbx
    push rdi
    .pushreg rdi
    sub rsp,30h
    .allocstack 30h
    .savereg rbx,40h
    .endprolog
    mov rbx,rcx
    mov rdi,rdx
    call CenterBody
CenterExit label byte
    mov rbx,[rsp+40h]
    add rsp,30h
    pop rdi
    ret
CenterEntry endp
GridEntry proc frame
    mov [rsp+18h],rbx
    mov [rsp+20h],rsi
    push rbp
    .pushreg rbp
    lea rbp,[rsp-57h]
    sub rsp,0c0h
    .allocstack 0c0h
    .savereg rbx,0e0h
    .savereg rsi,0e8h
    .endprolog
    mov rbx,rdx
    mov rsi,rcx
    lea r8,[rbp-49h]
    lea r9,[rbp-9]
    call GridBody
    mov rax,[rsi+20h]
    movss xmm4,Scale
    movss xmm0,dword ptr [rax]
    addss xmm0,dword ptr [rbp-49h]
GridX label byte
    vmulss xmm1,xmm0,xmm4
    movss xmm0,dword ptr [rax+4]
    addss xmm0,dword ptr [rbp-45h]
GridY label byte
    vmulss xmm2,xmm0,xmm4
GridResult label byte
    mov rax,[rsi+10h]
    xor eax,eax
GridExit label byte
    lea r11,[rsp+0c0h]
    mov rbx,[r11+20h]
    mov rsi,[r11+28h]
    mov rsp,r11
    pop rbp
    ret
GridEntry endp
; Verify caller nonvolatile/SIMD/MXCSR/stack survive instrumentation.
CheckState proc frame
    push rbx
    .pushreg rbx
    push rdi
    .pushreg rdi
    push rsi
    .pushreg rsi
    push rbp
    .pushreg rbp
    push r12
    .pushreg r12
    push r13
    .pushreg r13
    push r14
    .pushreg r14
    push r15
    .pushreg r15
    sub rsp,0c8h
    .allocstack 0c8h
    movdqu [rsp+20h],xmm6
    .savexmm128 xmm6,20h
    movdqu [rsp+30h],xmm7
    .savexmm128 xmm7,30h
    movdqu [rsp+40h],xmm8
    .savexmm128 xmm8,40h
    movdqu [rsp+50h],xmm9
    .savexmm128 xmm9,50h
    movdqu [rsp+60h],xmm10
    .savexmm128 xmm10,60h
    movdqu [rsp+70h],xmm11
    .savexmm128 xmm11,70h
    movdqu [rsp+80h],xmm12
    .savexmm128 xmm12,80h
    movdqu [rsp+90h],xmm13
    .savexmm128 xmm13,90h
    movdqu [rsp+0a0h],xmm14
    .savexmm128 xmm14,0a0h
    movdqu [rsp+0b0h],xmm15
    .savexmm128 xmm15,0b0h
    .endprolog
    stmxcsr [rsp+0c0h]
    mov rbx,1122334455667700h
    mov rdi,1122334455667701h
    mov rsi,1122334455667702h
    mov rbp,1122334455667703h
    mov r12,1122334455667704h
    mov r13,1122334455667705h
    mov r14,1122334455667706h
    mov r15,1122334455667707h
    pcmpeqd xmm6,xmm6
    pcmpeqd xmm7,xmm7
    pcmpeqd xmm8,xmm8
    pcmpeqd xmm9,xmm9
    pcmpeqd xmm10,xmm10
    pcmpeqd xmm11,xmm11
    pcmpeqd xmm12,xmm12
    pcmpeqd xmm13,xmm13
    pcmpeqd xmm14,xmm14
    pcmpeqd xmm15,xmm15
    call CenterEntry
    mov rax,1122334455667700h
    cmp rbx,rax
    jne bad
    mov rax,1122334455667701h
    cmp rdi,rax
    jne bad
    mov rax,1122334455667702h
    cmp rsi,rax
    jne bad
    mov rax,1122334455667703h
    cmp rbp,rax
    jne bad
    mov rax,1122334455667704h
    cmp r12,rax
    jne bad
    mov rax,1122334455667705h
    cmp r13,rax
    jne bad
    mov rax,1122334455667706h
    cmp r14,rax
    jne bad
    mov rax,1122334455667707h
    cmp r15,rax
    jne bad
    pmovmskb eax,xmm6
    cmp eax,0ffffh
    jne bad
    pmovmskb eax,xmm7
    cmp eax,0ffffh
    jne bad
    pmovmskb eax,xmm8
    cmp eax,0ffffh
    jne bad
    pmovmskb eax,xmm9
    cmp eax,0ffffh
    jne bad
    pmovmskb eax,xmm10
    cmp eax,0ffffh
    jne bad
    pmovmskb eax,xmm11
    cmp eax,0ffffh
    jne bad
    pmovmskb eax,xmm12
    cmp eax,0ffffh
    jne bad
    pmovmskb eax,xmm13
    cmp eax,0ffffh
    jne bad
    pmovmskb eax,xmm14
    cmp eax,0ffffh
    jne bad
    pmovmskb eax,xmm15
    cmp eax,0ffffh
    jne bad
    stmxcsr [rsp+0c4h]
    mov eax,[rsp+0c0h]
    cmp eax,[rsp+0c4h]
    jne bad
    mov eax,1
    jmp done
bad:
    xor eax,eax
done:
    movdqu xmm6,[rsp+20h]
    movdqu xmm7,[rsp+30h]
    movdqu xmm8,[rsp+40h]
    movdqu xmm9,[rsp+50h]
    movdqu xmm10,[rsp+60h]
    movdqu xmm11,[rsp+70h]
    movdqu xmm12,[rsp+80h]
    movdqu xmm13,[rsp+90h]
    movdqu xmm14,[rsp+0a0h]
    movdqu xmm15,[rsp+0b0h]
    add rsp,0c8h
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbp
    pop rsi
    pop rdi
    pop rbx
    ret
CheckState endp
end
