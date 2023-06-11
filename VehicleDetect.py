import tkinter
import tkinter.messagebox
import customtkinter
import cv2
from SpeedTracker import *
import PIL
from PIL import ImageTk
from PIL import Image
import os
from ultralytics import YOLO
import time
import numpy
import cvzone
import math
from sort import *

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

video_dir="./Resources/recv20.mp4"

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class CustomFrame(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("SKYHAWK-Speed-Violation-Detection-V1.0")
        self.captureAll=False
        self.captureExceed=True
        self.recordVideo=False
        self.recordFlag=False
        self.geometry(f"{1250}x{650}")  # dimension of display screen

        # configure grid layout (4x4)
        self.grid_columnconfigure((1,4), weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2,3,4,5,6), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,9,10,11,12), weight=1)


        # side tabview
        self.tabview = customtkinter.CTkTabview(self.sidebar_frame,height=200,
        segmented_button_selected_color= "#003158",
        segmented_button_selected_hover_color= "#003158",
        segmented_button_unselected_color="#29577e",
        segmented_button_fg_color="#29577e",
       
        border_color="#5e6b7b",
        width=180
        )
        self.tabview.grid(row=0, column=0, padx=(2, 2), pady=(3, 0), sticky="nsew")
       
        self.tabview.add("Con\nfig")
        self.tabview.add("Left\nStart")
        self.tabview.add("Left\nEnd")
        self.tabview.add("Right\nStart")
        self.tabview.add("Right\nEnd")
        
        self.tabview.tab("Con\nfig").grid_columnconfigure((0), weight=1)  # configure INPUTS OF CONFIG
        self.labelspeed = customtkinter.CTkLabel(self.tabview.tab("Con\nfig"), text="Speed Limit:")
        self.labelspeed.grid(row=0, column=0, padx=5, pady=5)
        self.labelppm = customtkinter.CTkLabel(self.tabview.tab("Con\nfig"), text="Pixel per Miter:")
        self.labelppm.grid(row=0, column=1, padx=5, pady=5)
        self.inputspeed = customtkinter.CTkEntry(self.tabview.tab("Con\nfig"),placeholder_text = "Enter Speed Limit", width=90, font=('calibre',10,'normal'))
        self.inputspeed.grid(row=1, column=0, padx=5, pady=(0, 0))
        self.inputppm = customtkinter.CTkEntry(self.tabview.tab("Con\nfig"),placeholder_text = "Enter Pixel per Miter", width=90, font=('calibre',10,'normal'))
        self.inputppm.grid(row=1, column=1, padx=5, pady=(0, 0))
       

        self.tabview.tab("Left\nStart").grid_columnconfigure((0), weight=1)  # configure INPUTS OF LEFT SIDE START LINE
        self.labelLS1stX1 = customtkinter.CTkLabel(self.tabview.tab("Left\nStart"), text="Left Start X1:")
        self.labelLS1stX1.grid(row=0, column=0, padx=5, pady=5)
        self.labelLS1stY1 = customtkinter.CTkLabel(self.tabview.tab("Left\nStart"), text="Left Start Y1:")
        self.labelLS1stY1.grid(row=0, column=1, padx=5, pady=5)
        self.inputLSX1 = customtkinter.CTkEntry(self.tabview.tab("Left\nStart"),placeholder_text = "Enter Left Start X1", width=90, font=('calibre',10,'normal'))
        self.inputLSX1.grid(row=1, column=0, padx=5, pady=(0, 0))
        self.inputLSY1 = customtkinter.CTkEntry(self.tabview.tab("Left\nStart"),placeholder_text = "Enter Left Start Y1", width=90, font=('calibre',10,'normal'))
        self.inputLSY1.grid(row=1, column=1, padx=5, pady=(0, 0))
        self.labelLS1stX2 = customtkinter.CTkLabel(self.tabview.tab("Left\nStart"), text="Left Start X2:")
        self.labelLS1stX2.grid(row=2, column=0, padx=5, pady=5)
        self.labelLS1stY2 = customtkinter.CTkLabel(self.tabview.tab("Left\nStart"), text="Left Start Y2:")
        self.labelLS1stY2.grid(row=2, column=1, padx=5, pady=5)
        self.inputLSX2 = customtkinter.CTkEntry(self.tabview.tab("Left\nStart"),placeholder_text = "Enter Left Start X2", width=90, font=('calibre',10,'normal'))
        self.inputLSX2.grid(row=3, column=0, padx=5, pady=(0, 0))
        self.inputLSY2 = customtkinter.CTkEntry(self.tabview.tab("Left\nStart"),placeholder_text = "Enter Left Start Y2", width=90, font=('calibre',10,'normal'))
        self.inputLSY2.grid(row=3, column=1, padx=5, pady=(0, 0))



        self.tabview.tab("Left\nEnd").grid_columnconfigure((0,1), weight=1)  # configure INPUTS OF LEFT SIDE 2ND LINE 
        self.labelLS2ndX1 = customtkinter.CTkLabel(self.tabview.tab("Left\nEnd"), text="Left End X1:")
        self.labelLS2ndX1.grid(row=0, column=0, padx=5, pady=5)
        self.labelLS2ndY1 = customtkinter.CTkLabel(self.tabview.tab("Left\nEnd"), text="Left End Y1:")
        self.labelLS2ndY1.grid(row=0, column=1, padx=5, pady=5)
        self.inputLEX1 = customtkinter.CTkEntry(self.tabview.tab("Left\nEnd"),placeholder_text = "Enter Left End X1", width=90, font=('calibre',10,'normal'))
        self.inputLEX1.grid(row=1, column=0, padx=5, pady=(0, 0))
        self.inputLEY1 = customtkinter.CTkEntry(self.tabview.tab("Left\nEnd"),placeholder_text = "Enter Left End Y1", width=90, font=('calibre',10,'normal'))
        self.inputLEY1.grid(row=1, column=1, padx=5, pady=(0, 0))
        self.labelLS2ndX2 = customtkinter.CTkLabel(self.tabview.tab("Left\nEnd"), text="Left End X2:")
        self.labelLS2ndX2.grid(row=2, column=0, padx=5, pady=5)
        self.labelLS2ndY2 = customtkinter.CTkLabel(self.tabview.tab("Left\nEnd"), text="Left End Y2:")
        self.labelLS2ndY2.grid(row=2, column=1, padx=5, pady=5)
        self.inputLEX2 = customtkinter.CTkEntry(self.tabview.tab("Left\nEnd"),placeholder_text = "Enter Left End X2", width=90, font=('calibre',10,'normal'))
        self.inputLEX2.grid(row=3, column=0, padx=5, pady=(0, 0))
        self.inputLEY2 = customtkinter.CTkEntry(self.tabview.tab("Left\nEnd"),placeholder_text = "Enter Left End Y2", width=90,font=('calibre',10,'normal'))
        self.inputLEY2.grid(row=3, column=1, padx=5, pady=(0, 0))
     


        self.tabview.tab("Right\nStart").grid_columnconfigure((0,1), weight=1)  # configure INPUTS OF RIGHT SIDE 1ST LINE 
        self.labelRS2ndX1 = customtkinter.CTkLabel(self.tabview.tab("Right\nStart"), text="Right Start X1:",font=('calibre',12,'normal'))
        self.labelRS2ndX1.grid(row=0, column=0, padx=5, pady=5)
        self.labelRS2ndY1 = customtkinter.CTkLabel(self.tabview.tab("Right\nStart"), text="Right Start Y1:")
        self.labelRS2ndY1.grid(row=0, column=1, padx=5, pady=5)
        self.inputRSX1 = customtkinter.CTkEntry(self.tabview.tab("Right\nStart"),placeholder_text = "Enter Right Start X1", width=90, font=('calibre',10,'normal'))
        self.inputRSX1.grid(row=1, column=0, padx=5, pady=(0, 0))
        self.inputRSY1 = customtkinter.CTkEntry(self.tabview.tab("Right\nStart"),placeholder_text = "Enter Right Start Y1", width=90, font=('calibre',10,'normal'))
        self.inputRSY1.grid(row=1, column=1, padx=5, pady=(0, 0))
        self.labelRS2ndX2 = customtkinter.CTkLabel(self.tabview.tab("Right\nStart"), text="Right Start X2:")
        self.labelRS2ndX2.grid(row=2, column=0, padx=5, pady=5)
        self.labelRS2ndY2 = customtkinter.CTkLabel(self.tabview.tab("Right\nStart"), text="Right Start Y2:")
        self.labelRS2ndY2.grid(row=2, column=1, padx=5, pady=5)
        self.inputRSX2 = customtkinter.CTkEntry(self.tabview.tab("Right\nStart"),placeholder_text = "Enter Right Start X2", width=90, font=('calibre',10,'normal'))
        self.inputRSX2.grid(row=3, column=0, padx=5, pady=(0, 0))
        self.inputRSY2 = customtkinter.CTkEntry(self.tabview.tab("Right\nStart"),placeholder_text = "Enter Right Start X2", width=90, font=('calibre',10,'normal'))
        self.inputRSY2.grid(row=3, column=1, padx=5, pady=(0, 0))
    
       

        self.tabview.tab("Right\nEnd").grid_columnconfigure((0,1), weight=1)  # configure INPUTS OF RIGHT SIDE 2ND LINE 
        self.labelRS2ndX1 = customtkinter.CTkLabel(self.tabview.tab("Right\nEnd"), text="Right End X1:")
        self.labelRS2ndX1.grid(row=0, column=0, padx=5, pady=5)
        self.labelRS2ndY1 = customtkinter.CTkLabel(self.tabview.tab("Right\nEnd"), text="Right End Y1:")
        self.labelRS2ndY1.grid(row=0, column=1, padx=5, pady=5)
        self.inputREX1 = customtkinter.CTkEntry(self.tabview.tab("Right\nEnd"),placeholder_text = "Enter Right End X1", width=90, font=('calibre',10,'normal'))
        self.inputREX1.grid(row=1, column=0, padx=5, pady=(0, 0))
        self.inputREY1 = customtkinter.CTkEntry(self.tabview.tab("Right\nEnd"),placeholder_text = "Enter Right End Y1", width=90, font=('calibre',10,'normal'))
        self.inputREY1.grid(row=1, column=1, padx=5, pady=(0, 0))
        self.labelRS2ndX2 = customtkinter.CTkLabel(self.tabview.tab("Right\nEnd"), text="Right End X2:")
        self.labelRS2ndX2.grid(row=2, column=0, padx=5, pady=5)
        self.labelRS2ndY2 = customtkinter.CTkLabel(self.tabview.tab("Right\nEnd"), text="Right End Y2:")
        self.labelRS2ndY2.grid(row=2, column=1, padx=5, pady=5)
        self.inputREX2 = customtkinter.CTkEntry(self.tabview.tab("Right\nEnd"),placeholder_text = "Enter Right End X2", width=90,font=('calibre',10,'normal'))
        self.inputREX2.grid(row=3, column=0, padx=5, pady=(0, 0))
        self.inputREY2 = customtkinter.CTkEntry(self.tabview.tab("Right\nEnd"),placeholder_text = "Enter Right End Y2", width=90, font=('calibre',10,'normal'))
        self.inputREY2.grid(row=3, column=1, padx=5, pady=(0, 0))
     
  
       
        self.rightside_button_2 = customtkinter.CTkButton(self.sidebar_frame,height=30,fg_color="#16375c",text="Submit", command=self.changeValues) #left side 2nd button 
        self.rightside_button_2.grid(row=1, column=0,columnspan=2, padx=20, pady=(10,10))


        # side constant text 
       
        self.side_mid_frame = customtkinter.CTkFrame(self.sidebar_frame,height=200,fg_color=("#aec6cf","#416382"), width=140, corner_radius=5)
        self.side_mid_frame.grid(row=2, column=0, padx=10, pady=(0,10))

        self.labelfxl = customtkinter.CTkLabel(self.side_mid_frame, text="Frame X ")
        self.labelfxl.grid(row=0, column=0,columnspan=3,padx=10, pady=0)
        self.inputframex1 = customtkinter.CTkEntry(self.side_mid_frame,placeholder_text = "Frame X1", width=60, font=('calibre',10,'normal'))
        self.inputframex1.grid(row=1, column=0, padx=(20,3), pady=(0, 0))
        self.label1 = customtkinter.CTkLabel(self.side_mid_frame, text=" : ")
        self.label1.grid(row=1, column=1,padx=0, pady=0)
        self.inputframex2 = customtkinter.CTkEntry(self.side_mid_frame,placeholder_text = "Frame X2", width=60, font=('calibre',10,'normal'))
        self.inputframex2.grid(row=1, column=2,padx=(3,20), pady=(0, 0))
        self.labelfyl = customtkinter.CTkLabel(self.side_mid_frame, text="Frame Y")
        self.labelfyl.grid(row=2, column=0, columnspan=3,padx=10, pady=(5,0))
        self.inputframey1 = customtkinter.CTkEntry(self.side_mid_frame,placeholder_text = "Frame Y1", width=60, font=('calibre',10,'normal'))
        self.inputframey1.grid(row=3, column=0, padx=(20,3), pady=(0, 0))
        self.label2 = customtkinter.CTkLabel(self.side_mid_frame, text=" : ")
        self.label2.grid(row=3, column=1,padx=0, pady=0)
        self.inputframey2 = customtkinter.CTkEntry(self.side_mid_frame,placeholder_text = "Frame Y2", width=60, font=('calibre',10,'normal'))
        self.inputframey2.grid(row=3, column=2,padx=(3,20), pady=(0, 0))
        self.fps=0
        self.labelfps = customtkinter.CTkLabel(self.side_mid_frame, text="Frame Per Second: "+str(self.fps))
        self.labelfps.grid(row=4, column=0, columnspan=3,padx=30, pady=(5,5))
        
        """
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=150)
        self.textbox.grid(row=1, column=0, columnspan=2, padx=(30, 30), pady=(20, 0), sticky="nsew")
        self.textbox.insert("20.0", "Frame X Left: " + "400\n\n")
        self.textbox.insert("20.0", "Frame X Right: " + "400\n\n")
        self.textbox.insert("20.0", "Frame Y Left: " + "400\n\n")
        self.textbox.insert("20.0", "Frame Y Right: " + "400\n\n")
        """

         # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self.sidebar_frame,height=100,width=200)
        self.checkbox_slider_frame.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(2, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,fg_color="#003158",text="Capture All", command=self.captureallcheck)
        self.checkbox_1.grid(row=0, column=0, pady=(10, 0), padx=(0,0))
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, fg_color="#003158",text="Capture Exceed", command=self.captureexceedcheck)
        self.checkbox_2.grid(row=1, column=0, pady=10, padx=(17,0))
        self.checkbox_2.select()
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,fg_color="#003158",text="Record Video", command=self.recordvideocheck)
        self.checkbox_3.grid(row=2, column=0, pady=(0, 15), padx=(5,0))


        # bottom options
        self.side_botom_frame = customtkinter.CTkFrame(self.sidebar_frame,height=200,fg_color=("#e5e5e5","#212121"), width=180)
        self.side_botom_frame.grid(row=12, column=0,columnspan=2, padx=10, pady=5)
        self.appearance_mode_label = customtkinter.CTkLabel(self.side_botom_frame, text="Appearance Mode:", anchor="w") 
        self.appearance_mode_label.grid(row=0, column=0, padx=20, pady=(5, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.side_botom_frame, fg_color="#29577e",button_color="#003158",values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=20, pady=(0, 5))
        self.scaling_label = customtkinter.CTkLabel(self.side_botom_frame, text="Display Scalling:", anchor="w")
        self.scaling_label.grid(row=2, column=0, padx=20, pady=(0, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.side_botom_frame, fg_color="#29577e",button_color="#003158",values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=3, column=0, padx=20, pady=(0, 15))

      #default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")

        #set value

        self.inputppm.insert(1,str(ppm[0]))
        self.inputspeed.insert(1,str(limit[0]))

        self.inputLSX1.insert(1,str(start_region_x[0]))
        self.inputLSY1.insert(1,str(start_region_y[0]))

        self.inputLSX2.insert(1,str(start_region_x[1]))
        self.inputLSY2.insert(1,str(start_region_y[1]))

        self.inputRSX1.insert(1,str(start_region_x[2]))
        self.inputRSY1.insert(1,str(start_region_y[2]))

        self.inputRSX2.insert(1,str(start_region_x[3]))
        self.inputRSY2.insert(1,str(start_region_y[3]))

        self.inputLEX1.insert(1,str(end_region_x[0]))
        self.inputLEY1.insert(1,str(end_region_y[0]))

        self.inputLEX2.insert(1,str(end_region_x[1]))
        self.inputLEY2.insert(1,str(end_region_y[1]))

        self.inputREX1.insert(1,str(end_region_x[2]))
        self.inputREY1.insert(1,str(end_region_y[2]))

        self.inputREX2.insert(1,str(end_region_x[3]))
        self.inputREY2.insert(1,str(end_region_y[3]))

        self.inputframex1.insert(1,str(fx[0]))
        self.inputframex2.insert(1,str(fx[1]))

        self.inputframey1.insert(1,str(fy[0]))
        self.inputframey2.insert(1,str(fy[1]))


      #middle frame
        self.Mid_frame = customtkinter.CTkFrame(self, fg_color=("#e5e5e5","#212121"), corner_radius=5)
        self.Mid_frame.grid(row=0, column=1, columnspan=4, rowspan=9,padx=(10, 0), pady=(5, 5), sticky="nsew")
        self.label = customtkinter.CTkLabel(self, bg_color=("#e5e5e5","#212121"), text="")
        self.label.grid(row=0, column=1, columnspan=4, rowspan=9,sticky="nsew")
        

       #right side frame
        self.Right_frame = customtkinter.CTkFrame(self, width=200,fg_color=("#e5e5e5","#212121"), corner_radius=5)
        self.Right_frame.grid(row=0, column=5, rowspan=9,padx=(10, 10), pady=(0, 0), sticky="nsew")
        #self.labelRight = customtkinter.CTkLabel(self.Right_frame,  corner_radius=5,width=200,text="Frame X Left:400\n Frame X Right:400\nFrame Y Left: 400\nFrame Y Right:400\n")
        self.text = customtkinter.CTkTextbox(self, height=12, width=30, fg_color=("#eaeaea","#272727"))
        self.text.configure(state=tkinter.DISABLED)
        self.text.grid(row=0, column=5, rowspan=9,sticky='nsew', padx=(5, 5))
        
        # Create a VideoCapture object to read the video file
        self.cap = cv2.VideoCapture(video_dir)
        
        self.vfps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.model = YOLO("./TrainedModel/bestn.pt")
        self.classNames = ["Bike", "Auto", "Car", "Truck", "Bus", "Other Vehicle"]
        self.tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
        #Creater Tracker Object
        self.speedtracker = SpeedTracker()
        self.dim = (900, 900)
        self.fps=self.vfps
        self.labelfps.configure(text="Frame Per Second: "+str(self.fps))
        frame_width = int(1200)
        frame_height = int(720)
        self.out = cv2.VideoWriter('./TrafficRecord/video/output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
        self.update()
    def changeValues(self):

        ppm[0]= int(self.inputppm.get())
        
        limit[0]=int(self.inputspeed.get())

        start_region_x[0]= int(self.inputLSX1.get())
        start_region_x[1]=int(self.inputLSX2.get())
        start_region_x[2]=int(self.inputRSX1.get())
        start_region_x[3]=int(self.inputRSX2.get())

        start_region_y[0]=int(self.inputLSY1.get())
        start_region_y[1]=int(self.inputLSY2.get())
        start_region_y[2]=int(self.inputRSY1.get())
        start_region_y[3]=int(self.inputRSY2.get())
        
        end_region_x[0]=int(self.inputLEX1.get())
        end_region_x[1]=int(self.inputLEX2.get())
        end_region_x[2]=int(self.inputREX1.get())
        end_region_x[3]=int(self.inputREX2.get())

        end_region_y[0]=int(self.inputLEY1.get())
        end_region_y[1]=int(self.inputLEY2.get())
        end_region_y[2]=int(self.inputREY1.get())
        end_region_y[3]=int(self.inputREY2.get())

        fx[0]=int(self.inputframex1.get())
        fx[1]=int(self.inputframex2.get())

        fy[0]=int(self.inputframey1.get())
        fy[1]=int(self.inputframey2.get())
        self.speedtracker.changeconfig()

  

    def update(self):
        ret, image = self.cap.read()
        if ret:
            start_time = time.time()
            image = cv2.resize(image, self.dim, fx=0.5, fy=0.5)
            H, W, _ = image.shape
            image = image[fy[0]:fy[1],fx[0]:fx[1]]
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
            #time.sleep(0.2)
            end_time = time.time()
            #print(frame_processing_time*1000)
            calcfps=1/self.vfps
            frame_processing_time = (end_time - start_time)-calcfps
            
            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                #print(result)
                w, h = x2 - x1, y2 - y1
                objects_rect.append([x1,y1,w,h,id])
                self.speedtracker.update(objects_rect,frame_processing_time)
                objects_rect.clear()

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
                
                
                
                
                if speed!=0:
                    if(self.captureExceed):
                        self.speedtracker.exceededCapture(image, x1, y1, h, w, speed, id)
                    if(self.captureAll):
                        self.speedtracker.capture(image, x1, y1, h, w, speed, id)
                    self.speedtracker.dataTrack(speed, id) 
                    
                    


            # DRAW LINES


            cv2.line(image, (start_region_x[0], start_region_y[0]), (start_region_x[1], start_region_y[1]), (122, 255, 105), 2)#left start

            cv2.line(image, (end_region_x[0], end_region_y[0]), (end_region_x[1], end_region_y[1]), (81, 75, 201), 2)#left end



            cv2.line(image, (start_region_x[2], start_region_y[2]), (start_region_x[3], start_region_y[3]), (122, 255, 105), 2)#right start

            
            cv2.line(image, (end_region_x[2], end_region_y[2]), (end_region_x[3], end_region_y[3]), (81, 75, 201), 2)#right end
            
            
            #DISPLAY
            #cv2.imshow('Frame',image)
            #cv2.waitKey(1)
            # ret, frame = self.cap.read()
            if (self.recordVideo):
                # open_cv_image = np.array(pil_img)
                cv_img = cv2.resize(image, (1200, 720))
                self.out.write(cv_img)
                self.recordFlag=True
            if(self.recordFlag and not self.recordVideo):
                self.recordFlag=False
                self.out.release()
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img)
          
            
            # Convert the PIL image to a Tkinter-compatible image
            # tk_img = ImageTk.PhotoImage(pil_img)
            # Convert the PhotoImage to CTkImage
            # print(self.winfo_width())
            if(self.winfo_width()>450):
                ctk_image = customtkinter.CTkImage(pil_img, size=((self.winfo_width()-450),(self.winfo_height()-10)))
            else:
                ctk_image = customtkinter.CTkImage(pil_img, size=((self.winfo_width()-100),(self.winfo_height()-10)))
            
            
            
            # Set the image on the label widget
            self.label.configure(image=ctk_image)
            
            update_text(self)
            self.after(1000 // self.vfps, self.update)
        else:
            self.cap = cv2.VideoCapture(video_dir)
            self.update()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    def captureallcheck(self):
        if(self.checkbox_1.get()==1):
            self.captureAll=True
        else:
            self.captureAll=False
    def captureexceedcheck(self):
        if(self.checkbox_2.get()==1):
            self.captureExceed=True
        else:
            self.captureExceed=False
    def recordvideocheck(self):
        if(self.checkbox_3.get()==1):
            self.recordVideo=True
        else:
            self.recordVideo=False
            
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
        self.text.configure(state=tkinter.NORMAL)
        self.text.insert(tkinter.END, new_data)
        self.text.configure(state=tkinter.DISABLED)
        
    # Update previous contents
    prev_contents = data




if __name__ == "__main__":
    app = CustomFrame()
    app.iconbitmap("logo.ico")
    app.mainloop()
