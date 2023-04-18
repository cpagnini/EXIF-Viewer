import PIL
from PIL import Image,ExifTags
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
            return self.exif_data
        else:
            'No EXIF data found.'
       
        #     exif_str = ''
        #     for tag_id in sorted(self.exif_data):
        #         # Check if tag_id is for GPS coordinates
        #         tag_name = ExifTags.TAGS.get(tag_id, tag_id)
        #         tag_value = self.exif_data.get(tag_id)
        #         if (tag_name == "GPSInfo"):
        #             tag_value = self.getGPS(tag_value)
        #         if isinstance(tag_value, bytes):
        #             try:
        #                 tag_value = tag_value.decode('utf-8')
        #             except UnicodeDecodeError:
        #                 tag_value = tag_value.decode('utf-8', 'replace')
        #         exif_str += f'{tag_name}: {tag_value}\n'
        #     exif_str += f'\n'
        #     print(exif_str)
        #     return exif_str
        # else:
        #     return 'No EXIF data found.'

    def exif_key(self,key):
        return ExifTags.TAGS.get(key,key)
    
    def manage_gps_info(self,data):
        if data is not None:
            #create dictonary of all GPS infos
            gps_Info = {}

            # Check about all the infos about GPS https://exiftool.org/TagNames/GPS.html
            if(data.get(0) is not None):
                gps_Info['GPSVersionID'] = data.get(0)
            if (data.get(1) is not None):
                gps_Info['GPSLatitudeRef'] = data.get(1)
            if (data.get(2) is not None):
                gps_Info['GPSLatitude'] = data.get(2)
            if (data.get(3) is not None):
                gps_Info['GPSLongitudeRef'] = data.get(3)
            if (data.get(4) is not None):
                gps_Info['GPSLongitude'] = data.get(4)
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
            # if (data.get(20) is not None):
            #     gps_Info['GPSDestLatitude'] = data.get(20)
            # if (data.get(21) is not None):
            #     gps_Info['GPSDestLongitude'] = data.get(21)
            # if (data.get(22) is not None):
            #     gps_Info['GPSDestBearingRef'] = data.get(22)
            # if (data.get(23) is not None):
            #     gps_Info['GPSDestBearing'] = data.get(23)
            # if (data.get(24) is not None):
            #     gps_Info['GPSDestDistanceRef'] = data.get(24)
            # if (data.get(25) is not None):
            #     gps_Info['GPSDestDistance'] = data.get(25)
            # if (data.get(26) is not None):
            #     gps_Info['GPSProcessingMethod'] = data.get(26)
            # if (data.get(27) is not None):
            #     gps_Info['GPSAreaInformation'] = data.get(27)
            # if (data.get(28) is not None):
            #     gps_Info['GPSDateStamp'] = data.get(28)
            # if (data.get(29) is not None):
            #     gps_Info['GPSDifferential'] = data.get(29)
            # if (data.get(30) is not None):
            #     gps_Info['GPSHPositioningError'] = data.get(30)

            Lat_values =tuple(gps_Info['GPSLatitude'])
            latitude = str(int(Lat_values[0])) + '°' + str(int(Lat_values[1])) + '\'' + str(Lat_values[2]) + '\"'
            cardinal_lat = str(gps_Info['GPSLatitudeRef'])
            Lon_values = tuple(gps_Info['GPSLongitude'])
            longitude = str(int(Lon_values[0])) + '°' + str(int(Lon_values[1])) + '\'' + str(Lon_values[2]) + '\"'
            cardinal_lon = str(gps_Info['GPSLongitudeRef'])
            importantGPSInfos = "https://www.google.com/maps/place/"  + latitude + cardinal_lat + longitude + cardinal_lon


        return importantGPSInfos
