# -*- coding: utf-8 -*-
#
# This file is part of the pyFDA project hosted at https://github.com/chipmuenk/pyfda
#
# Copyright © pyFDA Project Contributors
# Licensed under the terms of the MIT License
# (see file LICENSE in root directory for details)
#
# Taken from https://github.com/sriyash25/filter-blocks
# (c) Christopher Felton and Sriyash Caculo

import pytest
import myhdl as hdl
from myhdl import Signal, intbv, StopSimulation, delay, traceSignals, ResetSignal

from pyfda.filter_blocks.support import Clock, Reset, Global, Samples
from pyfda.filter_blocks.iir import iir_parallel
#from pyfda.filter_blocks.fda.iir import FilterIIR


# TODO: fix these, they should not be failing!
@hdl.block
def test_iir_api():
    
    clock = Clock(0, frequency=50e6)
    reset = Reset(1, active=0, async=True)
    glbl = Global(clock, reset)
    tbclk = clock.process()

    w = (24,0,23)
    w_out = (24,0,23)
        
    ymax = 2**(2*w[0]-1)
    vmax = 2**(2*w[0])
    omax = 2**(w_out[0]-1)

    xt = Samples(min=-ymax, max=ymax, word_format = w)
    yt = Samples(min=-omax, max=omax, word_format = w_out)

    b = [[101, 0, 132], [23324, 0, 232]]
    a = [[24223, 1], [233, 0]]
    w = (24, 23, 0)

    #iir_test = FilterIIR(b, a)

    iir = iir_parallel.filter_iir_parallel(glbl, xt, yt, b, a, w)


    return hdl.instances()


@pytest.mark.xfail
def notest_iir_par_sim(): # this test stalls the test suite
    tb = traceSignals(test_iir_api())
    tb.run_sim()

    # tb = test_iir_parallel()
    # tb.run_sim()


if __name__ == '__main__':
    test_iir_par_sim()

