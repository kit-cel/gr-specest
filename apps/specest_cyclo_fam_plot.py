#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# Copyright 2011 Communications Engineering Lab, KIT
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
"""
Plots the magnitude of the spectral correlation density
(cyclic spectrum) of a file estimated with FAM.

"""

from optparse import OptionParser
from gnuradio.eng_option import eng_option
from specest import fam_matplotlib


def parse_options():
    """ Options parser. """
    usage = "%prog: [options] filename"
    parser = OptionParser(option_class=eng_option, usage=usage)
    parser.add_option("-s", "--sample-type", type="choice",
                      choices=("float", "complex"),
                      help="Set input type to float or complex.", default="complex")
    parser.add_option("-N", "--Np", type="int", default=32,
            help="N' (not N!)")
    parser.add_option("-P", type="int", default=128,
            help="P")
    parser.add_option("-L", default=2,
            help="L")
    (options, args) = parser.parse_args ()
    if len(args) != 1:
        return (options, None)
    return (options, args[0])

def main():
    """ Setup plot widget and run. """
    (options, filename) = parse_options()
    fam_matplotlib.setup_fam_matplotlib(filename=filename,
                                        Np=options.Np, P=options.P, L=options.L,
                                        sample_type=options.sample_type,
                                        verbose=True)

if __name__ == "__main__":
    main()

