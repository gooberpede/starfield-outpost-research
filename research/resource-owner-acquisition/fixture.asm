; SPDX-License-Identifier: GPL-3.0-or-later
; Original synthetic ABI fixture. It supplies retail stack/register relations,
; not copied retail instructions or an authoritative native semantics oracle.
EXTERN map_fixture_begin:PROC, map_fixture_next:PROC, map_fixture_step:PROC
EXTERN map_fixture_candidates:PROC
EXTERN map_fixture_has_descriptor:PROC
PUBLIC diagnostic_run, diagnostic_entry, diagnostic_call, diagnostic_return
PUBLIC map_loop, map_cleanup, map_return, map_wrapper_return
PUBLIC candidate_ready
.code
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
    push rbx
    push rsi
    push rdi
    push r12
    push r13
    push r14
    push r15
    sub rsp,2a0h
    mov r14,rcx
    mov rcx,rsp
    call map_fixture_begin
    lea r9,[rsp+210h]
    call map_wrapper
map_return LABEL BYTE
    nop
    call map_fixture_has_descriptor
    test eax,eax
    jz call_done
    mov rcx,rsp
    call map_fixture_candidates
    mov rbx,rax
    mov esi,dword ptr [rsp+40h]
    lea rsi,[rbx+rsi*8]
candidate_ready LABEL BYTE
    nop
call_next:
    cmp rbx,rsi
    je call_done
    mov rdx,[rbx]
    lea r8,[rsp+80h]
diagnostic_call LABEL BYTE
    nop
    add rbx,8
    jmp call_next
call_done:
    add rsp,2a0h
    pop r15
    pop r14
    pop r13
    pop r12
    pop rdi
    pop rsi
    pop rbx
    ret
diagnostic_inner ENDP
map_wrapper PROC
    sub rsp,48h
    call map_inner
map_wrapper_return LABEL BYTE
    nop
    add rsp,48h
    ret
map_wrapper ENDP
map_inner PROC
    push rdi
    push r12
    push r13
    push r14
    push r15
    sub rsp,0e0h
    mov r15,r9
    lea rbx,[rsp+0a0h]
    xor eax,eax
    mov [rsp+20h],rax
    mov [rsp+28h],rax
    mov rcx,rbx
    call map_fixture_next
    test eax,eax
    jz empty_range
map_again:
map_loop LABEL BYTE
    nop
    mov rcx,rbx
    lea rdx,[rsp+20h]
    mov r8,r15
    call map_fixture_step
    mov rcx,rbx
    call map_fixture_next
    test eax,eax
    jnz map_again
empty_range:
map_cleanup LABEL BYTE
    nop
    add rsp,0e0h
    pop r15
    pop r14
    pop r13
    pop r12
    pop rdi
    ret
map_inner ENDP
END
