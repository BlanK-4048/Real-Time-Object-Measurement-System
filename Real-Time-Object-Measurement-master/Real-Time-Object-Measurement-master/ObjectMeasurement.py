import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import utlis
from tkinter import ttk

class ObjectMeasurementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Measurement")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='lightgrey')

        self.setup_gui()

    def setup_gui(self):

        style = ttk.Style()
        style.configure("TButton",
                        foreground="midnight blue",
                        background="lightgrey",
                        font=("Helvetica", 16),
                        padding=10)
        # Left Section
        left_frame = tk.Frame(self.root, bg='lightgrey', padx=20)  # Add padx=20 for padding on the left side
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        title_label = tk.Label(left_frame, text="REAL TIME \n OBJECT MEASUREMENT", font=("Helvetica", 25), bg='lightgrey')
        title_label.pack(pady=(20, 10))

        select_button = ttk.Button(left_frame, text="Select Image", command=self.get_measurement,padding=(10,10))
        select_button.pack(pady=(200, 50))

        close_button = ttk.Button(left_frame, text="Close Application", command=self.on_close,padding=10)
        close_button.pack(pady=(10, 20))


        # Middle Section
        self.middle_frame = tk.Frame(self.root, bg='lightgrey')
        self.middle_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        original_label = tk.Label(self.middle_frame, text="ORIGINAL IMAGE", font=("Helvetica", 14))
        original_label.pack(pady=10)

        self.original_label = tk.Label(self.middle_frame)
        self.original_label.pack(pady=(0, 20))

        # Right Section
        self.right_frame = tk.Frame(self.root, bg='lightgrey')
        self.right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        output_label = tk.Label(self.right_frame, text="OBJECT MEASUREMENT", font=("Helvetica", 14))
        output_label.pack(pady=10)

        self.output_label = tk.Label(self.right_frame)
        self.output_label.pack(pady=(0, 20))

    def get_measurement(self):
        file_path = filedialog.askopenfilename(initialdir="./", title="Select Image", filetypes=(
        ("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")))

        if file_path:
            img = cv2.imread(file_path)

            imgContours, conts = utlis.getContours(img, minArea=50000, filter=4)
            if len(conts) != 0:
                biggest = conts[0][2]
                scale = 3
                wP = 210 * scale
                hP = 297 * scale

                imgWarp = utlis.warpImg(img, biggest, wP, hP)
                imgContours2, conts2 = utlis.getContours(imgWarp,
                                                         minArea=2000, filter=4,
                                                         cThr=[50, 50], draw=False)
                if len(conts2) != 0:
                    for obj in conts2:
                        nPoints = utlis.reorder(obj[2])
                        nW = round((utlis.findDis(nPoints[0][0] // scale, nPoints[1][0] // scale) / 10), 1)
                        nH = round((utlis.findDis(nPoints[0][0] // scale, nPoints[2][0] // scale) / 10), 1)
                        cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                        (nPoints[1][0][0], nPoints[1][0][1]),
                                        (255, 0, 255), 3, 8, 0, 0.05)
                        cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                        (nPoints[2][0][0], nPoints[2][0][1]),
                                        (255, 0, 255), 3, 8, 0, 0.05)
                        x, y, w, h = obj[3]
                        cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                    (255, 0, 255), 2)
                        cv2.putText(imgContours2, '{}cm'.format(nH), (x - 70, y + h // 2),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                    1.5,
                                    (255, 0, 255), 2)

                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(img)
                    img = ImageTk.PhotoImage(image=img.resize((525, 725)))  # Set size of original image

                    self.original_label.config(image=img)
                    self.original_label.image = img

                    imgContours2 = cv2.cvtColor(imgContours2, cv2.COLOR_BGR2RGB)
                    imgContours2 = Image.fromarray(imgContours2)
                    imgContours2 = ImageTk.PhotoImage(image=imgContours2.resize((525, 725)))  # Set size of output image

                    self.output_label.config(image=imgContours2)
                    self.output_label.image = imgContours2

    def on_close(self):
        self.root.destroy()


def main():
    root = tk.Tk()
    app = ObjectMeasurementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
