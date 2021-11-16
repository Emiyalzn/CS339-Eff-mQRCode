import os
from PIL import Image
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt

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

def plot_acc(x, y):
	plt.figure(figsize=(10,5))
	plt.title("deblurPix2PixGAN acc over time")
	plt.xlabel("epoch")
	plt.ylabel("acc")
	plt.plot(x,y, label="test_acc")
	plt.legend()
	plt.grid(True)
	plt.show()


if __name__ == "__main__":
	test_epochs = [20, 40, 60, 80, 100, 120, 160, 200]
	test_accs = []
	for epoch in test_epochs:
		dir_name = f"../results/deblurPix2PixGAN_default/test_{epoch}/images"
		test_acc = compute_acc(dir_name, 1716)
		print(f"Epoch {epoch}'s test accuracy is: {test_acc:.4f}.")
		test_accs.append(test_acc)
	plot_acc(test_epochs, test_accs)