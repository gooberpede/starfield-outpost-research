; SPDX-License-Identifier: GPL-3.0-or-later
; Owned disposable native stack fixture. Not retail code or a native oracle.
EXTERN fixture_next:PROC
EXTERN fixture_nested:PROC
EXTERN fixture_insert:PROC
EXTERN fixture_decide:PROC
EXTERN fixture_skip:PROC
PUBLIC fixture_updater_entry, fixture_run, fixture_callback_call, fixture_callback_return
PUBLIC fixture_update_return, fixture_transfer, fixture_accept, fixture_reject
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
    mov eax,43160000h
    movd xmm2,eax
    pxor xmm3,xmm3
    test dword ptr [rbx+44],2
    jnz other_update
    call update_inner
fixture_update_return LABEL BYTE
    nop
    jmp run_done
other_update:
    call update_inner
    nop
run_done:
    add rsp,28h
    pop rbx
    pop rdi
    pop rsi
    pop r14
    ret
fixture_run ENDP
update_inner PROC
fixture_updater_entry LABEL BYTE
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
    mov [rbp-48h],rdx
    lea rax,[rsp+60h]
    mov [rbp-40h],rax
    lea rax,[rsp+80h]
    mov [rsp+60h],rax
    mov [rsp+68h],rax
    add rax,20h
    mov [rsp+70h],rax
    mov dword ptr [rbp-38h],43160000h
    mov dword ptr [rbp-34h],0
callback_next:
    mov r15,[rbx+24]
    mov rdi,[rbx+56]
    mov r8,[rbx+16]
    mov rdx,rbx
    lea rcx,[rbp-48h]
    test dword ptr [rbx+44],1
    jnz wrong_callback
fixture_callback_call LABEL BYTE
    call callback_inner
fixture_callback_return LABEL BYTE
    nop
    jmp callback_finished
wrong_callback:
    call callback_inner
    nop
callback_finished:
    mov rcx,rbx
    call fixture_next
    mov rax,[rbx+48]
    test rax,rax
    jz transfer_ready
    mov rbx,rax
    jmp callback_next
transfer_ready:
    test dword ptr [rbx+44],16
    jz not_empty
    mov rax,[rsp+60h]
    mov [rsp+68h],rax
not_empty:
    lea rdx,[rsp+60h]
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
callback_inner PROC
    mov rax,rsp
    mov [rax+8],rbx
    mov [rax+10h],rdx
    push rbp
    push rsi
    push rdi
    push r12
    push r13
    push r14
    push r15
    lea rbp,[rax-1c8h]
    sub rsp,290h
    mov rsi,rcx
    mov rdi,rdx
    mov rax,[r8]
    mov [rbp-58h],rax
    mov r13,[rdi]
    mov rbx,[rdi+8]
    xor r12d,r12d
    mov rax,[rsi]
    mov rdx,[rax]
    mov [rbp+70h],rdx
    mov edx,[rax+8]
    mov [rbp+78h],edx
    test dword ptr [rdi+44],32
    jz no_index_offset
    mov eax,42c80000h
    movd xmm0,eax
    addss xmm0,dword ptr [rbp+70h]
    movss dword ptr [rbp+70h],xmm0
no_index_offset:
    mov rcx,rdi
    call fixture_nested
    mov rcx,rdi
    mov rdx,rsi
    call fixture_skip
    test eax,eax
    jnz callback_done
    mov rcx,rdi
    mov rdx,rsi
    call fixture_decide
    test eax,eax
    jz rejected
fixture_accept LABEL BYTE
    nop
    mov rcx,[rsi+8]
    mov rdx,r13
    call fixture_insert
    jmp callback_done
rejected:
fixture_reject LABEL BYTE
    nop
callback_done:
    add rsp,290h
    pop r15
    pop r14
    pop r13
    pop r12
    pop rdi
    pop rsi
    pop rbp
    mov rbx,[rsp+8]
    mov eax,1
    ret
callback_inner ENDP
PUBLIC diagnostic_run,diagnostic_entry,diagnostic_call,diagnostic_return
diagnostic_run PROC
    sub rsp,28h
    call diagnostic_inner
diagnostic_return LABEL BYTE
    nop
    add rsp,28h
    ret
diagnostic_run ENDP
diagnostic_inner PROC
diagnostic_entry LABEL BYTE
    sub rsp,2d8h
diagnostic_call LABEL BYTE
    nop
    add rsp,2d8h
    ret
diagnostic_inner ENDP
END
