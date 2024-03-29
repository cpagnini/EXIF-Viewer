from PIL import Image,ExifTags, ImageQt
from PyQt5.QtGui import QPixmap, QTransform

# ImageModel class responsible for managing image data and EXIF information
class ImageModel:
    def __init__(self):
        # Initialize the model with initial data
        self.image = None
        self.exif_data = None
        self.filepath = None
        self.left_num_rotation = 0
        self.right_num_rotation = 0
        self.num_rotations = 0
        self.angle = 0

    # Function to open an image file and extract EXIF data
    def open_image(self, filepath):
        self.num_rotations = 0
        with Image.open(filepath) as img:
            self.filepath = filepath
            self.image = QPixmap(filepath)
            self.exif_data = img._getexif()

    # Function to set the image rotation angle to 90 degrees clockwise
    def set_Rightangle(self):
        self.right_num_rotation =1
        self.num_rotations = self.right_num_rotation
        self.angle = 90

   # Function to set the image rotation angle to 90 degrees counterclockwise
    def set_Leftangle(self):
        self.left_num_rotation =1
        self.num_rotations = self.left_num_rotation
        self.angle = -90

    # Function to save the current image to a file
    def save_image(self, filepath):
       self.image.save(filepath)

    # Function to get the current image
    def get_image(self):
        return self.image

    # Function to get the rotated image based on the current angle
    def get_rotated_image(self):
        angle = self.num_rotations * self.angle 
        trans = QTransform()
        trans.rotate(angle)
        self.image = self.image.transformed(trans)
        return self.image
    
    # Function to get the EXIF data of the image
    def get_exif_data(self):
        if self.exif_data:
            return self.exif_data
        else:
            'No EXIF data found.'
        
    # Function to map EXIF tag keys to their corresponding human-readable names
    def exif_key(self,key):
        return ExifTags.TAGS.get(key,key)
    
    # Function to extract and format GPS information from EXIF data
    def manage_gps_info(self,data):
        if data is not None:
            canGetGeolocalization = True
            gps_Info = {}

            # Extract specific GPS information from EXIF data
            if(data.get(0) is not None):
                gps_Info['GPSVersionID'] = data.get(0)
            if (data.get(1) is not None):
                gps_Info['GPSLatitudeRef'] = data.get(1)
            else:
                canGetGeolocalization = False
            if (data.get(2) is not None):
                gps_Info['GPSLatitude'] = data.get(2)
            else:
                canGetGeolocalization = False
            if (data.get(3) is not None):
                gps_Info['GPSLongitudeRef'] = data.get(3)
            else:
                canGetGeolocalization = False
            if (data.get(4) is not None):
                gps_Info['GPSLongitude'] = data.get(4)
            else:
                canGetGeolocalization = False
            if (data.get(5) is not None):
                gps_Info['GPSAltitudeRef'] = data.get(5)
            if(data.get(6) is not None):
                gps_Info['GPSAltitude'] = data.get(6)
            if (data.get(7) is not None):
                gps_Info['GPSTimeStamp'] = data.get(7)
            if(data.get(8) is not None):
                gps_Info['GPSSatellites'] = data.get(8)
            if(data.get(9) is not None):
                gps_Info['GPSStatus'] = data.get(9)
            if (data.get(10) is not None):
                gps_Info['GPSMeasureMode'] = data.get(10)
            if (data.get(11) is not None):
                gps_Info['GPSDOP'] = data.get(11)
            if (data.get(12) is not None):
                gps_Info['GPSSpeedRef'] = data.get(12)
            if (data.get(13) is not None):
                gps_Info['GPSSpeed'] = data.get(13)
            if (data.get(14) is not None):
                gps_Info['GPSTrackRef'] = data.get(14)
            if (data.get(15) is not None):
                gps_Info['GPSTrack'] = data.get(15)
            if (data.get(16) is not None):
                gps_Info['GPSImgDirectionRef'] = data.get(16)
            if (data.get(17) is not None):
                gps_Info['GPSMapDatum'] = data.get(17)
            if (data.get(18) is not None):
                gps_Info['GPSDestLatitudeRef'] = data.get(18)
            if (data.get(19) is not None):
                gps_Info['GPSDestLatitude'] = data.get(19)
            if (data.get(20) is not None):
                gps_Info['GPSDestLatitude'] = data.get(20)
            if (data.get(21) is not None):
                gps_Info['GPSDestLongitude'] = data.get(21)
            if (data.get(22) is not None):
                gps_Info['GPSDestBearingRef'] = data.get(22)
            if (data.get(23) is not None):
                gps_Info['GPSDestBearing'] = data.get(23)
            if (data.get(24) is not None):
                gps_Info['GPSDestDistanceRef'] = data.get(24)
            if (data.get(25) is not None):
                gps_Info['GPSDestDistance'] = data.get(25)
            if (data.get(26) is not None):
                gps_Info['GPSProcessingMethod'] = data.get(26)
            if (data.get(27) is not None):
                gps_Info['GPSAreaInformation'] = data.get(27)
            if (data.get(28) is not None):
                gps_Info['GPSDateStamp'] = data.get(28)
            if (data.get(29) is not None):
                gps_Info['GPSDifferential'] = data.get(29)
            if (data.get(30) is not None):
                gps_Info['GPSHPositioningError'] = data.get(30)
            if data.get(31) is not None:
                gps_Info['GPSHPositioningError'] = data.get(31)
            
            # Continue extracting other GPS information as needed
            if(canGetGeolocalization):
                Lat_values =tuple(gps_Info['GPSLatitude'])
                latitude = str(int(Lat_values[0])) + '°' + str(int(Lat_values[1])) + '\'' + str(Lat_values[2]) + '\"'
                cardinal_lat = str(gps_Info['GPSLatitudeRef'])
                Lon_values = tuple(gps_Info['GPSLongitude'])
                longitude = str(int(Lon_values[0])) + '°' + str(int(Lon_values[1])) + '\'' + str(Lon_values[2]) + '\"'
                cardinal_lon = str(gps_Info['GPSLongitudeRef'])
                importantGPSInfos = "https://www.google.com/maps/place/"  + latitude + cardinal_lat + longitude + cardinal_lon

                return importantGPSInfos
            else:
                return None
        else:
            return None
