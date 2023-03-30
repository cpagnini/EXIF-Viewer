import sys
from PIL import Image, ImageQt, ExifTags
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QScrollArea, QHBoxLayout


class ExifViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('EXIF Viewer')
        self.setFixedSize(500, 400)
        #self.setLayout(QVBoxLayout())

        # Add a button to open an image file
        self.open_button = QPushButton('Open Image', self)
        self.open_button.clicked.connect(self.open_image)
        self.open_button.setGeometry(10, 10, 100, 30)
        #self.layout().addWidget(self.open_button)

        # Add a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(120, 70, 320, 320)
        

        # Add a label to display the EXIF data
        self.scroll_area = QScrollArea(self) #scroll area widget - Labels will move inside this widget
        self.scroll_area.setGeometry(10, 70, 480, 340)
        self.exif_label = QLabel('No image opened.',  self.scroll_area)
        self.scroll_area.setWidget(self.exif_label)
        self.scroll_area.setWidgetResizable(True)
        #self.layout().addWidget(self.exif_label)
        #self.exif_label.setGeometry(10, 70, 480, 340)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.open_button)
        self.button_layout.addStretch()
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.scroll_area)
        self.image_layout = QHBoxLayout()
        self.image_layout.addWidget(self.image_label)
        self.image_layout.addWidget(self.scroll_area)
        self.layout.addLayout(self.image_layout)
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
