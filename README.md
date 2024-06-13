# Homomorphic Encryption Socket Program

This project demonstrates secure computation of matrix multiplication using homomorphic encryption with socket programming. The Paillier cryptosystem is used to encrypt and decrypt the data securely.

## Description

The project consists of two programs:
- `alice_server.py`: Alice's program that acts as the server.
- `bob_client.py`: Bob's program that acts as the client.

Alice generates a matrix `A`, encrypts it, and sends it to Bob. Bob generates his matrix `B`, performs homomorphic matrix multiplication with the encrypted matrix `A`, and sends the encrypted result back to Alice. Alice then decrypts the result to get the final matrix product `A * B`.

## Prerequisites

- Python 3.x
- `phe` library (Paillier Homomorphic Encryption)
- `numpy` library

You can install the required libraries using:
```bash
pip install phe numpy
