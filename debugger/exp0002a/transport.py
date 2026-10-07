# SPDX-License-Identifier: GPL-3.0-or-later
"""Original x64dbg headless command transport (standard library only).

Launches the supplied installed headless.exe with an isolated user directory.
Does not itself attach or start a debuggee. Commands supplied by its caller can
intervene in execution. Records stdout incrementally with fsync in a create-new
local file. Never kills the debugger or debuggee; caller must verify detach
before exit. Command acknowledgment confirms queue processing, not semantics.
"""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time


class Transport:
    def __init__(self, debugger, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=False)
        user = self.root/'user'
        user.mkdir()
        # Fresh isolated settings must not insert unrelated TLS/DLL/thread
        # breakpoints. Default TlsCallbacks=1 was observed in manual-002.
        (user/'headless.ini').write_text(
            '[Events]\nTlsCallbacks=0\nTlsCallbacksSystem=0\nDllEntry=0\n'
            'DllEntrySystem=0\nDllLoad=0\nDllLoadSystem=0\n'
            'ThreadEntry=0\nThreadStart=0\n', encoding='utf-8')
        self.events = queue.Queue()
        self.lines = []
        self.error = None
        self.sequence = 0
        self.bytes = 0
        self.stream = (self.root/'transport.jsonl').open('x', encoding='utf-8', newline='\n')
        self.process = subprocess.Popen([str(debugger), '-userdir', str(user.resolve())],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, text=True,
                                        encoding='utf-8', errors='replace', bufsize=1)
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()
        self.wait('Handling command line...', 20)

    def _read(self):
        try:
            for line in self.process.stdout:
                self.bytes += len(line.encode('utf-8'))
                if self.bytes > 2_000_000 or len(line) > 32768:
                    self.error = 'output_bound'
                    # Continue draining, without storing an unbounded stream.
                    continue
                record = {'utc': datetime.now(timezone.utc).isoformat(), 'text': line.rstrip('\n')}
                self.stream.write(json.dumps(record)+'\n')
                self.stream.flush()
                # Persist evidence and command boundaries, not every verbose
                # symbol-loader line: per-line disk sync there can starve the
                # command channel before arming. All preceding text is included.
                if line.startswith(('SOR_', '[FAIL]')):
                    os.fsync(self.stream.fileno())
                self.lines.append(line)
                self.events.put(line)
        except Exception as error:
            self.error = repr(error)

    def send(self, command):
        if '\n' in command or '\r' in command:
            raise ValueError('One command per write')
        self.process.stdin.write(command+'\n')
        self.process.stdin.flush()

    def wait(self, marker, seconds=5):
        deadline = time.monotonic()+seconds
        seen = []
        while time.monotonic() < deadline:
            if self.error:
                raise RuntimeError(self.error)
            try:
                line = self.events.get(timeout=.05)
                seen.append(line)
                if marker in line:
                    return seen
            except queue.Empty:
                if self.process.poll() is not None:
                    raise RuntimeError('Debugger exited before marker: '+marker)
        raise TimeoutError(marker)

    def command(self, command, seconds=5):
        self.sequence += 1
        marker = f'SOR_ACK_{self.sequence:06d}'
        self.send(command)
        self.send(f'log "{marker}"')
        seen = self.wait(marker, seconds)
        if any('[FAIL]' in line or 'Unknown command' in line or 'Invalid expression' in line or 'is debug-only' in line for line in seen):
            raise RuntimeError('Debugger rejected command: '+command)
        return seen

    def exit_detached(self):
        """Only call after independently verifying no debuggee remains attached."""
        self.send('exit')
        self.process.wait(timeout=10)
        self.reader.join(timeout=10)
        if self.reader.is_alive():
            raise RuntimeError('Output drain incomplete; log retained')
        self.stream.flush()
        os.fsync(self.stream.fileno())
        self.stream.close()
