import cv2
from SpeedTracker import *
import numpy as np
import PIL
from PIL import ImageTk
from PIL import Image
import tkinter as tk
import os
from ultralytics import YOLO
import time
import numpy as np
import cvzone
import math
from sort import *

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
fy1=200
fy2=900
fx1=0
fx2=900
video_dir="./Resources/recv20.mp4"
class CustomFrame(tk.Frame):
    def __init__(self,master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create a label widget to display the video
        self.label = tk.Label(self)
        self.label.grid(row=0, column=2,rowspan=30)

        self.button1 = tk.Button(self,text='Submit',command = self.changeValues)
        self.button1.grid(row=11, column=4)

        self.labelLSX1 = tk.Label(self,text='Left Start X1:')
        self.labelLSX1.grid(row=0, column=0)
        self.inputLSX1 = tk.Text(self,height = 1.2,width = 10)
        self.inputLSX1.grid(row=1, column=0)

        self.labelLSY1 = tk.Label(self,text='Left Start Y1:')
        self.labelLSY1.grid(row=0, column=1)
        self.inputLSY1 = tk.Text(self,height = 1.2,width = 10)
        self.inputLSY1.grid(row=1, column=1)

        self.labelRSX1 = tk.Label(self,text='Right Start X1:')
        self.labelRSX1.grid(row=0, column=3)
        self.inputRSX1 = tk.Text(self,height = 1.2,width = 10)
        self.inputRSX1.grid(row=1, column=3)

        self.labelRSY1 = tk.Label(self,text='Right Start Y1:')
        self.labelRSY1.grid(row=0, column=4)
        self.inputRSY1 = tk.Text(self,height = 1.2,width = 10)
        self.inputRSY1.grid(row=1, column=4)

        #start x1
        self.labelLSX2 = tk.Label(self,text='Left Start X2:')
        self.labelLSX2.grid(row=2, column=0)
        self.inputLSX2 = tk.Text(self,height = 1.2,width = 10)
        self.inputLSX2.grid(row=3, column=0)

        self.labelLSY2 = tk.Label(self,text='Left Start Y2:')
        self.labelLSY2.grid(row=2, column=1)
        self.inputLSY2 = tk.Text(self,height = 1.2,width = 10)
        self.inputLSY2.grid(row=3, column=1)

        self.labelRSX2 = tk.Label(self,text='Right Start X2:')
        self.labelRSX2.grid(row=2, column=3)
        self.inputRSX2 = tk.Text(self,height = 1.2,width = 10)
        self.inputRSX2.grid(row=3, column=3)

        self.labelRSY2 = tk.Label(self,text='Right Start Y2:')
        self.labelRSY2.grid(row=2, column=4)
        self.inputRSY2 = tk.Text(self,height = 1.2,width = 10)
        self.inputRSY2.grid(row=3, column=4)


        #end
        self.labelLEX1 = tk.Label(self,text='Left End X1:')
        self.labelLEX1.grid(row=4, column=0)
        self.inputLEX1 = tk.Text(self,height = 1.2,width = 10)
        self.inputLEX1.grid(row=5, column=0)

        self.labelLEY1 = tk.Label(self,text='Left End Y1:')
        self.labelLEY1.grid(row=4, column=1)
        self.inputLEY1 = tk.Text(self,height = 1.2,width = 10)
        self.inputLEY1.grid(row=5, column=1)

        self.labelREX1 = tk.Label(self,text='Right End X1:')
        self.labelREX1.grid(row=4, column=3)
        self.inputREX1 = tk.Text(self,height = 1.2,width = 10)
        self.inputREX1.grid(row=5, column=3)

        self.labelREY1 = tk.Label(self,text='Right End Y1:')
        self.labelREY1.grid(row=4, column=4)
        self.inputREY1 = tk.Text(self,height = 1.2,width = 10)
        self.inputREY1.grid(row=5, column=4)

        #end x2
        self.labelLEX2 = tk.Label(self,text='Left End X2:')
        self.labelLEX2.grid(row=6, column=0)
        self.inputLEX2 = tk.Text(self,height = 1.2,width = 10)
        self.inputLEX2.grid(row=7, column=0)

        self.labelLEY2 = tk.Label(self,text='Left End Y2:')
        self.labelLEY2.grid(row=6, column=1)
        self.inputLEY2 = tk.Text(self,height = 1.2,width = 10)
        self.inputLEY2.grid(row=7, column=1)

        self.labelREX2 = tk.Label(self,text='Right End X2:')
        self.labelREX2.grid(row=6, column=3)
        self.inputREX2 = tk.Text(self,height = 1.2,width = 10)
        self.inputREX2.grid(row=7, column=3)

        self.labelREY2 = tk.Label(self,text='Right End Y2:')
        self.labelREY2.grid(row=6, column=4)
        self.inputREY2 = tk.Text(self,height = 1.2,width = 10)
        self.inputREY2.grid(row=7, column=4)

        #frame text box
        self.labelFX1 = tk.Label(self,text='Frame X-left:')
        self.labelFX1.grid(row=8, column=0)
        self.inputFX1 = tk.Text(self,height = 1.2,width = 10)
        self.inputFX1.grid(row=9, column=0)

        self.labelFX2 = tk.Label(self,text='Frame X-right:')
        self.labelFX2.grid(row=8, column=1)
        self.inputFX2 = tk.Text(self,height = 1.2,width = 10)
        self.inputFX2.grid(row=9, column=1)

        self.labelFY1 = tk.Label(self,text='Frame Y-left:')
        self.labelFY1.grid(row=8, column=3)
        self.inputFY1 = tk.Text(self,height = 1.2,width = 10)
        self.inputFY1.grid(row=9, column=3)

        self.labelFY2 = tk.Label(self,text='Frame X-right:')
        self.labelFY2.grid(row=8, column=4)
        self.inputFY2 = tk.Text(self,height = 1.2,width = 10)
        self.inputFY2.grid(row=9, column=4)

        #text file
        self.text = tk.Text(self, height=12, width=30,)
        self.text.config(state=tk.DISABLED)
        self.text.grid(column=5, row=0, rowspan=33, sticky='nsew')
        

        #fps value
        self.labelFPV = tk.Label(self,text='FPS calculated Value:')
        self.labelFPV.grid(row=10, column=3 , columnspan=2)
        self.inputFPV = tk.Text(self,height = 1.2,width = 10)
        self.inputFPV.grid(row=11, column=3)

        #set value
        self.inputLSX1.insert(1.0,str(start_region_x[0]))
        self.inputLSY1.insert(1.0,str(start_region_y[0]))

        self.inputLSX2.insert(1.0,str(start_region_x[1]))
        self.inputLSY2.insert(1.0,str(start_region_y[1]))

        self.inputRSX1.insert(1.0,str(start_region_x[2]))
        self.inputRSY1.insert(1.0,str(start_region_y[2]))

        self.inputRSX2.insert(1.0,str(start_region_x[3]))
        self.inputRSY2.insert(1.0,str(start_region_y[3]))

        self.inputLEX1.insert(1.0,str(end_region_x[0]))
        self.inputLEY1.insert(1.0,str(end_region_y[0]))

        self.inputLEX2.insert(1.0,str(end_region_x[1]))
        self.inputLEY2.insert(1.0,str(end_region_y[1]))

        self.inputREX1.insert(1.0,str(end_region_x[2]))
        self.inputREY1.insert(1.0,str(end_region_y[2]))

        self.inputREX2.insert(1.0,str(end_region_x[3]))
        self.inputREY2.insert(1.0,str(end_region_y[3]))

        self.inputFX1.insert(1.0,str(fx1))
        self.inputFX2.insert(1.0,str(fx2))
        self.inputFY1.insert(1.0,str(fy1))
        self.inputFY2.insert(1.0,str(fy2))

        



        
        #self.create_window(200, 180, window=button1)



        # Create a VideoCapture object to read the video file
        self.cap = cv2.VideoCapture(video_dir)
        self.vfps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.model = YOLO("./TrainedModel/bestn.pt")
        self.classNames = ["Bike", "Auto", "Car", "Truck", "Bus", "Other Vehicle"]
        self.tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
        #Creater Tracker Object
        self.speedtracker = SpeedTracker()
        self.dim = (900, 900)
        self.inputFPV.insert(1.0,str(self.vfps))
        self.update()
    def changeValues(self):
        start_region_x[0]= int(self.inputLSX1.get(1.0, "end-1c"))
        start_region_x[1]=int(self.inputLSX2.get(1.0, "end-1c"))
        start_region_x[2]=int(self.inputRSX1.get(1.0, "end-1c"))
        start_region_x[3]=int(self.inputRSX2.get(1.0, "end-1c"))

        start_region_y[0]=int(self.inputLSY1.get(1.0, "end-1c"))
        start_region_y[1]=int(self.inputLSY2.get(1.0, "end-1c"))
        start_region_y[2]=int(self.inputRSY1.get(1.0, "end-1c"))
        start_region_y[3]=int(self.inputRSY2.get(1.0, "end-1c"))
        
        end_region_x[0]=int(self.inputLEX1.get(1.0, "end-1c"))
        end_region_x[1]=int(self.inputLEX2.get(1.0, "end-1c"))
        end_region_x[2]=int(self.inputREX1.get(1.0, "end-1c"))
        end_region_x[3]=int(self.inputREX2.get(1.0, "end-1c"))

        end_region_y[0]=int(self.inputLEY1.get(1.0, "end-1c"))
        end_region_y[1]=int(self.inputLEY2.get(1.0, "end-1c"))
        end_region_y[2]=int(self.inputREY1.get(1.0, "end-1c"))
        end_region_y[3]=int(self.inputREY2.get(1.0, "end-1c"))

        fx1=int(self.inputFX1.get(1.0, "end-1c"))
        fx2=int(self.inputFX2.get(1.0, "end-1c"))
        fy1=int(self.inputFY1.get(1.0, "end-1c"))
        fy2=int(self.inputFY2.get(1.0, "end-1c"))

        FPSCalc=int(self.inputFPV.get(1.0, "end-1c"))

    def update(self):
        ret, image = self.cap.read()
        if ret:
            image = cv2.resize(image, self.dim, fx=0.5, fy=0.5)
            H, W, _ = image.shape
            image = image[fy1:fy2,fx1:fx2]
            results = self.model(image, stream=True)
            detections = np.empty((0, 5))
            objects_rect = []


            for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        # Bounding Box
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
                        w, h = x2 - x1, y2 - y1

                        # Confidence
                        conf = math.ceil((box.conf[0] * 100)) / 100
                        # Class Name
                        cls = int(box.cls[0])
                        currentClass = self.classNames[cls]

                        if conf > 0.3:
                            currentArray = np.array([x1, y1, x2, y2, conf])
                            detections = np.vstack((detections, currentArray))

            resultsTracker = self.tracker.update(detections)

            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(result)
                w, h = x2 - x1, y2 - y1
                objects_rect.append([x1,y1,w,h,id])
                self.speedtracker.update(objects_rect)
                
                speed=self.speedtracker.getsp(id)
                if speed>self.speedtracker.limit():
                    cvzone.cornerRect(image, (x1, y1, w, h), l=9, rt=2, colorR=(97,105,255))
                    cx, cy = x1 + w // 2, y1 + h // 2
                    cv2.circle(image, (cx, cy), 5, (97,105,255), cv2.FILLED)
                    cvzone.putTextRect(image, f' {int(id), int(speed)}', (max(0, x1), max(35, y1)),
                                    scale=0.8, thickness=1, offset=5, colorR=(92,92,205))
                else:
                    cvzone.cornerRect(image, (x1, y1, w, h), l=9, rt=2, colorR=(50,205,50))
                    cx, cy = x1 + w // 2, y1 + h // 2
                    cv2.circle(image, (cx, cy), 5, (50,205,50), cv2.FILLED)
                    cvzone.putTextRect(image, f' {int(id), int(speed)}', (max(0, x1), max(35, y1)),
                                    scale=0.8, thickness=1, offset=5, colorR=(107,142,35))
                
                
                print(speed)
                
                if speed!=0:
                    self.speedtracker.exceededCapture(image, x1, y1, h, w, speed, id)
                    self.speedtracker.capture(image, x1, y1, h, w, speed, id)
                    self.speedtracker.dataTrack(speed, id)


            # DRAW LINES


            cv2.line(image, (start_region_x[0], start_region_y[0]), (start_region_x[1], start_region_y[1]), (0, 255, 0), 2)#left start
            cv2.line(image, (start_region_x[0], start_region_y[0]+30), (start_region_x[1], start_region_y[1]+30), (0, 255, 0), 2)

            cv2.line(image, (end_region_x[0], end_region_y[0]), (end_region_x[1], end_region_y[1]), (0, 0, 255), 2)#left end
            cv2.line(image, (end_region_x[0], end_region_y[0]+30), (end_region_x[1], end_region_y[1]+30), (0, 0, 255), 2)



            cv2.line(image, (start_region_x[2], start_region_y[2]), (start_region_x[3], start_region_y[3]), (0, 255, 0), 2)#right start
            cv2.line(image, (start_region_x[2], start_region_y[2]+30), (start_region_x[3], start_region_y[3]+30), (0, 255, 0), 2)

            
            cv2.line(image, (end_region_x[2], end_region_y[2]), (end_region_x[3], end_region_y[3]), (0, 0, 255), 2)#right end
            cv2.line(image, (end_region_x[2], end_region_y[2]+30), (end_region_x[3], end_region_y[3]+30), (0, 0, 255), 2)
            
            
            #DISPLAY
            #cv2.imshow('Frame',image)
            #cv2.waitKey(1)
            # ret, frame = self.cap.read()
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img)

            # Convert the PIL image to a Tkinter-compatible image
            tk_img = ImageTk.PhotoImage(pil_img)

            # Set the image on the label widget
            self.label.config(image=tk_img)
            self.label.image = tk_img
            update_text(self)
            self.after(1000 // self.vfps, self.update)
        else:
            self.cap = cv2.VideoCapture(video_dir)
            self.update()
prev_contents = ""
def update_text(self):
    global prev_contents
    # Open text file and read contents
 
    with open("./TrafficRecord/SpeedRecord.txt", "r") as file:
        data = file.read()
    
    # Find new data
    new_data = data[len(prev_contents):]
    
    # Insert new data into Text widget
    if new_data:
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, new_data)
        self.text.config(state=tk.DISABLED)
        
    # Update previous contents
    prev_contents = data

if __name__ == "__main__":
    # Create a tkinter window and a custom frame
    root = tk.Tk()
    root.title("Speed Detection V1.0")
    photo = tk.PhotoImage(file = "nkp-ico.png")
    root.iconphoto(False, photo)
    frame = CustomFrame(root)

    # Set the size of the frame and make it visible
    frame.config(width=800, height=600, background="#c0c0c0")
    frame.pack()

    # Start the tkinter event loop
    root.mainloop()