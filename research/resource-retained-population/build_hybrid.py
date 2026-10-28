# SPDX-License-Identifier: GPL-3.0-or-later
"""Build the D5N hybrid using installed MSVC and owned D5M build methods.

Reads the D5M source closure and hybrid.py; writes fresh ignored generated
sources, binaries, logs and build pins. Executes build tools only. No network,
installation, game/save/analysis changes or Git mutations. Both disk floors apply.
"""
import build_native
import hybrid

# The build keeps its existing closure/hash logic. The two adapted translation
# units are written into the fresh build; historical sources remain unchanged.
source = hybrid.replace((hybrid.SRC/'build_native.py').read_text(encoding='utf8'),
    "generated.write_text(controller_source(inherited), encoding='utf8', newline='\\n')",
    "generated.write_text(controller_source(inherited), encoding='utf8', newline='\\n')\n"
    "    (out/'native-fixture.cpp').write_text(hybrid.fixture((SRC/'native-fixture.cpp').read_text()), encoding='utf8', newline='\\n')")
source = source.replace('SRC/"native-fixture.cpp"', 'out/"native-fixture.cpp"')
source = source.replace("SRC/'native-fixture.cpp']", "out/'native-fixture.cpp']")
namespace = dict(__name__='d5n_build', __file__=str(hybrid.SRC/'build_native.py'), hybrid=hybrid)
exec(compile(source, namespace['__file__']+'[D5N adapted]', 'exec'), namespace)
original = namespace['controller_source']
namespace['controller_source'] = lambda inherited: hybrid.controller(original(inherited))

if __name__ == '__main__':
    raise SystemExit(namespace['main']())
