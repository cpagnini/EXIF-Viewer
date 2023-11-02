import webbrowser
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt, QSize
import PIL

class ImageController:
    def __init__(self, model, view):
        # Initialize the controller with the model and view
        self.model = model
        self.view = view
        # Connect various user-triggered actions to their respective functions
        self.view.openAction.triggered.connect(self.open_image)
        self.view.rotateRightAction.triggered.connect(self.rotateRight_image)
        self.view.rotateLeftAction.triggered.connect(self.rotateLeft_image)
        self.view.resetAction.triggered.connect(self.reset_image)
        self.view.saveAction.triggered.connect(self.save_image)
        self.view.exif_table.itemDoubleClicked.connect(self.open_link)

        # Update the view to reflect any initial state from the model
        self.update_view()

    # Function to open an image file
    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Open a file dialog for the user to choose an image file
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, 'Open Image', '', "Image Files (*.jpg *.png *.jpeg *.bmp *.gif)", options=options)

        #Trying to open the selected image 
        if file_path: 
            try:
                # Store the file path and open the image using the model
                self.file_path = file_path
                self.model.open_image(file_path)

                # Update the view to display the image in a label
                self.update_view() 
            except Exception as e:
                print(f"Error opening image file: {e}")
                self.view.exif_label.setText('Error opening image file.')

    # Function to save the currently displayed image
    def save_image(self):
        # Check if there is an image to save
        if self.model.get_image() is None:
            self.view.exif_label.setText('No image to save')
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog

            # Open a file dialog for the user to choose a location to save the image
            file_path, _ = QFileDialog.getSaveFileName(
                self.view, 'Save Image', 'NoName.jpg', "Image Files (*.jpg *.png *.jpeg *.bmp *.gif)", options=options)
            if file_path:
                try:
                    # Save the image using the model
                    self.model.save_image(file_path)
                except Exception as e:
                    print(f"Error saving image file: {e}")
                    self.view.exif_label.setText('Error saving image file.')

    # Function to rotate the image to the right
    def rotateRight_image(self):
        # Rotate the image to the right using the model and update the view
        self.model.set_Rightangle()
        self.update_view()

    # Function to rotate the image to the left
    def rotateLeft_image(self):
        # Rotate the image to the left using the model and update the view
        self.model.set_Leftangle()
        self.update_view()

    # Function to reset the image to its original state
    def reset_image(self):
        if self.file_path is not None:
            # Reopen the original image and update the view
            self.model.open_image(self.file_path)
            self.update_view()
        else:
            return

    # Function to calculate and maintain the aspect ratio while resizing the image
    def resize_image(self,size):
        w = 0
        h = 0
        width_ratio = size.width() / 512
        height_ratio = size.height() / 512

        # Determine the appropriate dimensions to fit within a 512x512 bounding box
        if width_ratio > height_ratio:
            w = 512
            h = int(size.height() / width_ratio)
            new_size = QSize(512, int(size.height() / width_ratio))
        else:
            h = int(size.width() / height_ratio)
            w = 512
            new_size = QSize(int(size.width() / height_ratio), 512)
        return h,w
        
        
    # Function to update the view with the rotated image and Exif data
    def update_view(self):
        if self.model.filepath:
            rotateImg = self.model.get_rotated_image()
            size = rotateImg.size()
            h, w = self.resize_image(size)

            # Set the displayed image to the rotated image
            self.view.image_label.setPixmap(rotateImg)
            _exif_data = self.model.get_exif_data()
            if(_exif_data is not None):
                self.view.exif_table.setRowCount(len(_exif_data))
                i = 0

                # Iterate through Exif data and display it in a table in the view
                for key in _exif_data:
                    tag_name = self.model.exif_key(key)
                    if tag_name == 'GPSInfo':
                        self.view.exif_table.setItem(i, 0, QTableWidgetItem(tag_name))
                        self.view.exif_table.setItem(i, 1, QTableWidgetItem(self.model.manage_gps_info(_exif_data[key])))
                    else:
                        self.view.exif_table.setItem(i, 0, QTableWidgetItem(tag_name))
                        self.view.exif_table.setItem(i, 1, QTableWidgetItem(str(_exif_data[key])))
                    i += 1

    # Function to open a web link if the item text contains "maps"
    def open_link(self, item):
        if 'maps' in item.text():
            webbrowser.open(item.text())
