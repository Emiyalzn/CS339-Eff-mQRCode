import os
from PIL import Image
from pyzbar.pyzbar import decode

def qr_decode(url):
	decode_result = decode(Image.open(url))
	if len(decode_result):
		return str(decode_result[0].data, encoding='utf-8')
	else:
		return "failed to recognize"

if __name__ == "__main__":
	dir_name = "../datasets/qrcode/trainB"
	files = os.listdir(dir_name)
	for file in files:
		path = os.path.join(dir_name, file)
		# print(decode_qrcode(path + '/' + file,file))
		qr_decode(path)