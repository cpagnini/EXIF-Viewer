import webbrowser
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt, QSize
import PIL

class ImageController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.file_path = None
        self.view.openAction.triggered.connect(self.open_image)
        self.view.rotateRightAction.triggered.connect(self.rotateRight_image)
        self.view.rotateLeftAction.triggered.connect(self.rotateLeft_image)
        self.view.resetAction.triggered.connect(self.reset_image)
        self.view.saveAction.triggered.connect(self.save_image)
        self.view.exif_table.itemDoubleClicked.connect(self.open_link)
        self.update_view()
        #print('controller')

    def open_image(self):
        #Opens dialog to choose image
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, 'Open Image', '', "Image Files (*.jpg *.png *.jpeg *.bmp *.gif)", options=options)
        #Trying to open image 
        if file_path: 
            try:
                self.file_path = file_path
                self.model.open_image(file_path)
                self.update_view() #Show it in a label
            except Exception as e:
                print(f"Error opening image file: {e}")
                self.view.exif_label.setText('Error opening image file.')

    def save_image(self):
        if self.model.get_image() is None:
            self.view.exif_label.setText('No image to save')
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self.view, 'Save Image', 'NoName.jpg', "Image Files (*.jpg *.png *.jpeg *.bmp *.gif)", options=options)
            if file_path:
                try:
                    self.model.save_image(file_path)
                except Exception as e:
                    print(f"Error saving image file: {e}")
                    self.view.exif_label.setText('Error saving image file.')


    def rotateRight_image(self):
        self.model.set_Rightangle()
        self.update_view()

    def rotateLeft_image(self):
        self.model.set_Leftangle()
        self.update_view()

    def reset_image(self):
        if self.file_path is not None:
            self.model.open_image(self.file_path)
            self.update_view()
        else:
            return
    
    def resize_image(self,size):
        # calculate new label size while maintaining aspect ratio
        w = 0
        h = 0
        width_ratio = size.width() / 512
        height_ratio = size.height() / 512
        if width_ratio > height_ratio:
            w = 512
            h = int(size.height() / width_ratio)
            new_size = QSize(512, int(size.height() / width_ratio))
        else:
            h = int(size.width() / height_ratio)
            w = 512
            new_size = QSize(int(size.width() / height_ratio), 512)
        return h,w
        
        

    def update_view(self):
        if self.model.filepath:
            rotateImg = self.model.get_rotated_image()
            size = rotateImg.size()
            h, w = self.resize_image(size)
            self.view.image_label.setPixmap(rotateImg)
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
                    i += 1


    def open_link(self, item):
        #If the item passed has maps in it, open browswer with its text - aka a Link
        if 'maps' in item.text():
            webbrowser.open(item.text())
