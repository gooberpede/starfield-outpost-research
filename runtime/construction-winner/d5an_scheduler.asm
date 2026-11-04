; SPDX-License-Identifier: GPL-3.0-or-later
; Every site reaches this bridge with RSP mod 16 = 8. Framed inline sites use
; CALL; the three function-entry sites use JMP and retain their native return.
; Generic filtering performs bounded native loads only. Matched callbacks save
; all sixteen YMM registers; flags and volatile GPRs are restored on both paths.
EXTERN D5AM_sched_registry:BYTE
EXTERN D5AM_sched_vtables:QWORD
EXTERN D5AM_sched_falls:QWORD
EXTERN D5AM_sched_capture_admitted:PROC
EXTERN D5AM_sched_dispatch_admitted:PROC
EXTERN D5AM_sched_ready_admitted:PROC
EXTERN D5AM_sched_callback_target:QWORD
EXTERN D5AM_sched_command_capture:PROC
EXTERN D5AM_sched_core_active:QWORD
EXTERN D5AM_sched_enabled:QWORD
EXTERN D5AM_sched_bridge_active:QWORD
EXTERN D5AM_sched_counter_faults:QWORD
EXTERN D5AM_sched_fixture_admission:QWORD
EXTERN D5AM_sched_claim_proxy:PROC
EXTERN D5AM_sched_queue_proxy:PROC
EXTERN D5AN_counter_next:PROC
EXTERN D5AN_counter_leave:PROC
.code
save_frame MACRO
 push rbp
 .pushreg rbp
 pushfq
 .allocstack 8
 push rax
 .allocstack 8
 push rcx
 .allocstack 8
 push rdx
 .allocstack 8
 push r8
 .allocstack 8
 push r9
 .allocstack 8
 push r10
 .allocstack 8
 push r11
 .allocstack 8
 sub rsp,640
 .allocstack 640
 mov rbp,rsp
 .setframe rbp,0
 .endprolog
ENDM
save_ymm MACRO
 vmovdqu ymmword ptr [rsp+128],ymm0
 vmovdqu ymmword ptr [rsp+160],ymm1
 vmovdqu ymmword ptr [rsp+192],ymm2
 vmovdqu ymmword ptr [rsp+224],ymm3
 vmovdqu ymmword ptr [rsp+256],ymm4
 vmovdqu ymmword ptr [rsp+288],ymm5
 vmovdqu ymmword ptr [rsp+320],ymm6
 vmovdqu ymmword ptr [rsp+352],ymm7
 vmovdqu ymmword ptr [rsp+384],ymm8
 vmovdqu ymmword ptr [rsp+416],ymm9
 vmovdqu ymmword ptr [rsp+448],ymm10
 vmovdqu ymmword ptr [rsp+480],ymm11
 vmovdqu ymmword ptr [rsp+512],ymm12
 vmovdqu ymmword ptr [rsp+544],ymm13
 vmovdqu ymmword ptr [rsp+576],ymm14
 vmovdqu ymmword ptr [rsp+608],ymm15
ENDM
restore_ymm MACRO
 vmovdqu ymm0,ymmword ptr [rsp+128]
 vmovdqu ymm1,ymmword ptr [rsp+160]
 vmovdqu ymm2,ymmword ptr [rsp+192]
 vmovdqu ymm3,ymmword ptr [rsp+224]
 vmovdqu ymm4,ymmword ptr [rsp+256]
 vmovdqu ymm5,ymmword ptr [rsp+288]
 vmovdqu ymm6,ymmword ptr [rsp+320]
 vmovdqu ymm7,ymmword ptr [rsp+352]
 vmovdqu ymm8,ymmword ptr [rsp+384]
 vmovdqu ymm9,ymmword ptr [rsp+416]
 vmovdqu ymm10,ymmword ptr [rsp+448]
 vmovdqu ymm11,ymmword ptr [rsp+480]
 vmovdqu ymm12,ymmword ptr [rsp+512]
 vmovdqu ymm13,ymmword ptr [rsp+544]
 vmovdqu ymm14,ymmword ptr [rsp+576]
 vmovdqu ymm15,ymmword ptr [rsp+608]
ENDM
restore_frame MACRO
 mov r11,[rbp+640]
 mov r10,[rbp+648]
 mov r9,[rbp+656]
 mov r8,[rbp+664]
 mov rdx,[rbp+672]
 mov rcx,[rbp+680]
 mov rax,[rbp+688]
 push QWORD PTR [rbp+696]
 popfq
 lea rsp,[rbp+704]
 pop rbp
