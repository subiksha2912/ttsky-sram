# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Starting Memory Test")

    # -------------------------
    # CLOCK
    # -------------------------
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # -------------------------
    # RESET
    # -------------------------
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("Reset Done")

    # -------------------------
    # TEST PARAMETERS
    # -------------------------
    addr = 2
    data = 55

    # -------------------------
    # WRITE OPERATION
    # -------------------------
    dut._log.info(f"Writing data={data} to addr={addr}")

    # valid=1, wr_rd=1 (write), addr in bits [3:2]
    dut.ui_in.value = (addr << 2) | (1 << 1) | 1
    dut.uio_in.value = data

    # Hold write for enough cycles (important for gate-level)
    await ClockCycles(dut.clk, 2)

    # Small gap (stabilization)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 1)

    # -------------------------
    # READ OPERATION
    # -------------------------
    dut._log.info(f"Reading from addr={addr}")

    # valid=1, wr_rd=0 (read)
    dut.ui_in.value = (addr << 2) | (0 << 1) | 1
    dut.uio_in.value = 0

    # Wait for pipeline + gate delay
    await ClockCycles(dut.clk, 3)

    read_data = int(dut.uio_out.value)

    dut._log.info(f"Read data = {read_data}")

    # -------------------------
    # CHECK
    # -------------------------
    assert read_data == data, f"FAIL: expected {data}, got {read_data}"

    dut._log.info("Memory Test PASSED ✅")
