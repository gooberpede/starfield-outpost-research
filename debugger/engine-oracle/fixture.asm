; SPDX-License-Identifier: GPL-3.0-or-later
; Synthetic register-layout bridge. Saves/restores all touched nonvolatile state.
.code
OracleCheckpoint proc
    push rbx
    push rsi
    push rbp
    sub rsp, 20h
    mov rbx, rcx
    mov rsi, rdx
    mov rbp, r8
    call OracleMarker
    add rsp, 20h
    pop rbp
    pop rsi
    pop rbx
    ret
OracleCheckpoint endp
OracleMarker proc
    nop
    ret
OracleMarker endp
end