ENDM
; R11 is the native-owned node. The cookie copies its key before the operation
; and the current observer registry allocation/serial before any C++ callback.
copy_cookie MACRO missing
 LOCAL search,found
 mov [rsp+80],r11
 mov rax,[r11+8]
 mov [rsp+32],rax
 mov eax,[r11+16]
 mov [rsp+40],rax
 mov rax,[r11]
 mov [rsp+48],rax
 mov QWORD PTR [rsp+56],0
 mov QWORD PTR [rsp+64],0
 mov QWORD PTR [rsp+72],-1
 mov rax,r11
 shr rax,4
 and eax,32767
 mov r10d,64
search:
 mov r8,rax
 shl r8,6
 lea r9,D5AM_sched_registry
 add r9,r8
 cmp [r9],r11
 je found
 cmp QWORD PTR [r9],0
 je missing
 inc rax
 and eax,32767
 dec r10d
 jnz search
 jmp missing
found:
 mov r8,[r9+8]
 mov [rsp+64],r8
 mov r8,[r9+16]
 mov [rsp+56],r8
 mov [rsp+72],rax
ENDM
gate MACRO unmatched
 mov rax,D5AM_sched_enabled
 cmp BYTE PTR [rax],0
 je unmatched
 cmp r11,10000h
 jb unmatched
 mov rax,[r11]
 cmp rax,D5AM_sched_vtables
 je @F
 cmp rax,D5AM_sched_vtables+8
 je @F
 cmp rax,D5AM_sched_vtables+16
 jne unmatched
@@:
ENDM
admission_probe MACRO phase
 LOCAL done
 cmp D5AM_sched_fixture_admission,0
 je done
 mov [rsp+96],r11
 save_ymm
 mov ecx,phase
 call QWORD PTR D5AM_sched_fixture_admission
 restore_ymm
 mov r11,[rsp+96]
done:
ENDM
enter_producer MACRO failed_label
 LOCAL core_held,bridge_held,rollback,admitted
 admission_probe 0
 mov [rsp+96],r11
 save_ymm
 mov rcx,D5AM_sched_core_active
 mov edx,1
 mov r8d,2
 xor r9d,r9d
 call D5AN_counter_next
 test al,al
 jnz core_held
 restore_ymm
 mov r11,[rsp+96]
 jmp failed_label
core_held:
 lea rcx,D5AM_sched_bridge_active
 mov edx,8
 mov r8d,3
 xor r9d,r9d
 call D5AN_counter_next
 test al,al
 jnz bridge_held
 restore_ymm
 mov r11,[rsp+96]
 jmp rollback
bridge_held:
 restore_ymm
 mov r11,[rsp+96]
 mov rax,D5AM_sched_enabled
 cmp BYTE PTR [rax],0
 jne admitted
 save_ymm
 lea rcx,D5AM_sched_bridge_active
 mov edx,8
 mov r8d,14
 call D5AN_counter_leave
 restore_ymm
rollback:
 save_ymm
 mov rcx,D5AM_sched_core_active
 mov edx,1
 mov r8d,15
 call D5AN_counter_leave
 restore_ymm
 jmp failed_label
admitted:
 admission_probe 1
ENDM
leave_producer MACRO
 save_ymm
 lea rcx,D5AM_sched_bridge_active
 mov edx,8
 mov r8d,14
 call D5AN_counter_leave
 restore_ymm
 save_ymm
 mov rcx,D5AM_sched_core_active
 mov edx,1
 mov r8d,15
 call D5AN_counter_leave
 restore_ymm
ENDM
invoke MACRO stage
 save_ymm
 mov rcx,[rsp+80]
 mov edx,stage
 mov r8,[rsp+88]
 lea r9,[rsp+32]
 call D5AM_sched_capture_admitted
 restore_ymm
ENDM

PUBLIC D5AM_sched_activated
D5AM_sched_activated PROC FRAME
 mov [rsp+8],rbx
 save_frame
 mov r11,[rsp+672]
 cmp r11,10000h
 jb activated_done
 mov r11,[r11]
 gate activated_done
 mov rax,[rsp+680]
 mov rax,[rax]
 mov [rsp+88],rax
 enter_producer activated_done
 copy_cookie activated_capture
activated_capture:
 invoke 2
 leave_producer
activated_done:
 restore_frame
 jmp QWORD PTR D5AM_sched_falls
D5AM_sched_activated ENDP

PUBLIC D5AM_sched_dispatch
D5AM_sched_dispatch PROC FRAME
 mov [rsp+10h],rbx
 save_frame
 mov r11,[rsp+672]
 gate dispatch_done
 mov rax,[rsp+680]
 mov [rsp+88],rax
 enter_producer dispatch_done
 copy_cookie dispatch_capture
