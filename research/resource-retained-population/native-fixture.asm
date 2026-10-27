; SPDX-License-Identifier: GPL-3.0-or-later
; Original ABI scaffold. It supplies native-shaped registers/stacks/memory;
; C++ performs the disclosed synthetic generation, never game-native calls.
option casemap:none
extern fixture_native_visit:proc
extern fixture_native_lookup:proc
extern fixture_native_insert:proc
extern fixture_native_release:proc
extern fixture_native_append:proc
.code
public fixture_source_init,native_execute,native_visited,native_lookup,native_query,native_mask,native_append,native_complete
public native_init,native_reset,native_destroy,native_erase,native_grid_clear,native_source_init
public native_grid_init,after_native_grid_init,fixture_init,fixture_reset,fixture_grid_init
public native_source_retire,after_native_source_retire
public after_native_visited,after_native_lookup,after_native_query,after_native_mask,after_native_append,after_native_complete
public after_native_init,after_native_reset,after_native_destroy,after_native_erase,after_native_grid_clear,after_native_source_init
public native_inner_return,native_outer_return,native_outer_return2
native_execute proc
 push rbp
 push rbx
 push rsi
 push rdi
 push r12
 push r13
 push r14
 push r15
 sub rsp,408h
 mov [rsp+80h],rcx
 mov rax,[rcx]
 mov [rsp+3d0h],rax
 mov r13,rax
 mov rax,[rcx+8]
 mov [rsp+38h],rax
 mov rax,[rcx+16]
 mov [rsp+100h],rax
 mov rax,[rcx+24]
 mov [rsp+3d8h],rax
 lea rbp,[rsp+100h]
 call fixture_native_visit
 mov sil,al
 mov rdi,[rsp+38h]
 mov rdi,[rdi+68h]
native_visited::
 test sil,sil
after_native_visited::
 jnz provider_done
 mov rcx,[rsp+80h]
 call fixture_native_lookup
native_lookup::
 cmp rax,[r13+28h]
after_native_lookup::
 jne provider_release
 mov rcx,[rsp+80h]
 call fixture_native_insert
 mov rcx,[rsp+80h]
 mov r8,[rcx+32]
 mov r9,[rcx+24]
native_query::
 call converter
 call generator
native_complete::
 lea rax,[native_execute]
after_native_complete::
provider_release:
 mov rcx,[rsp+80h]
 call fixture_native_release
provider_done:
 add rsp,408h
 pop r15
 pop r14
 pop r13
 pop r12
 pop rdi
 pop rsi
 pop rbx
 pop rbp
 ret
native_execute endp
converter proc
after_native_query::
 ret
converter endp
generator proc
 push rbx
 push rsi
 push rdi
 push r12
 push r13
 push r14
 push r15
 sub rsp,2a0h
 mov rcx,[rsp+360h]
 test dword ptr [rcx+88],8
 jnz generation_done
 mov rax,[rcx+40]
 mov [rsp+2f0h],rax
 mov eax,[rcx+48]
native_mask::
 mov [rsp+30h],al
after_native_mask::
 call cell_loop
native_outer_return::
 mov rcx,[rsp+360h]
 test dword ptr [rcx+88],4
 jz generation_done
 mov dword ptr [rcx+92],1
 call cell_loop
native_outer_return2::
generation_done:
 add rsp,2a0h
 pop r15
 pop r14
 pop r13
 pop r12
 pop rdi
 pop rsi
 pop rbx
 ret
generator endp
cell_loop proc
 push rsi
 push rdi
 push r14
 sub rsp,50h
 call inner
native_inner_return::
 add rsp,50h
 pop r14
 pop rdi
 pop rsi
 ret
cell_loop endp
inner proc
 push rbx
 push rsi
 push rdi
 push r12
 push r13
 push r14
 push r15
 sub rsp,1d0h
 mov rcx,[rsp+5e0h]
 mov eax,[rcx+80]
 mov [rsp+230h],eax
 lea rdx,[rsp+50h]
 call fixture_native_append
 mov rcx,[rsp+5e0h]
 mov rbx,[rcx+72]
native_append::
 mov r12b,1
after_native_append::
 add rsp,1d0h
 pop r15
 pop r14
 pop r13
 pop r12
 pop rdi
 pop rsi
 pop rbx
 ret
inner endp
fixture_init proc
 push rdi
 mov rdi,rcx
 xor ecx,ecx
native_init::
 mov rax,rdi
after_native_init::
 pop rdi
 ret
fixture_init endp
fixture_reset proc
 push rsi
 mov rsi,rcx
 xor ecx,ecx
native_reset::
 mov rax,[rsi+28h]
after_native_reset::
 pop rsi
 ret
fixture_reset endp
fixture_grid_init proc
 push r15
 mov r15,rcx
 xor ecx,ecx
native_grid_init::
 mov rax,r15
after_native_grid_init::
 pop r15
 ret
fixture_grid_init endp
native_destroy proc
 mov [rsp+8],rbx
after_native_destroy::
 ret
native_destroy endp
native_erase proc
 db 40h
 push rbx
after_native_erase::
 pop rbx
 ret
native_erase endp
native_grid_clear proc
 mov [rsp+10h],rbx
after_native_grid_clear::
 ret
native_grid_clear endp
native_source_retire proc
 mov [rsp+10h],rbx
after_native_source_retire::
 ret
native_source_retire endp
fixture_source_init proc
 push r12
 push r13
 push r14
 mov r14,rcx
 lea r12,[rdx+10h]
 mov r13,r8
 xor ecx,ecx
native_source_init::
 jmp short source_after
 db 6 dup(90h)
source_after:
after_native_source_init::
 pop r14
 pop r13
 pop r12
 ret
fixture_source_init endp
end
