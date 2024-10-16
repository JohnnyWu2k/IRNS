import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QCheckBox, QComboBox
from PyQt5.QtCore import Qt
import mpmath
import os

class IrrationalSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Irrational Number Search")

        # Set up layout and central widget
        layout = QVBoxLayout()

        # Label and combobox to select irrational number
        self.num_label = QLabel("Select the irrational number:")
        layout.addWidget(self.num_label)

        self.num_selector = QComboBox(self)
        self.num_selector.addItems(["Pi (π)", "Euler's Number (e)", "Square Root (√n)"])
        layout.addWidget(self.num_selector)

        # Input for square root n (only used if √n is selected)
        self.sqrt_n_label = QLabel("Enter the value of n for √n (if applicable):")
        layout.addWidget(self.sqrt_n_label)
        self.sqrt_n_input = QLineEdit(self)
        layout.addWidget(self.sqrt_n_input)

        # Label and input for target number
        self.target_label = QLabel("Enter the number segment to search:")
        layout.addWidget(self.target_label)

        self.target_input = QLineEdit(self)
        layout.addWidget(self.target_input)

        # Checkbox to search all results
        self.search_all_checkbox = QCheckBox("Search all occurrences")
        layout.addWidget(self.search_all_checkbox)

        # Label and input for digits (10^n)
        self.digits_label = QLabel("Enter the value of n (for 10^n digits):")
        layout.addWidget(self.digits_label)

        self.digits_input = QLineEdit(self)
        layout.addWidget(self.digits_input)

        # Button to start search
        self.search_button = QPushButton("Start Search", self)
        self.search_button.clicked.connect(self.start_search)
        layout.addWidget(self.search_button)

        # Set layout in the central widget
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_search(self):
        # Get the input values
        target = self.target_input.text().strip()
        try:
            n = int(self.digits_input.text().strip())
            digits = 10 ** n
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid integer for n.")
            return
        
        search_all = self.search_all_checkbox.isChecked()

        # Select the irrational number
        selected_num = self.num_selector.currentText()

        # Compute the chosen irrational number
        irrational_str = self.compute_irrational_number(selected_num, digits)

        if not irrational_str:
            return  # If there was an error in computation

        # Display estimated time
        estimated_time = (digits / 10 ** 6) * (5 if search_all else 2)
        QMessageBox.information(self, "Estimated Time", f"Estimated search time: {estimated_time:.2f} seconds.")

        # Perform the search
        if search_all:
            self.search_all_occurrences(irrational_str, target)
        else:
            self.search_first_occurrence(irrational_str, target)

    def compute_irrational_number(self, selected_num, digits):
        # Compute based on the selected irrational number
        try:
            mpmath.mp.dps = digits  # Set precision for mpmath
            if selected_num == "Pi (π)":
                return str(mpmath.pi)[2:]  # Remove the integer part '3.'
            elif selected_num == "Euler's Number (e)":
                return str(mpmath.e)[2:]  # Remove the integer part '2.'
            elif selected_num == "Square Root (√n)":
                try:
                    n_value = int(self.sqrt_n_input.text().strip())
                    return str(mpmath.sqrt(n_value))[2:]  # Compute √n and remove integer part
                except ValueError:
                    QMessageBox.critical(self, "Error", "Please enter a valid integer for √n.")
                    return None
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in computing {selected_num}: {str(e)}")
            return None

    def search_first_occurrence(self, irrational_str, target):
        # Search for the first occurrence
        position = irrational_str.find(target)
        if position == -1:
            QMessageBox.information(self, "Search Result", f"Number segment '{target}' not found.")
        else:
            context = irrational_str[max(0, position - 5):position + len(target) + 5]
            QMessageBox.information(self, "Search Result", f"Found at position {position + 1}.\nContext: {context}")

    def search_all_occurrences(self, irrational_str, target):
        positions = []
        start = 0
        while True:
            position = irrational_str.find(target, start)
            if position == -1:
                break
            positions.append(position)
            start = position + 1

        if not positions:
            QMessageBox.information(self, "Search Result", f"Number segment '{target}' not found.")
        else:
            # Save results to a new text file
            with open("results.txt", "w") as f:
                f.write(f"Found {len(positions)} occurrences of '{target}':\n\n")
                for pos in positions:
                    context = irrational_str[max(0, pos - 5):pos + len(target) + 5]
                    f.write(f"Position {pos + 1}, Context: {context}\n")
            QMessageBox.information(self, "Search Result", f"Found {len(positions)} occurrences. Results saved to results.txt.")

def main():
    app = QApplication(sys.argv)
    window = IrrationalSearchApp()
    window.resize(400, 400)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
