; SPDX-License-Identifier: GPL-3.0-or-later
; Exact CALL17DF4E2: RDI selected native ref, RSI selected operation record.
; Preserve all ABI channels; copy those nonvolatile inputs to observation-only
; stack arguments. No stolen instructions or return-address substitution.
.code
EXTERN producer_hook:PROC
PUBLIC producer_bridge
producer_bridge PROC FRAME
 sub rsp,38h
 .allocstack 38h
 .endprolog
 mov [rsp+20h],rdi
 mov [rsp+28h],rsi
 call producer_hook
 add rsp,38h
 ret
producer_bridge ENDP
END
