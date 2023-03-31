import sys
from PIL import Image, ImageQt, ExifTags
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QScrollArea, QSizePolicy


class ExifViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('EXIF Viewer')
        self.setMinimumSize(640, 480)

        # Add a button to open an image file
        self.open_button = QPushButton('Open Image', self)
        self.open_button.clicked.connect(self.open_image)

        # Add a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add a label to display the EXIF data
        # scroll area widget - Labels will move inside this widget
        self.scroll_area = QScrollArea(self)
        self.exif_label = QLabel('No image opened.',  self.scroll_area)
        self.scroll_area.setWidget(self.exif_label)
        self.scroll_area.setWidgetResizable(True)

        # Set up the main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        
    def open_image(self):
        # Open an image file and extract its EXIF data
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open Image', '', 'Image Files (*.jpg *.png *.bmp)')
        if file_path:
            try:
                with Image.open(file_path) as img:
                    # Scale the image to fit in the window
                    img.thumbnail((320, 320))

                    # Display the image
                    qimg = ImageQt.toqpixmap(img)
                    self.image_label.setPixmap(qimg)

                    exif_data = img._getexif()
                    if exif_data:
                        # Format the EXIF data as a string
                        exif_str = ''
                        for tag_id in sorted(exif_data):
                            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                            tag_value = exif_data.get(tag_id)
                            if isinstance(tag_value, bytes):
                                try:
                                    tag_value = tag_value.decode('utf-8')
                                except UnicodeDecodeError:
                                    tag_value = tag_value.decode(
                                        'utf-8', 'replace')
                            exif_str += f'{tag_name}: {tag_value}\n'

                        # Set the label's text to the formatted EXIF data
                        self.exif_label.setText(exif_str)
                    
                    else:
                        self.exif_label.setText('No EXIF data found.')
            except Exception as e:
                print(f"Error opening image file: {e}")
                self.exif_label.setText('Error opening image file.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExifViewer()
    window.show()
    sys.exit(app.exec_())
