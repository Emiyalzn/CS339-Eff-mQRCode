import os

def rename(root):
    sum_list = [0] * 10000
    sum = 0
    for i in range(9880):
        name = f'QR_{i}.jpg'
        file = os.path.join(root, name)
        if not os.path.isfile(file):
            sum += 1
        sum_list[i-sum+1] = sum

    for i in range(9880):
        orig_name = f'QR_{i+sum_list[i]}.jpg'
        orig_file = os.path.join(root, orig_name)
        new_name = f'QR_{i}.jpg'
        new_file = os.path.join(root, new_name)
        os.rename(orig_file, new_file)

def addBias(root, bias):
    for i in range(6624, 7624, 1):
        orig_name = f'QR_{i}.jpg'
        new_name = f'QR_{i+bias}.jpg'
        orig_file = os.path.join(root, orig_name)
        new_file = os.path.join(root, new_name)
        os.rename(orig_file, new_file)

if __name__ == '__main__':
    addBias("ToDo/change", -6624)