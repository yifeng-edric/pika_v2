

def convert_bytes_to_str(data):
    if isinstance(data, bytes):
        return data.decode()
    else:
        return data
