from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter, ImageEnhance
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

import os


class ImageProcessor():
    def __init__(self):
        self.file_name = None
        self.image = None
        self.folder_name = None
        self.save_dir = "Modified/"

    def load_image(self, dir, file_name):
        self.folder_name = dir
        self.file_name = file_name
        file_path = os.path.join(dir, file_name)
        self.image = Image.open(file_path)

    def show_image(self, path):
        cover.hide()
        pixmap_image = QPixmap(path)
        w, h = cover.width(), cover.height()
        pixmap_image = pixmap_image.scaled(w, h, Qt.KeepAspectRatio)
        cover.setPixmap(pixmap_image)
        cover.show()

    def save_image(self):
        path = os.path.join(work_dir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.file_name)
        self.image.save(image_path)

    def black_and_white(self):
        self.image = self.image.convert('L')
        self.save_image()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.show_image(image_path)

    def turn_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.show_image(image_path)

    def turn_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.show_image(image_path)

    def mirrow(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.show_image(image_path)

    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.save_image()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.show_image(image_path)

    def contrast(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.save_image()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.show_image(image_path)

    def cropped(self):
        box = (120, 100, 550, 500)
        pic_crop = self.original.crop(box)
        self.changed.append(pic_crop)
        pic_crop.save(self.named())

app = QApplication([])
window = QWidget()

#Создание интерфейса приложения
window.setWindowTitle('Easy Editor')
window.resize(900, 700)
#window.setStyleSheet('background-color: rgb(28, 43, 255);')

main_hline = QHBoxLayout()
v1_line = QVBoxLayout()
v2_line = QVBoxLayout()
h11_line = QHBoxLayout()
h12_line = QHBoxLayout()
h21_line = QHBoxLayout()
h22_line = QHBoxLayout()
h23_line = QHBoxLayout()

folder_btn = QPushButton('Папка')
h11_line.addWidget(folder_btn)

images = QListWidget()
h12_line.addWidget(images)

v1_line.addLayout(h11_line)
v1_line.addLayout(h12_line)
main_hline.addLayout(v1_line, stretch = 1)

cover = QLabel('Картинка')
h21_line.addWidget(cover)

left_btn = QPushButton('Лево')
right_btn = QPushButton('Право')
mirrow_btn = QPushButton('Зеркало')
contrast_btn = QPushButton('Резкость')
blur_btn = QPushButton('Размытие')
bw_btn = QPushButton('Ч/Б')
h22_line.addWidget(left_btn)
h22_line.addWidget(right_btn)
h22_line.addWidget(mirrow_btn)
h23_line.addWidget(blur_btn)
h23_line.addWidget(contrast_btn)
h23_line.addWidget(bw_btn)

v2_line.addLayout(h21_line)
v2_line.addLayout(h22_line)
v2_line.addLayout(h23_line)
main_hline.addLayout(v2_line, stretch = 4)

window.setLayout(main_hline)

#Функционал
work_dir = ''

def filter(files, extensions):
    total = []
    for file_name in files:
        for ext in extensions:
            if file_name.endswith(ext):
                total.append(file_name)
    return total

def save_folder():
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()
    return work_dir

def show_folder():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webm']
    work_dir = save_folder()
    try:
        files = os.listdir(work_dir)
        images.clear()
        images.addItems(filter(files, extensions))
    except FileNotFoundError:
        pass
    

folder_btn.clicked.connect(show_folder)

work_image = ImageProcessor()

def showChosenImage(self):
    if images.currentRow() >= 0:
        file_name = images.currentItem().text()
        work_image.load_image(work_dir, file_name)
        file_path = os.path.join(work_dir, work_image.file_name)
        work_image.show_image(file_path)

images.currentRowChanged.connect(showChosenImage)
bw_btn.clicked.connect(work_image.black_and_white)
left_btn.clicked.connect(work_image.turn_left)
right_btn.clicked.connect(work_image.turn_right)
mirrow_btn.clicked.connect(work_image.mirrow)
blur_btn.clicked.connect(work_image.blur)
contrast_btn.clicked.connect(work_image.contrast)

window.show()
app.exec_()