#!/usr/bin/env python3
"""
High-level tests for the overall functionallity and things in kc.py
"""
import sys
import os
from io import StringIO

sys.path.insert(0, '..')
from kerncraft import kerncraft as kc


def _find_file(name):
    testdir = os.path.dirname(__file__)
    name = os.path.join(testdir, 'test_files', name)
    assert os.path.exists(name)
    return name


output_stream = StringIO()

parser = kc.create_parser()
args = parser.parse_args(['-m', _find_file('phinally_gcc.yaml'),
                          '-p', 'ECMData',
                          _find_file('2d-5pt.c'),
                          '-D', 'N', '2000',
                          '-D', 'M', '2000',
                          '-vvv', ])
kc.check_arguments(args, parser)
kc.run(parser, args, output_file=output_stream)
