#!/usr/bin/env python
#
# Copyright 2011 Communications Engineering Lab, KIT
#
# This file is part of the GNU Radio Spectral Estimation Toolbox
#
# The GNU Radio Spectral Estimation Toolbox is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# The GNU Radio Spectral Estimation Toolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio Spectral Estimation Toolbox; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Start our unittests')
    parser.add_argument('--path', help = 'sets the PYTHONPATH for the test')
    parser.add_argument('--test', help = 'sets the filename containing the tests to run')
    args = parser.parse_args()
    python_path = {"PYTHONPATH" : args.path}
    return subprocess.call(args=args.test, env=python_path)

if __name__ == '__main__':
    main()
