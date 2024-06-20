from control import Controller
from model import Model
from view import View
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication([])
    model = Model()
    view = View(model)
    controller = Controller(model, view)
    view.show()
    app.exec()


if __name__ == "__main__":
    main()
