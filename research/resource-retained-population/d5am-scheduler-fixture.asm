; SPDX-License-Identifier: GPL-3.0-or-later
; Disposable ABI oracle, separate from the production bridges.
EXTERN D5AM_sched_activated:PROC
EXTERN D5AM_sched_dispatch:PROC
EXTERN D5AM_sched_retire:PROC
EXTERN D5AM_sched_ready:PROC
EXTERN D5AM_sched_dependency:PROC
EXTERN D5AM_sched_claim_entry:PROC
EXTERN D5AM_sched_queue_entry:PROC
EXTERN D5AM_fixture_server:BYTE
EXTERN D5AM_fixture_tree:BYTE
EXTERN D5AM_fixture_write:BYTE
EXTERN D5AM_fixture_server_pointer:QWORD
EXTERN D5AM_fixture_node_pointer:QWORD
EXTERN D5AM_fixture_dispatch_argument:QWORD
EXTERN D5AM_fixture_context:BYTE
EXTERN D5AM_fixture_command:QWORD
EXTERN D5AM_fixture_command_pointer:QWORD
EXTERN __imp_GetLastError:QWORD
EXTERN __imp_SetLastError:QWORD
.const
pattern QWORD 0123456789abcdefh,0fedcba9876543210h,0a55aa55aa55aa55ah,055aa55aa55aa55aah
.code
PUBLIC D5AM_sched_fixture_clobber
D5AM_sched_fixture_clobber PROC
 vpxor ymm0,ymm0,ymm0
 vpxor ymm1,ymm1,ymm1
 vpxor ymm2,ymm2,ymm2
 vpxor ymm3,ymm3,ymm3
 vpxor ymm4,ymm4,ymm4
 vpxor ymm5,ymm5,ymm5
 vzeroupper
 ret
D5AM_sched_fixture_clobber ENDP
PUBLIC D5AM_sched_probe_fall
D5AM_sched_probe_fall PROC
 ret
D5AM_sched_probe_fall ENDP

PUBLIC D5AM_sched_probe
D5AM_sched_probe PROC FRAME
 push rbx
 .pushreg rbx
 push rsi
 .pushreg rsi
 push rdi
 .pushreg rdi
 push r12
 .pushreg r12
 sub rsp,108h
 .allocstack 108h
 vmovdqu xmmword ptr [rsp+64],xmm6
 .savexmm128 xmm6,64
 vmovdqu xmmword ptr [rsp+80],xmm7
 .savexmm128 xmm7,80
 vmovdqu xmmword ptr [rsp+96],xmm8
 .savexmm128 xmm8,96
 vmovdqu xmmword ptr [rsp+112],xmm9
 .savexmm128 xmm9,112
 vmovdqu xmmword ptr [rsp+128],xmm10
 .savexmm128 xmm10,128
 vmovdqu xmmword ptr [rsp+144],xmm11
 .savexmm128 xmm11,144
 vmovdqu xmmword ptr [rsp+160],xmm12
 .savexmm128 xmm12,160
 vmovdqu xmmword ptr [rsp+176],xmm13
 .savexmm128 xmm13,176
 vmovdqu xmmword ptr [rsp+192],xmm14
 .savexmm128 xmm14,192
 vmovdqu xmmword ptr [rsp+208],xmm15
 .savexmm128 xmm15,208
 .endprolog
 mov rsi,rcx
 mov ebx,edx
 mov rdi,r8
 mov ecx,1234h
 call QWORD PTR __imp_SetLastError
 mov D5AM_fixture_node_pointer,rsi
 lea rcx,D5AM_fixture_server
 mov rdx,rsi
 lea r12,D5AM_sched_dispatch
 cmp ebx,2
 jne not_activated
 lea r12,D5AM_sched_activated
 lea rcx,D5AM_fixture_server_pointer
 lea rdx,D5AM_fixture_node_pointer
not_activated:
 cmp ebx,4
 jne not_retire
 lea r12,D5AM_sched_retire
not_retire:
 cmp ebx,5
 jne not_ready
 lea r12,D5AM_sched_ready
 lea rcx,D5AM_fixture_tree
not_ready:
 cmp ebx,6
 jne not_dependency
 lea r12,D5AM_sched_dependency
