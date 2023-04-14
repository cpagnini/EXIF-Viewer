from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog

class ImageController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.open_button.clicked.connect(self.open_image)
        self.view.rotate_button.clicked.connect(self.rotate_image)
        self.update_view()

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, 'Open Image', '', "Image Files (*.jpg *.png *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            try:
                self.model.open_image(file_path)
                self.update_view()
            except Exception as e:
                print(f"Error opening image file: {e}")
                self.view.exif_label.setText('Error opening image file.')

    def rotate_image(self):
        self.model.rotate_image()
        self.update_view()

    def update_view(self):
        if self.model.filepath:
            self.view.image_label.setPixmap(self.model.get_rotated_image())
            self.view.exif_label.setText(self.model.get_exif_data())
        else:
            self.view.image_label.setPixmap(QPixmap())
            self.view.exif_label.setText('No image opened.')
