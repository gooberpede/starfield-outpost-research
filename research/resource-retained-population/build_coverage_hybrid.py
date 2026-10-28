# SPDX-License-Identifier: GPL-3.0-or-later
"""Build D5O using installed MSVC; writes fresh ignored source/tool/build pins.

No targets, downloads, protected inputs or Git writes. Reuses owned D5N build
method under SOR-P-0002, substituting only the bounded D5O adapters.
"""
import build_hybrid
import coverage_hybrid

build_hybrid.namespace['controller_source'] = lambda inherited: coverage_hybrid.controller(
    build_hybrid.original(inherited))
build_hybrid.namespace['hybrid'] = coverage_hybrid

if __name__ == '__main__':
    raise SystemExit(build_hybrid.namespace['main']())
