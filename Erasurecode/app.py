import os
from flask import Flask, render_template, request, send_file
from hashlib import sha256
from random import randint
from sympy import Matrix

app = Flask(__name__)

class SecureErasureCode:
    def __init__(self, k, m):
        self.k = k  # Number of data blocks
        self.m = m  # Number of parity blocks
        self.n = k + m  # Total number of blocks
        self.parity_matrix = self.generate_parity_matrix()

    def generate_parity_matrix(self):
        matrix = []
        for i in range(self.k):
            row = []
            for j in range(self.m):
                row.append(randint(0, 255))
            matrix.append(row)
        return Matrix(matrix)

    def encode(self, data):
        if len(data) % self.k != 0:
            raise ValueError("Data length must be divisible by k")
        encoded_blocks = []
        for i in range(0, len(data), self.k):
            block = data[i:i + self.k]
            block_matrix = Matrix([list(block)])
            parity_block = (block_matrix * self.parity_matrix).tolist()[0]
            encoded_parity_block = bytes((x % 256) for x in parity_block)
            encoded_blocks.append(block + encoded_parity_block)
        return encoded_blocks

    def decode(self, encoded_blocks):
        if len(encoded_blocks[0]) % (self.k + self.m) != 0:
            raise ValueError("Encoded block size must be divisible by k+m")

        data_blocks = []
        for encoded_block in encoded_blocks:
            data_blocks.append(encoded_block[:self.k])

        data_matrix = Matrix([list(block) for block in data_blocks])

        if self.m < self.k:
            self.pad_parity_matrix()

        inverse_matrix = self.parity_matrix.inv_mod(256)
        decoded_blocks = []

        for encoded_block in encoded_blocks:
            encoded_block_data = encoded_block[:self.k]
            encoded_block_parity = encoded_block[self.k:]
            reconstructed_parity = (data_matrix * inverse_matrix).tolist()[0]
            reconstructed_block = bytes([a ^ b for a, b in zip(encoded_block_parity, reconstructed_parity)])
            if sha256(encoded_block_data).digest() == sha256(reconstructed_block).digest():
                decoded_blocks.append(reconstructed_block)
            else:
                print("Data integrity check failed. Block may have been tampered with.")
                return None
        return decoded_blocks

    def pad_parity_matrix(self):
        if self.m < self.k:
            num_padding_rows = self.k - self.m
            padding_matrix = Matrix.zeros(num_padding_rows, self.k)
            self.parity_matrix = self.parity_matrix.row_join(padding_matrix)


def save_to_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def read_from_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = file.filename
        data = file.read()
        k = 512 * 1024  # block size in bytes
        m = 3   # Number of parity blocks
        storage_folder = "Erasure_storage_folder"
        if not os.path.exists(storage_folder):
            os.makedirs(storage_folder)

        data_length = len(data)
        if data_length % k != 0:
            padding_length = k - (data_length % k)
            data += b'\x00' * padding_length
        secure_erasure_code = SecureErasureCode(k, m)
        encoded_blocks = []
        while True:
            chunk = data[:k]
            data = data[k:]
            if not chunk:
                break
            encoded_blocks.extend(secure_erasure_code.encode(chunk))
        for i, block in enumerate(encoded_blocks):
            save_to_file(block, os.path.join(storage_folder, f"block_{i}.bin"))
        return "File uploaded and erasure-coded successfully."

@app.route('/download')
def download():
    k = 512 * 1024  # block size in bytes
    m = 3   # Number of parity blocks
    storage_folder = "Erasure_storage_folder"
    files = os.listdir(storage_folder)
    encoded_blocks = []
    for file in files:
        encoded_blocks.append(read_from_file(os.path.join(storage_folder, file)))
    secure_erasure_code = SecureErasureCode(k, m)
    decoded_data = secure_erasure_code.decode(encoded_blocks)
    if decoded_data is not None:
        decoded_file_path = os.path.join(storage_folder, "decoded_file.bin")
        save_to_file(b''.join(decoded_data), decoded_file_path)
        return send_file(decoded_file_path, as_attachment=True)

@app.route('/quit')
def quit():
    # Add logic to quit the application if needed
    return "Quitting the program."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, )  # Run the Flask app in debug mode
