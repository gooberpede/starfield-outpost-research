# SPDX-License-Identifier: GPL-3.0-or-later
"""Required synthetic qualification roster; pure data, no effects."""
MODES = ['mask0', 'mask3', 'conflict', 'combined', 'linked', 'linked-reuse', 'linked-reset',
        'wrong-key', 'wrong-owner', 'wrong-query', 'partial-dnam', 'nested', 'threads',
        'injected-context-failure', 'no-hit', 'crash-before', 'crash-after',
        'cache-multi', 'cache-wrong-workshop', 'cache-wrong-body', 'cache-wrong-resource',
        'cache-unrelated-source', 'cache-stale-transfer', 'cache-pointer-reuse',
        'cache-source-reuse', 'cache-contention', 'cache-nested', 'cache-partial-page',
        'cache-corrupt', 'cache-nonfinite', 'cache-stop-many', 'ackfail', 'dropped-ack', 'kill-before-ack', 'empty-generation', 'cache-empty-transfer', 'ackfail-return']
