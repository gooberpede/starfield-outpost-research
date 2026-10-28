# SPDX-License-Identifier: GPL-3.0-or-later
"""Frozen D5M real-process cases required by prospective offline preparation.

Constants only. Does not run tests, authorize a target or perform file I/O.
"""
MODES = (
    'basic','reuse','reset','owner-aba','reset-window','destroy-window','grid-window',
    'source-window','query-change-hit','alternate-frame','failed','copy-failed',
    'partial','prereq','concurrent','nested','bad-read','crash','stop','pre-arm-stop',
    'step-stop','bad-ack','guard-loss','defer-peer','new-peer-step','exception',
    'contrary','early-exit','grid-stress','continue-failure','duplicate-failure',
    'close-failure','readback-failure','foreign-first','foreign-last','exit-peer-step',
    'duplicate-diagnostic-failure','close-diagnostic-failure',
    'cleanup-close-diagnostic-failure',
    'post-close-diagnostic-failure',
    'queued-same','queued-different',
)
