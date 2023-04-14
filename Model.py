from PIL import Image,  ExifTags
from PyQt5.QtGui import QPixmap, QTransform

class ImageModel:
    def __init__(self):
        self.exif_data = None
        self.filepath = None
        self.num_rotations = 0

    def open_image(self, filepath):
        with Image.open(filepath) as img:
            self.filepath = filepath
            self.exif_data = img._getexif()

    def rotate_image(self):
        self.num_rotations += 1

    def get_image(self):
        return QPixmap(self.filepath)

    def get_rotated_image(self):
        angle = self.num_rotations * 90
        trans = QTransform()
        trans.rotate(angle)
        return self.get_image().transformed(trans)

    def get_exif_data(self):
        if self.exif_data:
            exif_str = ''
            for tag_id in sorted(self.exif_data):
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                tag_value = self.exif_data.get(tag_id)
                if isinstance(tag_value, bytes):
                    try:
                        tag_value = tag_value.decode('utf-8')
                    except UnicodeDecodeError:
                        tag_value = tag_value.decode('utf-8', 'replace')
                exif_str += f'{tag_name}: {tag_value}\n'
            return exif_str
        else:
            return 'No EXIF data found.'
