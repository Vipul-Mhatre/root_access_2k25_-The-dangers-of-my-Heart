def vigenere_decrypt(text, key):
    result = []
    key_index = 0
    key = key.lower()
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            base = ord('a') if char.islower() else ord('A')
            dec_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(dec_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def iterative_decrypt(text, key, iterations=10):
    prev = text
    for i in range(iterations):
        new = vigenere_decrypt(prev, key)
        print(f"Iteration {i+1}: {new}")
        if new == prev:
            break
        prev = new
    return prev

ciphertext = "esjxriqrfs{ewp_kmh_lcrx_vjpckr}"
key = "nevergonna"

# Decrypt the entire flag once
plaintext = vigenere_decrypt(ciphertext, key)
print("Initial decryption:", plaintext)

# Extract inner part of the flag
start = plaintext.find('{')
end = plaintext.find('}', start)
if start != -1 and end != -1:
    inner = plaintext[start+1:end]
    print("Inner part before iteration:", inner)
    final_inner = iterative_decrypt(inner, key, iterations=10)
    print("Final inner after iterations:", final_inner)
else:
    print("Flag format not recognized.")