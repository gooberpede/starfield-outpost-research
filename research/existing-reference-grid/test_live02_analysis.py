# SPDX-License-Identifier: GPL-3.0-or-later
"""Supplemental lifetime controls; synthetic records only, no game access."""
import copy
import unittest
from live02_analysis import diagnostic_lifetimes


def example():
    return [dict(sequence=s,kind=k,invocation=i,parent=p,thread=1,reference=2,context=3,qpc=s)
            for s,k,i,p in [(1,7,1,0),(2,20,1,0),(3,10,2,1),(4,11,2,1),(5,8,1,0)]]


class LifetimeTests(unittest.TestCase):
    def test_complete_auxiliary_Q_and_nested_E(self):
        self.assertEqual(diagnostic_lifetimes(example())['E_normal'],1)

    def test_Q_without_E(self):
        e=example();self.assertTrue(diagnostic_lifetimes([e[0],e[-1]])['diagnostic_lifetimes_complete'])

    def test_missing_or_unwound_E_fails(self):
        for remove in (True,False):
            e=example()
            if remove:e.pop(3)
            else:e[3]['kind']=12
            with self.assertRaises(ValueError):diagnostic_lifetimes(e)

    def test_duplicate_entry_fails(self):
        e=example();e.insert(2,copy.deepcopy(e[1]))
        with self.assertRaises(ValueError):diagnostic_lifetimes(e)

    def test_identity_and_thread_corruption_fail(self):
        for at in (1,2):
            e=example();e[at]['thread']=7
            with self.assertRaises(ValueError):diagnostic_lifetimes(e)

    def test_outside_window_fails(self):
        for field in ('sequence','qpc'):
            e=example();e[2][field]=6;e[3][field]=7
            with self.assertRaises(ValueError):diagnostic_lifetimes(e)


if __name__=='__main__':unittest.main()