dispatch_capture:
 save_ymm
 mov rcx,[rsp+80]
 mov rdx,[rsp+88]
 lea r8,[rsp+32]
 mov r9,[rsp+664]
 call D5AM_sched_dispatch_admitted
 restore_ymm
 leave_producer
dispatch_done:
 restore_frame
 jmp QWORD PTR D5AM_sched_falls+8
D5AM_sched_dispatch ENDP

PUBLIC D5AM_sched_retire
D5AM_sched_retire PROC FRAME
 mov [rsp+8],rbx
 save_frame
 mov r11,[rsp+672]
 gate retire_done
 mov QWORD PTR [rsp+88],0
 enter_producer retire_done
 copy_cookie retire_capture
retire_capture:
 invoke 4
 leave_producer
retire_done:
 restore_frame
 jmp QWORD PTR D5AM_sched_falls+16
D5AM_sched_retire ENDP

PUBLIC D5AM_sched_ready
D5AM_sched_ready PROC FRAME
 save_frame
 mov r11,[rsp+672]
 gate ready_done
 mov rax,[rsp+680]
 sub rax,38h
 mov [rsp+88],rax
 enter_producer ready_done
 copy_cookie ready_capture
ready_capture:
 ; Read the actual tree serial once, exactly as the native MOV R9,[RCX+50].
 ; Its saved R9 survives hostile callbacks. R11 is native RSP, so the other
 ; displaced MOV below writes the native stack slot, not a node field.
 mov rax,[rsp+680]
 mov r9,[rax+50h]
 mov [rsp+656],r9
 save_ymm
 mov rcx,[rsp+80]
 mov rdx,[rsp+88]
 lea r8,[rsp+32]
 mov r9,[rsp+656]
 call D5AM_sched_ready_admitted
 restore_ymm
 leave_producer
 restore_frame
 mov [r11+8],rdx
 ret
ready_done:
 restore_frame
 mov r9,[rcx+50h]
 mov [r11+8],rdx
 ret
D5AM_sched_ready ENDP

PUBLIC D5AM_sched_dependency
D5AM_sched_dependency PROC FRAME
 save_frame
 mov r11,[rsp+688]
 gate dependency_unwatched
 mov QWORD PTR [rsp+88],0
 enter_producer dependency_unwatched
 copy_cookie dependency_operation
dependency_operation:
 mov r11,[rsp+80]
 add DWORD PTR [r11+90h],-1
 pushfq
 pop QWORD PTR [rsp+696]
 invoke 6
 leave_producer
 jmp dependency_done
dependency_unwatched:
 mov r11,[rsp+688]
 add DWORD PTR [r11+90h],-1
 pushfq
 pop QWORD PTR [rsp+696]
dependency_done:
 restore_frame
 ret
D5AM_sched_dependency ENDP

PUBLIC D5AM_sched_command
D5AM_sched_command PROC FRAME
 save_frame
 mov QWORD PTR [rsp+688],0
 mov r11,[rsp+672]
 test r11,r11
 jz command_done
 mov r11,[r11]
 and r11,-2
 test r11,r11
 jz command_done
 mov rax,[r11+8]
 cmp rax,D5AM_sched_callback_target
 jne command_done
 save_ymm
 mov rcx,[rsp+680]
 mov rdx,[rsp+672]
 mov r8,[rsp+664]
 mov r9,[rsp+656]
 mov rax,[rsp+752]
 mov [rsp+32],rax
 call D5AM_sched_command_capture
 movzx eax,al
 mov [rsp+688],rax
 restore_ymm
command_done:
 restore_frame
 ret
D5AM_sched_command ENDP

; Function-level native interfaces return only an integer/pointer. Preserve all
; incoming vector state and flags around the ABI-conforming proxy as well as
; returning its actual RAX. The original helpers are still called exactly once.
PUBLIC D5AM_sched_claim_entry
D5AM_sched_claim_entry PROC FRAME
 save_frame
 save_ymm
 mov rcx,[rsp+680]
 mov rdx,[rsp+672]
 mov r8,[rsp+664]
 mov r9,[rsp+656]
 mov rax,[rsp+752]
 mov [rsp+32],rax
 call D5AM_sched_claim_proxy
 mov [rsp+688],rax
 restore_ymm
 restore_frame
 ret
D5AM_sched_claim_entry ENDP

PUBLIC D5AM_sched_queue_entry
D5AM_sched_queue_entry PROC FRAME
 save_frame
 save_ymm
 mov rcx,[rsp+680]
 mov rdx,[rsp+672]
 mov r8,[rsp+664]
 mov r9,[rsp+656]
 call D5AM_sched_queue_proxy
 mov [rsp+688],rax
 restore_ymm
 restore_frame
 ret
D5AM_sched_queue_entry ENDP
END
