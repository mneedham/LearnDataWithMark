import hashlib

def colour_code_for(label):
    hash_object = hashlib.sha256(label.encode())
    hash_int = int.from_bytes(hash_object.digest(), 'big')
    darker_color_code_int = hash_int % 0x505050
    return f'#{darker_color_code_int:06x}'