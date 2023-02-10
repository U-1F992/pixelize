from time import sleep

import cv2
from PIL import Image

from pixelize import pixelize


CLEAR = "\033[2J"
TOP = "\033[H"
RESET = "\033[0m"

print(CLEAR + TOP)


capture = cv2.VideoCapture(0)
if not capture.isOpened():
    raise IOError()

try:
    while True:
        _, mat = capture.read()

        height, width, _ = mat.shape
        mat = cv2.resize(mat, (width // 12, height // 12))
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)

        print(TOP)
        for line in pixelize(Image.fromarray(mat)).splitlines():
            print(line)

except KeyboardInterrupt:
    capture.release()
    print(RESET + CLEAR + TOP)
