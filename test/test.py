# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start Memory Test")

    # Clock
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    dut._log.info("Writing to memory")

    # -------------------------
    # WRITE: addr=2, data=55
    # ui_in mapping:
    # bit0 = valid
    # bit1 = wr_rd (1 = write)
    # bits[3:2] = addr
    # -------------------------

    addr = 2
    data = 55

    dut.ui_in.value = (addr << 2) | (1 << 1) | 1  # valid=1, wr_rd=1
    dut.uio_in.value = data

    await ClockCycles(dut.clk, 1)

    # -------------------------
    # READ: addr=2
    # -------------------------

    dut._log.info("Reading from memory")

    dut.ui_in.value = (addr << 2) | (0 << 1) | 1  # valid=1, wr_rd=0
    dut.uio_in.value = 0

    await ClockCycles(dut.clk, 2)  # read is 1-cycle delayed

    read_data = int(dut.uio_out.value)

    dut._log.info(f"Read data = {read_data}")

    # Check result
    assert read_data == data, f"Memory read failed: expected {data}, got {read_data}"

    dut._log.info("Memory test passed ✅")
