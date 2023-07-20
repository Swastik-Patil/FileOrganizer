import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QListWidget, QMessageBox


class FileOrganizerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        header_label = QLabel("File Organizer", self)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header_label)

        self.file_list_widget = QListWidget(self)
        layout.addWidget(self.file_list_widget)

        select_directory_button = QPushButton("Select Directory", self)
        select_directory_button.clicked.connect(self.select_directory)
        layout.addWidget(select_directory_button)

        organize_button = QPushButton("Organize Files", self)
        organize_button.clicked.connect(self.organize_files)
        layout.addWidget(organize_button)

        self.source_dir = ""

    def select_directory(self):
        self.file_list_widget.clear();
        self.source_dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        if self.source_dir:
            self.populate_file_list()

    def populate_file_list(self):
        self.file_list_widget.clear()
        self.files = os.listdir(self.source_dir)
        self.file_list_widget.addItems(self.files)
        
    def createfolder(self,foldername):
        if not os.path.exists(foldername):
            os.makedirs(foldername)

    def move(self,foldername,files):
        for file in files:
            os.replace(file, f"{foldername}/{file}")

    def organize_files(self):
        if not self.source_dir:
            QMessageBox.warning(self, "Warning", "Please select a directory.")
            return

        imgext = [".png", ".jpg", ".jpeg", ".gif"]
        medext = [".mpg", ".mp4", ".mpeg", ".mp3", ".mkv", ".avi"]
        rarext = [".rar", ".zip", ".7z"]
        codext = [".py", ".js", ".css", ".html", ".c", ".cpp", ".java", ".r"]
        docsext = [".docs", ".ppt", ".pdf", ".md", ".doc", ".docx", ".txt"]
        softext = [".exe", ".msi"]

        image = []
        media = []
        rar = []
        code = []
        docs = []
        soft = []
        other = []

        for file in self.files:
            if file == "fileOrganizer.py":
                continue
            e = os.path.splitext(file)[1]
            if e in imgext:
                self.createfolder("Images")
                image.append(file)
            elif e in medext:
                self.createfolder("Media")
                media.append(file)
            elif e in rarext:
                self.createfolder("RAR/ZIP")
                rar.append(file)
            elif e in codext:
                self.createfolder("Code")
                code.append(file)
            elif e in docsext:
                self.createfolder("Docs")
                docs.append(file)
            elif e in softext:
                self.createfolder("Softwares")
                soft.append(file)
            else:
                self.createfolder("Others")
                if(os.path.isfile(file)):
                    other.append(file)

        self.move("Images", image)
        self.move("Media", media)
        self.move("RAR/ZIP", rar)
        self.move("Softwares", soft)
        self.move("Code", code)
        self.move("Docs", docs)
        self.move("Others", other)

        QMessageBox.information(self, "File Organizer", "File organization completed!")
        self.file_list_widget.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerUI()
    window.show()
    sys.exit(app.exec_())
    