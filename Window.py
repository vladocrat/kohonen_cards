from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel, QFormLayout, \
    QCheckBox, QPushButton, QFileDialog


class Row(QWidget):

    def __init__(self, name, validator, validator_required=False):
        super().__init__()

        self.row = QHBoxLayout()
        self.edit = QLineEdit("")

        if validator_required:
            self.edit.setValidator(validator)

        self.label = QLabel(name)
        self.row.addWidget(self.label)
        self.row.addWidget(self.edit)
        self.setLayout(self.row)


class Window(QWidget):
    """learning_rate, learning_rate_step, filepath, epoch counter, outputs_counter"""
    calculate = pyqtSignal(float, float, str, int, int)
    file = ""

    def __init__(self):
        super().__init__()

        layout = QFormLayout(self)

        self.learning_rate_step = Row(name="Learning rate step: ", validator_required=True, validator=QtGui.QDoubleValidator())
        self.random_learning_rate = QCheckBox("Random learning rate?")
        self.learning_rate = Row(name="Learning rate: ", validator_required=True, validator=QtGui.QDoubleValidator())
        self.epoch_counter = Row(name="Epochs: ", validator_required=True, validator=QtGui.QIntValidator())
        self.epoch_counter.edit.setText("100")
        self.outputs_count = Row(name="Outputs: ", validator_required=True, validator=QtGui.QIntValidator())
        self.outputs_count.edit.setText("4")

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_inner)
        load_file_button = QPushButton("Load File")
        load_file_button.clicked.connect(self.choose_file)

        self.random_learning_rate.stateChanged.connect(lambda state: self.learning_rate.setEnabled(state != 2))

        layout.addWidget(self.outputs_count)
        layout.addWidget(self.epoch_counter)
        layout.addWidget(self.learning_rate)
        layout.addWidget(self.learning_rate_step)
        layout.addWidget(self.random_learning_rate)
        layout.addWidget(load_file_button)
        layout.addWidget(calculate_button)

        self.setLayout(layout)
        self.setWindowTitle('')
        self.setGeometry(300, 300, 400, 200)

    def choose_file(self):
        self.file = QFileDialog.getOpenFileName(self, "Choose file", filter="Text files (*.txt)")

    def calculate_inner(self):
        if len(self.file) == 0:
            return

        if len(self.epoch_counter.edit.text()) == 0:
            return

        if len(self.outputs_count.edit.text()) == 0:
            return

        epochs = int(self.epoch_counter.edit.text())
        outputs = int(self.outputs_count.edit.text())

        if self.random_learning_rate.isChecked():
            if len(self.learning_rate_step.edit.text()) > 0:
                learning_rate_step = float(self.learning_rate_step.edit.text())
                self.calculate.emit(0, learning_rate_step, self.file[0], epochs, outputs)
        else:
            if len(self.learning_rate.edit.text()) > 0 and len(self.learning_rate_step.edit.text()) > 0:
                learning_rate = float(self.learning_rate.edit.text())
                learning_rate_step = float(self.learning_rate_step.edit.text())
                self.calculate.emit(learning_rate, learning_rate_step, self.file[0], epochs, outputs)

