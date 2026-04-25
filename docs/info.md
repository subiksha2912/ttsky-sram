# Simple Synchronous Memory

## Description

This project implements a small synchronous memory that supports read and write operations using a valid-ready handshake mechanism.

## How it works

The design allows writing data into memory and reading it back using control signals.

* **valid (ui[0])** → Starts an operation
* **wr_rd (ui[1])** → Selects operation (1 = write, 0 = read)
* **addr (ui[3:2])** → Selects memory location
* **data (uio[7:0])** → Input/output data bus

### Operation:

* **Write:** When `valid=1` and `wr_rd=1`, data from `uio_in` is stored at the given address.
* **Read:** When `valid=1` and `wr_rd=0`, data is returned from memory after one clock cycle.

## Inputs

| Pin   | Name  | Description         |
| ----- | ----- | ------------------- |
| ui[0] | valid | Start operation     |
| ui[1] | wr_rd | 1 = write, 0 = read |
| ui[2] | addr0 | Address bit 0       |
| ui[3] | addr1 | Address bit 1       |

## Outputs

| Pin     | Name  | Description        |
| ------- | ----- | ------------------ |
| uo[0]   | ready | Operation complete |
| uo[7:1] | rdata | Partial read data  |

## Bidirectional Pins

| Pin      | Name | Description                                   |
| -------- | ---- | --------------------------------------------- |
| uio[7:0] | data | Used for both input (write) and output (read) |

## Features

* 4-word memory (2-bit address)
* 8-bit data width
* 1-cycle latency for read operations
* Simple handshake interface

## Test Strategy

The design is verified using cocotb by:

* Writing data to memory
* Reading it back
* Checking correctness

## Applications

* Basic memory blocks in digital systems
* Data buffering
* Learning memory design concepts

## Author

Subiksha
