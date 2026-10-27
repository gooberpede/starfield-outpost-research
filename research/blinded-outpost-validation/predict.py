# SPDX-License-Identifier: GPL-3.0-or-later
"""Location-only research runner; reads provisioned location/policy, writes JSON.

No raw save, extractor catalogue or native result is an input. The generic
effective-centre conversion is unqualified, so this version fails closed with
UNKNOWN for all three candidate bodies. conditional.py separately exercises
unchanged geometry on qualified historical/synthetic source contexts. Stdlib.
"""
import json
from bridge import validate


def predict(location):
    validate(location)
    return dict(schema='sor-blind-prediction/1', trial=location['trial'],
        body=location['body'], body_formid=location['body_formid'], workshop=location['workshop'],
        location=location, classification='UNSUPPORTED',
        reason='MISSING_EFFECTIVE_WORKSHOP_FRAME_AND_COMPLETE_CANDIDATE_CORPUS',
        sources=[], presence={}, special_helium3='UNKNOWN', terrestrial_water='UNKNOWN',
        atmospheric='UNKNOWN', scope_complete=False)


if __name__ == '__main__':
    from bridge import loads
    with open('../input/location.json', encoding='utf8') as stream:
        result = predict(loads(stream.read()))
    with open('prediction.json', 'x', encoding='utf8') as stream:
        json.dump(result, stream, sort_keys=True, separators=(',', ':'), allow_nan=False)
        stream.write('\n')
