import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal,QSize

import speech_recognition as sr
from google_trans_new import google_translator
from gtts import gTTS
import pyttsx3

class InfiniteLoopThread(QThread):
    output_signal = Signal(str)  # Signal to send a string

    def run(self):
        r = sr.Recognizer()
        translator = google_translator()
        tts = pyttsx3.init()
        language = "en"
        output_string = "Running..."  # Replace with your dynamic output
        #self.output_signal.emit("Infinite loop started")  # Emit a string
        while not self.isInterruptionRequested():
            with sr.Microphone() as source:
                print("Speak/Play Audio Now!")
                r.adjust_for_ambient_noise(source,duration = 1)
                #audio = r.listen(source,timeout=7)
                audio = r.listen(source)
                try:
                    speech_text = r.recognize_google(audio)
                    print(speech_text)        
                
                    #translate text aquired    

                    output_string = translator.translate(speech_text,lang_tgt=f'{language}')
                    print(output_string)
                    tts.say(output_string)
                    tts.runAndWait()
            
                except sr.UnknownValueError:
                    print("Could not process/understand audio")
                except sr.RequestError:
                    print("Could not request result from Google")
                except sr.WaitTimeoutError:
                    print("No audio detected for the time limit")

                print("Running...")
                self.output_signal.emit(output_string)
                time.sleep(1)


        

        
        
        time.sleep(1)
       # self.output_signal.emit("Infinite loop stopped")

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Button Example")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        label = QLabel("Status:")
        layout.addWidget(label)

        self.status_label = QLabel("Stopped")
        layout.addWidget(self.status_label)

        self.start_stop_button = QPushButton(self)
        self.start_stop_button.setIconSize(QSize(100, 100))
        self.start_stop_button.setFixedSize(100, 100)
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.clicked.connect(self.toggle_infinite_loop)

        pixmap = QPixmap("recButton.jpg")
        self.start_stop_button.setIcon(pixmap)

        layout.addWidget(self.start_stop_button)

        
        #self.setGeometry(100, 100, 400, 200)
      

        label = QLabel("Translation text:")
       
        layout.addWidget(label)


        self.text_box = QLineEdit()
        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)

        self.text_box.textChanged.connect(self.adjust_text_box_height)

        
        self.result_label = QLabel()
        layout.addWidget(self.result_label)   

        self.infinite_loop_thread = InfiniteLoopThread()
        self.infinite_loop_thread.output_signal.connect(self.on_output_received)


    def adjust_text_box_height(self):
        text = self.text_box.text()
        font_metrics = self.text_box.fontMetrics()
        text_width = font_metrics.boundingRect(text).width()
        text_height = font_metrics.boundingRect(text).height()

        # Set a minimum height to ensure it's not too small
        min_height = 40

        # Set the height to the maximum of the calculated text height and the minimum height
        new_height = max(text_height, min_height)

        self.text_box.setFixedHeight(new_height)

    def toggle_infinite_loop(self):
        if self.start_stop_button.isChecked():
            
            self.status_label.setText("Running")
            self.infinite_loop_thread.start()
        else:
            
            self.status_label.setText("Stopped")
            self.infinite_loop_thread.requestInterruption()

    def on_output_received(self, output_string):
        self.text_box.setText(output_string)

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
