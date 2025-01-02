import os
import timeit
import array
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk  

class Node:
    def __init__(self, value=None, char=None, left=None, right=None):
        self.value = value
        self.char = char
        self.left = left
        self.right = right
    def is_leaf(self):
        return self.left is None and self.right is None

    def get_value(self):
        return self.value

    def get_char(self):
        return self.char


def compress(path, mode=1):
    if mode == 1:
        name = str(os.path.splitext(path)[0])
        data = str(read_file(path), 'utf-8')
        freq_map = frequency_map(data)
        language_map, compressed_header = huffman_coding(freq_map)
        output = encode(data, language_map, compressed_header, mode=mode)
        output = bytes(output, 'UTF-8')
        size = create_output(output, name + ".bin", 0)
    elif mode == 2:
        os.chdir(path)
        data = bytes()
        for file in os.listdir(path):
            if file.endswith(".txt"):
                data += read_file(file, mode=0) + b'\x11\x22\x33'
        data = str(data, 'utf-8')
        freq_map = frequency_map(data)
        language_map, compressed_header = huffman_coding(freq_map)
        output = encode(data, language_map, compressed_header, mode=mode)
        output = bytes(output, 'UTF-8')
        os.chdir('..')
        size = create_output(output, os.path.basename(path) + "_compressed.bin", 0)
        os.chdir(cwd)
    return size

def frequency_map(data):
    frequency = {}
    for character in data:
        if character not in frequency:
            frequency[character] = 1
        else:
            frequency[character] += 1
    return frequency

def huffman_coding(freq_map):
    freq_map = sorted(freq_map.items(), key=lambda x: x[1])
    nodes = []
    for key, value in freq_map:
        node = Node(value, key)
        nodes.append(node)
    while len(nodes) > 1:
        node1 = nodes[0]
        node2 = nodes[1]
        nodes = nodes[2:]
        sum_node = node1.get_value() + node2.get_value()
        node = Node(sum_node, left=node1, right=node2)
        i = 0
        while i < len(nodes) and node.get_value() > nodes[i].get_value():
            i += 1
        nodes[i:i] = [node]
    compressed_tree = encode_tree(nodes[0], "")
    d = assign_code(nodes[0], '')
    return d, compressed_tree

def encode_tree(node, code):
    if node.is_leaf():
        code += "1"
        code += f"{ord(node.get_char()):08b}"
    else:
        code += "0"
        code = encode_tree(node.left, code)
        code = encode_tree(node.right, code)
    return code

def assign_code(node, code=''):
    if not node.left and not node.right:
        return {node.get_char(): code}
    d = dict()
    d.update(assign_code(node.left, code + '0'))
    d.update(assign_code(node.right, code + '1'))
    return d

def encode(data, language_map, compressed_header, mode=0):
    compressed_header = str(mode) + compressed_header
    output = ""
    bits = ""
    for char in data:
        bits += language_map[char]
    num = 8 - (len(bits) + len(compressed_header)) % 8
    if num != 0:
        output = num * "0" + bits
    output = f"{compressed_header}{num:08b}{output}"
    return output

def create_output(data, name, mode=0):
    if mode == 0:
        b_arr = bytearray()
        for i in range(0, len(data), 8):
            b_arr.append(int(data[i:i + 8], 2))
        try:
            output_path = open(name, "wb")
            output_path.write(b_arr)
            print("Success, data saved at: " + name)
            return os.stat(name).st_size
        except IOError:
            print("Something went wrong")
            exit(-1)
    else:
        try:
            output_path = open(name, "w", encoding='utf-8', newline='\n')
            output_path.write(data)
            print("Success, data saved at: " + name)
            return os.stat(name).st_size
        except IOError:
            print("Something went wrong")
            exit(-1)

def decompress(path):
    data = read_file(path, mode=1)
    data = list(data)

    mode = int(data[0])
    del data[0]

    node = decode_tree(data)
    d = assign_code(node)
    reversed_tree = {v: k for k, v in d.items()}

    n_padding = data[:8]
    n_padding = int("".join(n_padding), 2)
    data = data[8:]
    data = data[n_padding:]

    data = decode(data, reversed_tree)

    name = str(os.path.splitext(path)[0])

    if mode == 1:
        output = ""
        for num in data:
            output += format(num, '08b')

        b_arr = bytearray()

        for i in range(0, len(output), 8):
            b_arr.append(int(output[i:i + 8], 2))

        create_output(str(b_arr, 'utf-8'), name + '.txt', mode=1)
    else:
        op_files = array.array('B', data).tobytes().split(b'\x11\x22\x33')
        for i, file in enumerate(op_files[0:len(op_files) - 1]):
            create_output(str(op_files[i][:len(op_files[i])], 'utf-8'), name + str(i) + '.txt', mode=1)

def decode_tree(data):
    char = data[0]
    del data[0]

    if char == "1":
        byte = ""
        for _ in range(8):
            byte += data[0]
            del data[0]

        return Node(char=int(byte, 2))
    else:
        left = decode_tree(data)
        right = decode_tree(data)

        return Node(None, left=left, right=right)

def decode(data, language_map):
    code = ""
    output = []
    for bit in data:
        code += bit
        if code in language_map:
            output.append(language_map[code])
            code = ""
    return output

def read_file(path, mode=0):
    f = open(path, 'rb')
    if mode == 0:
        return f.read()
    else:
        data = ""
        byte = f.read(1)
        while len(byte) > 0:
            data += f"{bin(ord(byte))[2:]:0>8}"
            byte = f.read(1)
        return data

def browse_file(file_type='txt'): 
    if file_type == 'bin':
        filename = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
    else:
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return filename

def on_compress():
    file_path = browse_file('txt')
    if not file_path:
        return
    original_size = os.stat(file_path).st_size
    start = timeit.default_timer()
    new_size = compress(file_path, mode=1)
    end = timeit.default_timer()
    compression_rate = 100 - (new_size / original_size) * 100
    messagebox.showinfo("Compression Done", f"File compressed successfully!\nCompression Rate: {compression_rate:.2f}%")
    execution_time = f"{end - start:.4f} seconds"
    status_label.config(text=f"Execution time: {execution_time}")

def on_decompress():
    file_path = browse_file('bin')  
    if not file_path:
        return
    start = timeit.default_timer()
    decompress(file_path)
    end = timeit.default_timer()
    execution_time = f"{end - start:.4f} seconds"
    messagebox.showinfo("Decompression Done", f"File decompressed successfully!")
    status_label.config(text=f"Execution time: {execution_time}")

root = ctk.CTk()  
root.title("File Compression and Decompression")
root.geometry("300x250")

compress_button = ctk.CTkButton(root, text="Compress File", command=on_compress, width=200, height=40)
compress_button.pack(pady=10)

decompress_button = ctk.CTkButton(root, text="Decompress File", command=on_decompress, width=200, height=40)
decompress_button.pack(pady=10)

status_label = ctk.CTkLabel(root, text="Execution time: N/A")
status_label.pack(pady=20)
root.mainloop()
