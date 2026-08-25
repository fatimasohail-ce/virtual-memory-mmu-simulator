# 32-bit Virtual Memory & MMU Simulator

A Python-based simulator that demonstrates the operation of a 32-bit virtual memory system and Memory Management Unit (MMU).

## Overview

This project simulates the process of translating virtual addresses into physical addresses using virtual memory concepts.

The simulator models virtual memory page accesses and compares different page replacement algorithms by tracking page faults for a given memory access trace.

## Features

- 32-bit virtual address trace simulation
- Page-based memory management
- FIFO page replacement
- LRU page replacement
- Optimal (OPT) page replacement
- Page fault counting
- Configurable RAM frame count
- Trace-based memory access simulation
- Belady's anomaly testing for FIFO

## Technologies Used

- Python
- Operating Systems concepts
- Virtual Memory
- Page Replacement Algorithms
- FIFO
- LRU
- Optimal (OPT)
- Belady's Anomaly

## Project Structure

```text
.
├── mmu_sim.py
├── config.json
├── trace.txt
└── 32 bit VM mmu.pdf
