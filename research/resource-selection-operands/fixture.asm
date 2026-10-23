; SPDX-License-Identifier: GPL-3.0-or-later
; Original synthetic caller frames. Not copied retail instruction payloads.
EXTERN fixture_setup:PROC
EXTERN fixture_nested:PROC
EXTERN fixture_cell_setup:PROC
.code
PUBLIC fixture_entry,fixture_resource_call,fixture_resource_return
PUBLIC fixture_cell_return,fixture_chance,fixture_terminal,fixture_run
fixture_run PROC
    push r12
    sub rsp,40h
    mov r12,rcx
    mov rax,[r12+20h]
    mov [rsp+20h],rax
    mov rax,[r12+28h]
    mov [rsp+28h],rax
    mov [rsp+30h],r12
    mov rcx,[r12]
    mov rdx,[r12+8]
    mov r8,[r12+10h]
    mov r9d,[r12+18h]
    call fixture_generation
fixture_terminal LABEL BYTE
    nop
    add rsp,40h
    pop r12
    ret
fixture_run ENDP
fixture_generation PROC
fixture_entry LABEL BYTE
    mov rax,rsp
    mov [rax+8],rcx
    mov [rax+10h],rdx
    mov [rax+18h],r8
    mov [rax+20h],r9d
    push rbx
    push rsi
    push rdi
    push r12
    push r13
    push r14
    push r15
    sub rsp,2a0h
    mov r12,[rsp+310h]
    mov rcx,r12
    mov rdx,rsp
    call fixture_setup
    mov rcx,r12
    call fixture_nested
resource_loop:
    mov rdx,[r12+30h]
    movzx edi,byte ptr [rsp+30h]
    mov eax,[rdx+110h]
    and eax,0ffh
    mov ecx,3f800000h
    cmp dil,8
    je inactive
    cmp al,dil
    jbe weight_ready
inactive:
    mov ecx,[r12+48h]
    cmp eax,5
    jbe weight_ready
    xor ecx,ecx
weight_ready:
    movd xmm3,ecx
    mov r8,[r12+38h]
    lea rcx,[rsp+180h]
    mov rbx,[rsp+50h]
    mov rax,[r12+68h]
    lea rbx,[rbx+rax*8]
fixture_resource_call LABEL BYTE
    call fixture_cells
fixture_resource_return LABEL BYTE
    nop
    mov r12,[r12+58h]
    test r12,r12
    jz resource_done
    mov rcx,r12
    mov rdx,rsp
    call fixture_setup
    jmp resource_loop
resource_done:
    add rsp,2a0h
    pop r15
    pop r14
    pop r13
    pop r12
    pop rdi
    pop rsi
    pop rbx
    ret
fixture_generation ENDP
fixture_cells PROC
    mov [rsp+18h],rbp
    push rsi
    push rdi
    push r14
    sub rsp,50h
    mov rbp,r8
    mov r14,rdx
    mov rdi,rcx
    movd dword ptr [rsp+40h],xmm3
    mov dword ptr [rsp+70h],10
    mov dword ptr [rsp+74h],1
cell_loop:
    lea rdx,[rsp+70h]
    mov rcx,r14
    mov r8,[rdi]
    mov r9,[rdi+18h]
    mov [rsp+20h],rbp
    mov eax,[rsp+40h]
    mov [rsp+28h],eax
    mov rax,[rdi+8]
    mov [rsp+30h],rax
    ; Deliberately clobber XMM3: it is no longer the weight here.
    pxor xmm3,xmm3
    call fixture_cell
fixture_cell_return LABEL BYTE
    nop
    inc dword ptr [rsp+70h]
    cmp dword ptr [rsp+70h],12
    jl cell_loop
    mov rbp,[rsp+80h]
    add rsp,50h
    pop r14
    pop rdi
    pop rsi
    ret
fixture_cells ENDP
fixture_cell PROC
    mov rax,rsp
    mov [rax+10h],rdx
    mov [rax+18h],r8
    push rbx
    push rsi
    push rdi
    push r12
    push r13
    push r14
    push r15
    sub rsp,1d0h
    mov rsi,rcx
    mov r8,rdx
    mov rdx,rsi
    mov rcx,rsp
    call fixture_cell_setup
    movzx eax,byte ptr [rsi+110h]
    add eax,7
    imul eax,eax,40
    mov r14,[rsp+230h]
    add r14,rax
    movss xmm7,dword ptr [rsp+238h]
    mulss xmm7,dword ptr [r14+1ch]
    movss xmm1,dword ptr [rsp+0a8h]
    comiss xmm1,xmm7
fixture_chance LABEL BYTE
    jnc rejected
    nop
rejected:
    add rsp,1d0h
    pop r15
    pop r14
    pop r13
    pop r12
    pop rdi
    pop rsi
    pop rbx
    ret
fixture_cell ENDP
END
