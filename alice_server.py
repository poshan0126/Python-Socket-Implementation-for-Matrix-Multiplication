import numpy as np
import socket
import pickle
from phe import paillier

# Function to send data through the socket
def send_data(conn, data):
    conn.sendall(pickle.dumps(data) + b"END")

# Function to receive data through the socket
def receive_data(conn):
    data = b""
    while True:
        packet = conn.recv(4096)
        if packet[-3:] == b"END":
            data += packet[:-3]
            break
        data += packet
    return pickle.loads(data)

def main(key_size):
    # Step 1: Key Generation
    public_key, private_key = paillier.generate_paillier_keypair(n_length=key_size)

    # Step 2: Generate Matrix A
    np.random.seed(42)
    A = np.random.randint(0, 10, (5, 8))
    encrypted_A = [[public_key.encrypt(int(x)) for x in row] for row in A]

    # Step 3: Set up the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 65432))
    server.listen(1)

    print("Alice's server is listening...")

    # Step 4: Wait for Bob to connect
    conn, addr = server.accept()
    print('Connected by', addr)

    # Step 5: Send public key and encrypted matrix A to Bob
    print("Sending public key and encrypted matrix A to Bob...")
    send_data(conn, (public_key, encrypted_A))
    print("Sent public key and encrypted matrix A to Bob.")

    # Step 6: Receive the encrypted result from Bob
    print("Waiting to receive encrypted result from Bob...")
    encrypted_result = receive_data(conn)
    print("Received encrypted result from Bob.")

    # Step 7: Decrypt the result
    result = np.zeros((A.shape[0], len(encrypted_result[0])), dtype=int)
    for i in range(A.shape[0]):
        for j in range(len(encrypted_result[0])):
            result[i][j] = private_key.decrypt(encrypted_result[i][j])

    # Report results
    print(f"Key Size: {key_size} bits")
    print("Matrix A (held by Alice):\n", A)
    print("Last ciphertext before decryption (first element):\n", encrypted_result[0][0].ciphertext())
    print("Matrix A * Matrix B (computed securely):\n", result)

    # Close the connection
    conn.close()
    server.close()

if __name__ == "__main__":
    main(512)  # Run with 512-bit key size
    main(1024)  # Run with 1024-bit key size
