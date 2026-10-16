// SPDX-License-Identifier: GPL-3.0-or-later
// Diagnostic-only extension of the owned disposable baseline.
#pragma once
extern unsigned diagnostic_condition, diagnostic_requested;
extern "C" LONG CALLBACK entry_handler(EXCEPTION_POINTERS*);
void diagnostic_open(int, char**);
void diagnostic_write(const unsigned char*, unsigned, unsigned);
void diagnostic_close();
