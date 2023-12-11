import cv2
import numpy as np


def generate_binary_img():
    # Create a black image
    image = np.zeros((1, 1, 3), np.uint8)

    # Save the image
    cv2.imwrite('data/test_image.png', image)


def read_binary_img():
    with open('../upload/test_image.png', 'rb') as image_file:
        binary_data = image_file.read()
        print(binary_data)


if __name__ == "__main__":
    # generate_binary_img()
    read_binary_img()

