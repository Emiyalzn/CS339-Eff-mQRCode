import os
from PIL import Image
from pyzbar.pyzbar import decode

def qr_decode(url):
	decode_result = decode(Image.open(url))
	if len(decode_result):
		return str(decode_result[0].data, encoding='utf-8')
	else:
		return "failed to recognize"

def compute_acc(dir_name, num):
	right_num = 0
	for i in range(num):
		fake_name = f"QR_{i}_fake_B.png"
		real_name = f"QR_{i}_real_B.png"
		fake_url = os.path.join(dir_name, fake_name)
		real_url = os.path.join(dir_name, real_name)
		real_content = qr_decode(real_url)
		fake_content = qr_decode(fake_url)
		if real_content == fake_content:
			right_num += 1
	acc = right_num / num
	return acc

if __name__ == "__main__":
	dir_name = "../results/deblurPix2PixGAN_default/test_latest/images"
	test_acc = compute_acc(dir_name, 1716)
	print(f"The test accuracy is: {test_acc:.4f}.")