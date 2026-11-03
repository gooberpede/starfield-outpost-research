; SPDX-License-Identifier: GPL-3.0-or-later
; Independent caller and hostile callback for the exact D5AM bridge object.
option casemap:none
EXTERN D5AM_pending:PROC
EXTERN D5AM_acquired:PROC
EXTERN D5AM_recursive:PROC
EXTERN D5AM_reader:PROC
EXTERN D5AM_reader_release:PROC
EXTERN D5AM_writer_release:PROC
EXTERN D5AM_recursive_release:PROC
EXTERN D5AM_reader_ready:PROC
EXTERN D5AM_inline_writer_release:PROC
EXTERN D5AM_inline_recursive_release:PROC
EXTERN D5AM_record:PROC
.code
D5AM_capture PROC FRAME
 sub rsp,56
 .allocstack 56
 .endprolog
 mov rax,[rsp+96]
 mov [rsp+32],rax
 mov rax,[rsp+104]
 mov [rsp+40],rax
 call D5AM_record
 add rsp,56
 mov rax,1
 mov rcx,2
 mov rdx,3
 mov r8,4
 mov r9,5
 mov r10,6
 mov r11,7
 pxor xmm0,xmm0
 pxor xmm1,xmm1
 pxor xmm2,xmm2
 pxor xmm3,xmm3
 pxor xmm4,xmm4
 pxor xmm5,xmm5
 clc
 ret
D5AM_capture ENDP
probe MACRO name,target,kind
name PROC FRAME
 push rbp
 .pushreg rbp
 push rbx
 .pushreg rbx
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
 sub rsp,188h
 .allocstack 188h
 .endprolog
 mov r15,rcx
 mov [r15+224],rsp
 mov r14,rdx
 lea rdi,[rdx+4]
 mov QWORD PTR [rsp+38h],7777h
 mov rbp,4545h
 mov rax,101h
 mov rcx,102h
 mov rdx,103h
 mov r8,108h
 mov r9,109h
 mov r10,110h
 mov r11,111h
 mov rbx,7000h
 mov rsi,6161h
 mov r12,1212h
 mov r13,1313h
 IF kind EQ 2
  mov eax,1000h
 ELSEIF kind EQ 3
  mov eax,1000h
 ELSEIF kind EQ 4
  mov esi,400000h
 ELSEIF kind EQ 5
  mov eax,1
 ELSEIF kind EQ 6
  mov rcx,rdi
  mov edx,0ffffffffh
 ELSEIF kind EQ 7
  mov rcx,rdi
  mov eax,0ffbff000h
 ELSEIF kind EQ 8
  mov rcx,rdi
  mov eax,0ffc00000h
 ELSEIF kind EQ 17
  mov rdi,r14
  mov ecx,0ffbff000h
 ELSEIF kind EQ 18
  mov rdi,r14
  mov ecx,0ffc00000h
 ENDIF
 pcmpeqd xmm0,xmm0
 pcmpeqd xmm1,xmm1
 pcmpeqd xmm2,xmm2
 pcmpeqd xmm3,xmm3
 pcmpeqd xmm4,xmm4
 pcmpeqd xmm5,xmm5
 stc
 IF (kind EQ 7) OR (kind EQ 8)
  lea rsp,[rsp-8]
 ENDIF
 PUBLIC name&_site
name&_site LABEL BYTE
 call target
 IF (kind EQ 7) OR (kind EQ 8)
  lea rsp,[rsp+8]
 ENDIF
 mov [r15],rax
 mov [r15+8],rcx
 mov [r15+16],rdx
 mov [r15+24],r8
 mov [r15+32],r9
 mov [r15+40],r10
 mov [r15+48],r11
 mov [r15+56],rbx
 mov [r15+64],rdi
 mov [r15+72],r12
 mov [r15+80],r13
 mov [r15+88],r14
 mov [r15+96],r15
 mov [r15+104],rbp
 pushfq
 pop rax
 mov [r15+112],rax
 movdqu [r15+128],xmm0
 movdqu [r15+144],xmm1
 movdqu [r15+160],xmm2
 movdqu [r15+176],xmm3
 movdqu [r15+192],xmm4
 movdqu [r15+208],xmm5
 mov [r15+240],rsp
 mov [r15+248],rsi
 mov rsp,[r15+224]
 add rsp,188h
 pop r15
 pop r14
 pop r13
 pop r12
 pop rdi
 pop rsi
 pop rbx
 pop rbp
 ret
name ENDP
ENDM
probe d5am_probe_pending,D5AM_pending,2
probe d5am_probe_acquired,D5AM_acquired,3
probe d5am_probe_recursive,D5AM_recursive,4
probe d5am_probe_reader,D5AM_reader,5
probe d5am_probe_reader_release,D5AM_reader_release,6
probe d5am_probe_writer_release,D5AM_writer_release,7
probe d5am_probe_recursive_release,D5AM_recursive_release,8
probe d5am_probe_reader_ready,D5AM_reader_ready,15
probe d5am_probe_inline_writer_release,D5AM_inline_writer_release,17
probe d5am_probe_inline_recursive_release,D5AM_inline_recursive_release,18
END
