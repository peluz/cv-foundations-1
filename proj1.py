import argparse
import numpy as np
import cv2
import sys


parser = argparse.ArgumentParser(
    description="Processamento de imagens ou vídeos")
parser.add_argument("requisito", type=int, nargs=1, choices=range(1, 5),
                    help="número do requisito de avaliação")
parser.add_argument("-file", nargs="?", default=None, metavar="path/to/file",
                    help="Caminho para a imagem/vídeo")

def openImage(file):
    if file is None:
        filename = "data/default_image.png"
    else:
        filename = file
    img = cv2.imread(filename)
    if img is None:
        sys.exit("Não foi possível abrir imagem")
    greyscale = (img[:, :, 0] == img[:, :, 1]).all() and (img[:, :, 0] == img[:, :, 2]).all()
    return img, greyscale


def openVideo(file):
    if file is None:
        filename = "data/default_video.avi"
    else:
        filename = file
    cap = cv2.VideoCapture(filename)
    if cap is None:
        sys.exit("Não foi possível abrir video")
    return cap


def getPixel(event, x, y, flags, params):
    img, greyscale = params
    if event == cv2.EVENT_LBUTTONUP:
        value = img[y][x][::-1]
        if greyscale:
            value = value[0]
        print("({}, {}) Valor: {}".format(y, x, value))


def clickImage(file=None):
    img, greyscale = openImage(file)
    cv2.namedWindow('Imagem')
    cv2.setMouseCallback('Imagem', getPixel, (img, greyscale))
    while(1):
        cv2.imshow("Imagem", img)
        cv2.waitKey(1)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


def magicImage(file=None):
    global value
    value = None
    img, _ = openImage(file)
    cv2.namedWindow('Imagem')
    cv2.setMouseCallback('Imagem', staticMagic, img)
    while(1):
        cv2.imshow("Imagem", img)
        if value is not None:
            img[np.linalg.norm(img.astype(float) - value.astype(float), axis=-1) < 13] = (0, 0, 255)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


def staticMagic(event, x, y, flags, params):
    global value
    if event == cv2.EVENT_LBUTTONUP:
        value = params[y][x]


def magicVideo(file=None):
    global value
    value = None
    cap = openVideo(file)
    delay = int( (1 / int(cap.get(5))) * 1000)
    while(cap.isOpened()):
        ret, img = cap.read()
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', staticMagic, img)
        if ret:
            if value is not None:
                img[np.linalg.norm(img.astype(float) - value.astype(float), axis=-1) < 13] = (0, 0, 255)
        cv2.imshow('image', img)
        if cv2.waitKey(delay) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def magicCam(file=None):
    global value
    value = None
    cap = cv2.VideoCapture(0)
    delay = int( (1 / int(cap.get(5))) * 1000)


    while(True):
        ret, img = cap.read()
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', staticMagic, img)
        if ret:
            if value is not None:
                img[np.linalg.norm(img.astype(float) - value.astype(float), axis=-1) < 13] = (0, 0, 255)
        cv2.imshow('image', img)
        if cv2.waitKey(delay) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def main(requisite, file=None):
    return {1: clickImage,
            2: magicImage,
            3: magicVideo,
            4: magicCam}[requisite](file)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.requisito[0], args.file)
