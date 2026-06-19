# ==================== PART 1: SHARE GENERATOR ====================
import os
import sys
import json
import hashlib
import random
from Crypto.Util import number

# === ARGUMENTS ===
if len(sys.argv) != 5:
    print("Usage: python part1_generator.py <input_file> <output_dir> <num_shares> <threshold>")
    sys.exit(1)

input_file = sys.argv[1]
output_dir = sys.argv[2]
num_shares = int(sys.argv[3])
threshold = int(sys.argv[4])
chunk_size = 132  

# === SETUP ===
os.makedirs(output_dir, exist_ok=True)
prime = number.getPrime(1128)
with open(os.path.join(output_dir, "prime.txt"), "w") as f:
    f.write(str(prime))

# === FUNCTIONS ===
def split_secret_bytes(chunk_bytes, n, k, prime):
    secret_int = int.from_bytes(chunk_bytes, byteorder='big')
    coeffs = [secret_int] + [random.randint(0, prime - 1) for _ in range(k - 1)]
    shares = []
    for i in range(1, n + 1):
        x = i
        y = sum([(c * pow(x, idx, prime)) % prime for idx, c in enumerate(coeffs)]) % prime
        shares.append((x, y))
    return shares

# === GENERATE SHARES ===
print("[*] Reading input file and splitting into chunks...")
with open(input_file, "rb") as f:
    binary_data = f.read()
chunks = [binary_data[i:i + chunk_size] for i in range(0, len(binary_data), chunk_size)]
chunks = [chunk.ljust(chunk_size, b'\x00') for chunk in chunks]
chunk_lengths = [len(chunk) for chunk in chunks]

share_files = [[] for _ in range(num_shares)]
hashes = {}

print("[*] Generating shares...")
for chunk in chunks:
    shares = split_secret_bytes(chunk, num_shares, threshold, prime)
    for i, (x, y) in enumerate(shares):
        y_hex = hex(y)[2:].zfill(chunk_size * 2)
        share_files[i].append(f"{x}-{y_hex}")

for i, share_lines in enumerate(share_files, start=1):
    joined = "\n".join(share_lines)
    filename = f"share_{i}.txt"
    full_path = os.path.join(output_dir, filename)
    with open(full_path, "w") as f:
        f.write(joined)
    sha = hashlib.sha256(joined.encode()).hexdigest()
    hashes[f"share_{i}"] = sha
    print(f"[+] share_{i} written to {full_path}")

with open(os.path.join(output_dir, "hashes.json"), "w") as f:
    json.dump(hashes, f, indent=4)
with open(os.path.join(output_dir, "lengths.json"), "w") as f:
    json.dump(chunk_lengths, f)
print("[+] Share generation complete.")