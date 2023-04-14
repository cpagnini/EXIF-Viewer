import sys
import Controller, Model, View


from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model.ImageModel()
    view = View.ImageViewer()
    controller = Controller.ImageController(model, view)
    view.show()
    sys.exit(app.exec_())
