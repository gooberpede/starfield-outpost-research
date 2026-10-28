# SPDX-License-Identifier: GPL-3.0-or-later
"""Run the D5N disposable matrix in three independent batches.

Reads an exact build and owned qualify_parallel method; writes fresh ignored
batch receipts and hash-verified aggregate copies. Runs only qualify_hybrid.py
on disposable sibling targets, with its documented debug/disposal effects.
No retail, network, installation, protected inputs, analysis or Git mutation.
"""
import hybrid
import qualify_hybrid

source=(hybrid.SRC/'qualify_parallel.py').read_text(encoding='utf8')
source=hybrid.replace(source, "with_name('qualify_native.py')", "with_name('qualify_hybrid.py')")
namespace=dict(__name__='d5n_parallel', __file__=str(hybrid.SRC/'qualify_parallel.py'))
exec(compile(source, namespace['__file__']+'[D5N adapted]', 'exec'), namespace)
namespace['MODES']=qualify_hybrid.namespace['MODES']

if __name__ == '__main__':
    raise SystemExit(namespace['main']())
