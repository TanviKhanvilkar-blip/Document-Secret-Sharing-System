# ==================== PART 2: RECONSTRUCTOR ====================
import os
import sys
import json
import hashlib
from Crypto.Util import number

# === ARGUMENTS ===
if len(sys.argv) != 5:
    print("Usage: python part2_reconstructor.py <input_dir> <output_file> <num_shares> <threshold>")
    sys.exit(1)

input_dir = sys.argv[1]
output_file = sys.argv[2]
num_shares = int(sys.argv[3])
threshold = int(sys.argv[4])
chunk_size = 132

# === SETUP ===
with open(os.path.join(input_dir, "prime.txt")) as f:
    prime = int(f.read())

# === FUNCTIONS ===
def modinv(a, p):
    return pow(a, -1, p)

def interpolate(x_values, y_values, p):
    total = 0
    for i in range(len(x_values)):
        xi, yi = x_values[i], y_values[i]
        li_num = 1
        li_den = 1
        for j in range(len(x_values)):
            if i != j:
                xj = x_values[j]
                li_num = (li_num * (-xj)) % p
                li_den = (li_den * (xi - xj)) % p
        inv_den = modinv(li_den, p)
        li = (li_num * inv_den) % p
        total = (total + yi * li) % p
    return total

def reconstruct_secret_bytes(shares, prime):
    x_vals, y_vals = zip(*shares)
    secret_int = interpolate(x_vals, y_vals, prime)
    return secret_int.to_bytes(chunk_size, byteorder='big')

# === LOAD AND VALIDATE SHARES ===
print("[*] Validating and loading shares...")
with open(os.path.join(input_dir, "hashes.json")) as f:
    expected_hashes = json.load(f)
with open(os.path.join(input_dir, "lengths.json")) as f:
    chunk_lengths = json.load(f)

valid_shares = []
valid_share_indices = []
missing_shares = []

for i in range(1, num_shares + 1):
    share_name = f"share_{i}"
    share_path = os.path.join(input_dir, f"{share_name}.txt")

    if not os.path.exists(share_path):
        print(f"[!] {share_name} is missing!")
        missing_shares.append(share_name)
        continue

    with open(share_path) as f:
        data = f.read().strip()

    sha = hashlib.sha256(data.encode()).hexdigest()
    if sha != expected_hashes.get(share_name):
        print(f"[!] {share_name} hash mismatch! Possible tampering detected!")
        continue

    print(f"[+] {share_name} passed hash check.")
    lines = [(int(x), int(y, 16)) for x, y in (line.split('-') for line in data.split('\n') if '-' in line)]
    valid_shares.append(lines)
    valid_share_indices.append(i)

# === RECONSTRUCT FILE ===
print("[*] Reconstructing document...")
if len(valid_shares) < threshold:
    print(f"[!] Not enough valid shares ({len(valid_shares)} provided, {threshold} required). Cannot reconstruct document.")
    sys.exit(1)

num_chunks = max(len(s) for s in valid_shares)
reconstructed = []

for chunk_idx in range(num_chunks):
    chunk_shares = [s[chunk_idx] for s in valid_shares if chunk_idx < len(s)]

    if len(chunk_shares) < threshold:
        print(f"[!] Skipping chunk {chunk_idx}: Not enough valid shares.")
        continue

    try:
        chunk = reconstruct_secret_bytes(chunk_shares[:threshold], prime)
        reconstructed.append(chunk)
    except Exception as e:
        print(f"[!] Error in chunk {chunk_idx}: {e}")

with open(output_file, "wb") as f:
    f.write(b''.join(reconstructed))
print(f"[+] Reconstructed file saved at: {output_file}")
