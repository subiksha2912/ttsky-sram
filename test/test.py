# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Starting Memory Test")

    # Start clock (10us period)
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
    # TEST: WRITE + READ
    # -------------------------
    addr = 2
    data = 55

    dut._log.info(f"Writing data={data} to addr={addr}")

    # WRITE
    # ui_in:
    # bit0 = valid
    # bit1 = wr_rd (1 = write)
    # bits[3:2] = addr
    dut.ui_in.value = (addr << 2) | (1 << 1) | 1
    dut.uio_in.value = data

    await ClockCycles(dut.clk, 1)

    # small gap (important for pipeline stability)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 1)

    # -------------------------
    # READ
    # -------------------------
    dut._log.info(f"Reading from addr={addr}")

    dut.ui_in.value = (addr << 2) | (0 << 1) | 1
    dut.uio_in.value = 0

    # wait for memory latency (1 cycle pipeline)
    await ClockCycles(dut.clk, 2)

    read_data = int(dut.uio_out.value)

    dut._log.info(f"Read data = {read_data}")

    # -------------------------
    # CHECK
    # -------------------------
    assert read_data == data, f"FAIL: expected {data}, got {read_data}"

    dut._log.info("Memory Test PASSED ✅")
