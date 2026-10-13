"""SPDX-License-Identifier: GPL-3.0-or-later
Isolated scalar contracts, not a saved-to-loaded Z predictor.
Reads caller-supplied operands only; returns values/UNKNOWN; no I/O, dependencies
outside stdlib, process access or analysis-project effects. Native provenance:
docs/experiments/workshop-z-restoration/report.md. Does not select loader paths.
Finite normal/zero binary32, round-to-nearest only; unobserved CPU modes excluded.
"""
import math
import struct


def f32(value):
    try:
        value = struct.unpack('<f', struct.pack('<f', value))[0]
    except OverflowError as error:
        raise ValueError('UNQUALIFIED_FLOAT_DOMAIN') from error
    if not math.isfinite(value) or 0 < abs(value) < 2**-126:
        raise ValueError('UNQUALIFIED_FLOAT_DOMAIN')
    return value


def known(value, operation):
    return dict(status='KNOWN_SCALAR_OPERATION', z=f32(value),
                z_hex=struct.pack('<f', value).hex(), operation=operation)


def unknown(*fields):
    return dict(status='UNKNOWN', missing=list(fields))


def center_z(reference_z, compensation_xyz):
    """140f4ab80: ALL three components control zero bypass, then Z VADDSS."""
    if reference_z is None or compensation_xyz is None:
        return unknown('reference_z', 'compensation_xyz')
    if len(compensation_xyz) != 3 or any(d is None for d in compensation_xyz):
        return unknown('complete_compensation_xyz')
    z = f32(reference_z)
    delta = tuple(f32(d) for d in compensation_xyz)
    return known(z if all(d == 0 for d in delta) else f32(delta[2] + z),
                 'workshop-center')


def convert_z(reference_z, flag_byte, target_bit, translation_z=None):
    """140b734c0 -> 140b73310; translation already has its native sign.
    Bit02 transition is required. This function does not infer a selected edge,
    parent, target bit or conversion invocation from saved frame bytes.
    """
    if flag_byte is None or reference_z is None or target_bit is None:
        return unknown('reference_z', 'reference_d3', 'target_bit')
    if type(flag_byte) is not int or not 0 <= flag_byte <= 255:
        raise ValueError('INVALID_FLAG_BYTE')
    if type(target_bit) is not bool:
        raise ValueError('TARGET_BIT_REQUIRES_BOOL')
    z = f32(reference_z)
    transition = bool(flag_byte & 2) != target_bit
    if transition and translation_z is None:
        return unknown('signed_translation_z')
    if transition:
        z = f32(z + f32(translation_z))
    result = known(z, 'ordinary-reference-conversion')
    result.update(flag_byte=(flag_byte & 0xfd) | (2 if target_bit else 0),
                  transitioned=transition)
    return result


def prepared_z(reference_z, subtract_selected, selected_z=None):
    """141856d10: caller must qualify ALL world/status/validity/flag gates.
    None means gates unavailable. This is preparation, not proven actual restore.
    """
    if reference_z is None or subtract_selected is None:
        return unknown('reference_z', 'qualified_preparation_branch')
    if type(subtract_selected) is not bool:
        raise ValueError('BRANCH_REQUIRES_BOOL')
    z = f32(reference_z)
    if subtract_selected:
        if selected_z is None:
            return unknown('selected_edge_z')
        z = f32(z - f32(selected_z))
    return known(z, 'reference-frame-preparation')


def initial_load_z(saved_z, saved_frame, qualified_addition=None):
    """Case5 pre-construction scalar only, 141833c9f..4003.
    Saved20-clear bypasses both edge additions. For saved20-set a caller must
    independently qualify the applicable branch and its signed addition.
    This does not include subsequent placement/registration/position writes.
    """
    if saved_z is None or saved_frame is None:
        return unknown('saved_z', 'saved_frame')
    if saved_frame not in (0x0b, 0x2b):
        raise ValueError('UNQUALIFIED_SAVED_FRAME')
    if not saved_frame & 0x20:
        return known(f32(saved_z), 'initial-loader-edge-addition-bypassed')
    if qualified_addition is None:
        return unknown('qualified_load_branch_and_signed_addition')
    return known(f32(f32(saved_z) + f32(qualified_addition)),
                 'initial-loader-qualified-addition')


def restore_from_saved(saved_z, history=None):
    """No complete event history is available; never fit constants to outputs.
    Deliberately refuses even an arbitrary history object: no loader dispatcher
    or post-load writer ordering has been qualified for the captured events.
    """
    return unknown('load_branch_and_parent', 'post_load_writer_history',
                   'same_invocation_selected_edge_and_height')
