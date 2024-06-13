import numpy as np
import socket
import pickle
from phe import paillier

# Function to send data through the socket
def send_data(sock, data):
    sock.sendall(pickle.dumps(data) + b"END")

# Function to receive data through the socket
def receive_data(sock):
    data = b""
    while True:
        packet = sock.recv(4096)
        if packet[-3:] == b"END":
            data += packet[:-3]
            break
        data += packet
    return pickle.loads(data)

def main():
    # Step 1: Generate Matrix B
    np.random.seed(42)
    B = np.random.randint(0, 10, (8, 4))
    print("Matrix B (held by Bob):\n", B)

    # Step 2: Connect to Alice's server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 65432))
    print("Connected to Alice's server.")

    # Step 3: Receive the public key and encrypted matrix A from Alice
    print("Receiving public key and encrypted matrix A from Alice...")
    public_key, encrypted_A = receive_data(client)
    print("Received public key and encrypted matrix A from Alice.")

    # Step 4: Perform homomorphic matrix multiplication
    print("Performing homomorphic matrix multiplication...")
    encrypted_result = []
    for i in range(len(encrypted_A)):
        row_result = []
        for j in range(B.shape[1]):
            encrypted_sum = public_key.encrypt(0)
            for k in range(len(encrypted_A[0])):
                encrypted_sum += encrypted_A[i][k] * int(B[k][j])
            row_result.append(encrypted_sum)
        encrypted_result.append(row_result)
    print("Homomorphic matrix multiplication done.")

    # Step 5: Send the encrypted result back to Alice
    print("Sending encrypted result back to Alice...")
    send_data(client, encrypted_result)
    print("Sent encrypted result back to Alice.")

    # Close the connection
    client.close()

if __name__ == "__main__":
    main()