not_dependency:
 vmovdqu ymm0,ymmword ptr pattern
 vmovdqu ymm1,ymmword ptr pattern
 vmovdqu ymm2,ymmword ptr pattern
 vmovdqu ymm3,ymmword ptr pattern
 vmovdqu ymm4,ymmword ptr pattern
 vmovdqu ymm5,ymmword ptr pattern
 vmovdqu ymm6,ymmword ptr pattern
 vmovdqu ymm7,ymmword ptr pattern
 vmovdqu ymm8,ymmword ptr pattern
 vmovdqu ymm9,ymmword ptr pattern
 vmovdqu ymm10,ymmword ptr pattern
 vmovdqu ymm11,ymmword ptr pattern
 vmovdqu ymm12,ymmword ptr pattern
 vmovdqu ymm13,ymmword ptr pattern
 vmovdqu ymm14,ymmword ptr pattern
 vmovdqu ymm15,ymmword ptr pattern
 mov rax,rsi
 mov r8,8888888888888888h
 cmp ebx,3
 jne not_dispatch_argument
 mov r8,D5AM_fixture_dispatch_argument
not_dispatch_argument:
 mov r9,9999999999999999h
 mov r10,0aaaaaaaaaaaaaaaah
 lea r11,D5AM_fixture_write
 mov D5AM_fixture_command+16,rsi
 cmp ebx,10
 jne not_claim_entry
 lea r12,D5AM_sched_claim_entry
 lea rdx,D5AM_fixture_command_pointer
 lea r8,D5AM_fixture_context
 mov r9d,1
 mov QWORD PTR [rsp+32],0
not_claim_entry:
 cmp ebx,11
 jne not_queue_entry
 lea r12,D5AM_sched_queue_entry
 lea rcx,D5AM_fixture_context
 lea rdx,D5AM_fixture_command_pointer
not_queue_entry:
 stc
 call r12
 pushfq
 pop QWORD PTR [rdi]
 mov [rdi+8],rax
 mov [rdi+16],rcx
 mov [rdi+24],rdx
 mov [rdi+32],r8
 mov [rdi+40],r9
 mov [rdi+48],r10
 mov [rdi+56],r11
 vmovdqu ymmword ptr [rdi+64],ymm0
 vmovdqu ymmword ptr [rdi+96],ymm1
 vmovdqu ymmword ptr [rdi+128],ymm2
 vmovdqu ymmword ptr [rdi+160],ymm3
 vmovdqu ymmword ptr [rdi+192],ymm4
 vmovdqu ymmword ptr [rdi+224],ymm5
 vmovdqu ymmword ptr [rdi+256],ymm6
 vmovdqu ymmword ptr [rdi+288],ymm7
 vmovdqu ymmword ptr [rdi+320],ymm8
 vmovdqu ymmword ptr [rdi+352],ymm9
 vmovdqu ymmword ptr [rdi+384],ymm10
 vmovdqu ymmword ptr [rdi+416],ymm11
 vmovdqu ymmword ptr [rdi+448],ymm12
 vmovdqu ymmword ptr [rdi+480],ymm13
 vmovdqu ymmword ptr [rdi+512],ymm14
 vmovdqu ymmword ptr [rdi+544],ymm15
 call QWORD PTR __imp_GetLastError
 mov [rdi+576],rax
 mov rax,QWORD PTR D5AM_fixture_write+8
 mov [rdi+584],rax
 vmovdqu xmm6,xmmword ptr [rsp+64]
 vmovdqu xmm7,xmmword ptr [rsp+80]
 vmovdqu xmm8,xmmword ptr [rsp+96]
 vmovdqu xmm9,xmmword ptr [rsp+112]
 vmovdqu xmm10,xmmword ptr [rsp+128]
 vmovdqu xmm11,xmmword ptr [rsp+144]
 vmovdqu xmm12,xmmword ptr [rsp+160]
 vmovdqu xmm13,xmmword ptr [rsp+176]
 vmovdqu xmm14,xmmword ptr [rsp+192]
 vmovdqu xmm15,xmmword ptr [rsp+208]
 mov eax,1
 add rsp,108h
 pop r12
 pop rdi
 pop rsi
 pop rbx
 ret
D5AM_sched_probe ENDP
END
