from pathlib import Path

from PIL import Image

from pixelize import pixelize

sample = Path(__file__).parent.joinpath("sample.png")
ret = pixelize(Image.open(sample))

print(ret)

# print("Don't know why, collapse")
# print(ret + "\n")
