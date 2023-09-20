import cv2
import numpy as np

# Use Keras-OCR
import keras_ocr


def main():
    image = cv2.imread("../../data/frame/peanuts_0_1.png")

    # Use Tesseract
    # text = cv2.getText(image, cv2.text.OCR_DEFAULT)

    # keras_ocr
    # # predictor = keras_ocr.Predictor(weights="english_weights.h5")
    # prediction = predictor.predict(image)

    mask = np.zeros(image.shape, dtype=np.uint8)
    for box in prediction["boxes"]:
        cv2.rectangle(mask, (box[0], box[1]), (box[2], box[3]), (255, 255, 255), -1)

    inpainted_image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

    cv2.imwrite("inpainted_image.jpg", inpainted_image)


if __name__ == "__main__":
    main()
