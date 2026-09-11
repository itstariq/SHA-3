# SHA3-256 Cryptographic Hash Algorithm Implementation

## Overview

This project implements the SHA3-256 cryptographic hash algorithm from the ground up, demonstrating the complete process of transforming an arbitrary-length input message into a secure 256-bit hash digest.

The implementation follows the SHA-3 Sponge Construction and Keccak-f[1600] permutation, covering the full hashing lifecycle from input processing and message padding to absorption, permutation, and final digest generation.

## Key Features

- Implemented the complete SHA3-256 hashing process.
- Converted input data into the required hexadecimal and binary representations.
- Applied SHA3-256 message padding and prepared 1088-bit rate blocks.
- Implemented the absorption phase using XOR operations on the 1600-bit Keccak state.
- Implemented the 24-round Keccak-f[1600] permutation.
- Applied all five Keccak round transformations:
  - Theta (θ)
  - Rho (ρ)
  - Pi (π)
  - Chi (χ)
  - Iota (ι)
- Performed the squeezing phase to generate the final 256-bit hash digest.
- Validated the internal state transformations through step-by-step calculations.

## How It Works

SHA3-256 processes the input through the following pipeline:

Input Message
→ Encoding
→ Padding
→ State Initialization
→ Absorption
→ 24 Keccak-f[1600] Rounds
→ Squeezing
→ 256-bit Hash Digest

The internal Keccak state consists of 1600 bits organized as a 5×5 matrix of 64-bit lanes. During each permutation round, the state is transformed using Theta, Rho, Pi, Chi, and Iota operations.

## Project Objective

The objective of this project was to implement and understand the internal mechanics of SHA3-256 rather than relying solely on built-in cryptographic libraries.

The project demonstrates practical understanding of cryptographic hashing, bitwise operations, state transformations, message padding, and the Keccak permutation used by SHA-3.

## Academic Context

Developed as part of the **Network Security (COS 471)** course at **King Saud University**.
