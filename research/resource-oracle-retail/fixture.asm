; SPDX-License-Identifier: GPL-3.0-or-later
; Original synthetic stack-shape fixture. Never linked into retail controller.
PUBLIC fixture_update_call, fixture_update_return, fixture_transfer
PUBLIC fixture_selector, fixture_grid_return, fixture_run
.code
fixture_run PROC
    push r14
    push rsi
    push rdi
    push rbx
    sub rsp,28h
    mov r14,rcx
    mov rsi,rdx
    mov rdi,r8
    mov rbx,r9
    lea rcx,[rsi+520h]
    lea rdx,[rsi+338h]
    cmp rbx,2
    je other_update
fixture_update_call LABEL BYTE
    call update_inner
fixture_update_return LABEL BYTE
    nop
    jmp after_update
other_update:
    call update_inner
    nop
after_update:
    lea rcx,[rsi+520h]
    mov rdx,rdi
    mov rdi,r14
    cmp rbx,1
    je wrong_caller
    call gate_inner
fixture_grid_return LABEL BYTE
    nop
    jmp finish
wrong_caller:
    call gate_inner
    nop
finish:
    add rsp,28h
    pop rbx
    pop rdi
    pop rsi
    pop r14
    ret
fixture_run ENDP
update_inner PROC
    mov rax,rsp
    mov [rax+8],rbx
    mov [rax+18h],rsi
    mov [rax+20h],rdi
    push rbp
    push r12
    push r13
    push r14
    push r15
    lea rbp,[rax-38h]
    sub rsp,110h
    mov r13,rdx
    mov r14,rcx
    mov rdx,rdi
fixture_transfer LABEL BYTE
    nop
    add rsp,110h
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbp
    mov rbx,[rsp+8]
    mov rsi,[rsp+18h]
    mov rdi,[rsp+20h]
    ret
update_inner ENDP
gate_inner PROC
    mov [rsp+8],rbx
    push rbp
    push rsi
    push rdi
    push r14
    push r15
    lea rbp,[rsp-37h]
    sub rsp,0d0h
    mov rax,[rdx]
    mov [rbp-79h],rax
    mov rax,[rdx+8]
    mov [rbp-71h],rax
    mov rax,[rdx+10h]
    mov [rbp-69h],rax
fixture_selector LABEL BYTE
    nop
    mov sil,1
    movzx eax,sil
    mov rbx,[rsp+100h]
    add rsp,0d0h
    pop r15
    pop r14
    pop rdi
    pop rsi
    pop rbp
    ret
gate_inner ENDP
END
