from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

class ImageController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.openAction.triggered.connect(self.open_image)
        self.view.rotateAction.triggered.connect(self.rotate_image)
        self.update_view()

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, 'Open Image', '', "Image Files (*.jpg *.png *.jpeg *.bmp *.gif)", options=options)
        #file_path = "C:\\Users\\claudio.pagnini\\Downloads\\gps_test2.jpg"
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
            _exif_data = self.model.get_exif_data()
            if(_exif_data is not None):
                self.view.exif_table.setRowCount(len(_exif_data))
                i = 0
                for key in _exif_data:
                    tag_name = self.model.exif_key(key)
                    if tag_name == 'GPSInfo':
                        self.view.exif_table.setItem(i, 0, QTableWidgetItem(tag_name))
                        self.view.exif_table.setItem(i, 1, QTableWidgetItem(self.model.manage_gps_info(_exif_data[key])))
                    else:
                        self.view.exif_table.setItem(i, 0, QTableWidgetItem(tag_name))
                        self.view.exif_table.setItem(i, 1, QTableWidgetItem(str(_exif_data[key])))
                    # Status bar description for clickable links
                    # if 'http' in self.view.exif_table.item(i, 1).text():
                    #     self.view.exif_table.setStatusTip(
                    #         'Double click on the GPS location link to open a map centered at those GPS coordinates.')
                    i += 1
                    #self.view.exif_table.itemDoubleClicked.connect(self.open_link)
        #else:
            #self.view.image_label.setPixmap(QPixmap())
            #self.view.exif_label.setText('No image opened.')

    #def open_link(self):
        #if 'http' in self.view.exif_table.item