# SPDX-License-Identifier: GPL-3.0-or-later
"""Test D5N's adapted admission against real offline metadata only.

Reads a completed hybrid preflight and inherited owned admission controls;
writes one fresh local results JSON. Approval-shaped controls stay in memory.
Never starts a target, calls collection, emits GO, changes configuration,
downloads dependencies or mutates Git.
"""
import hybrid
import operate_hybrid

source=(hybrid.SRC/'check_admission.py').read_text(encoding='utf8')
source=hybrid.replace(source, "['software_int3_14','all_stop_and_peer_suspend'",
    "['software_int3_13','hardware_dr0_grid_clear','all_stop_and_peer_suspend'")
source=hybrid.replace(source, "    refuse('expanded_interventions'", """    refuse('old_fourteen_software_gate',lambda g:g.update(allowed_interventions=['software_int3_14','all_stop_and_peer_suspend','owned_rip_tf_rearm','termination_teardown']))
    refuse('missing_hardware_authority',lambda g:g['allowed_interventions'].remove('hardware_dr0_grid_clear'))
    refuse('expanded_interventions'""")
namespace=dict(__name__='d5n_admission_tests',__file__=str(hybrid.SRC/'check_admission.py'))
exec(compile(source,namespace['__file__']+'[D5N adapted]','exec'),namespace)
namespace['admission_checks']=operate_hybrid.module('collect_native')['admission_checks']

if __name__=='__main__':
    namespace['main']()
