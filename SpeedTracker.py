import cv2
import math
import time
import numpy as np
import os

limit =[20]  # km/hr
#real time distance of 120 px = 5 meter
#real time distance of 1 meter=24px
ppm =[24]

fx=[0,900]
fy=[200,900]

start_region_x=[0,450,450,900] #left start x1, left start x2, right start x1, right start x2
start_region_y=[400,400,250,250] #left start y1, left start y2, right start y1, right start y2

end_region_x=[0,450,450,900]  #left end x1, left end x2, right end x1, right end x2
end_region_y=[250,250,400,400] #left end y1, left end y2, right end y1, right end y2


traffic_record_folder_name = "TrafficRecord"
config_record_folder_name = "ConfigRecord"
if not os.path.exists(config_record_folder_name):
    os.makedirs(config_record_folder_name)
    config_record_file_location = config_record_folder_name + "//Config.txt"
    file = open(config_record_file_location, "w")
    file.write(str(limit[0])+"\n"+str(ppm[0])+"\n"+
    str(start_region_x[0])+"\n"+str(start_region_x[1])+"\n"+str(start_region_x[2])+"\n"+str(start_region_x[3])+"\n"
    +str(start_region_y[0])+"\n"+str(start_region_y[1])+"\n"+str(start_region_y[2])+"\n"+str(start_region_y[3])+"\n"
    +str(end_region_x[0])+"\n"+str(end_region_x[1])+"\n"+str(end_region_x[2])+"\n"+str(end_region_x[3])+"\n"
    +str(end_region_y[0])+"\n"+str(end_region_y[1])+"\n"+str(end_region_y[2])+"\n"+str(end_region_y[3])+"\n"
    +str(fx[0])+"\n"+str(fx[1])+"\n"+str(fy[0])+"\n"+str(fy[1])+"\n")
    file.close()

if not os.path.exists(traffic_record_folder_name):
    os.makedirs(traffic_record_folder_name)
    os.makedirs(traffic_record_folder_name+"//exceeded")
    os.makedirs(traffic_record_folder_name+"//all")
    os.makedirs(traffic_record_folder_name+"//video")

speed_record_file_location = traffic_record_folder_name + "//SpeedRecord.txt"
file = open(speed_record_file_location, "w")
file.write("ID \t SPEED\n------\t-------\n")
file.close()

with open("./ConfigRecord/Config.txt", "r") as file:
            data = file.read()
            arrdata=data.split()
            limit[0]=int(arrdata[0])
            ppm[0]=int(arrdata[1])
            start_region_x[0]=int(arrdata[2])
            start_region_x[1]=int(arrdata[3])
            start_region_x[2]=int(arrdata[4])
            start_region_x[3]=int(arrdata[5])

            start_region_y[0]=int(arrdata[6])
            start_region_y[1]=int(arrdata[7])
            start_region_y[2]=int(arrdata[8])
            start_region_y[3]=int(arrdata[9])
            
            end_region_x[0]=int(arrdata[10])
            end_region_x[1]=int(arrdata[11])
            end_region_x[2]=int(arrdata[12])
            end_region_x[3]=int(arrdata[13])
            
            end_region_y[0]=int(arrdata[14])
            end_region_y[1]=int(arrdata[15])
            end_region_y[2]=int(arrdata[16])
            end_region_y[3]=int(arrdata[17])

            fx[0]=int(arrdata[18])
            fx[1]=int(arrdata[19])

            fy[0]=int(arrdata[20])
            fy[1]=int(arrdata[21])
            

class SpeedTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        
        self.id_count = 0
        # self.start = 0
        # self.stop = 0
        self.et = 0
        self.y1 = np.zeros((1, 10000))
        self.y2 = np.zeros((1, 10000))
        self.s1 = np.zeros((1, 10000))
        self.s2 = np.zeros((1, 10000))
        self.vpt = np.zeros((1, 10000))
        self.s = np.zeros((1, 10000))
        self.f = np.zeros(10000)
        self.capf = np.zeros(10000)
        self.capd = np.zeros(10000)
        self.count = 0
        self.exceeded = 0

    def update(self, objects_rect, frame_processing_time):
        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h, id = rect
            x, y, w, h, id = int(x), int(y), int(w), int(h), int(id)
            #print("id: "+str(id))
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            # START TIMER
            if ((cy >= start_region_y[0] and cy <= start_region_y[0]+30 and
                cy >= start_region_y[1] and cy <= start_region_y[1]+30 and
                cx >=start_region_x[0] and cx<=start_region_x[1]) or
                (cy >= start_region_y[2] and cy <= start_region_y[2]+30 and
                cy >= start_region_y[3] and cy <= start_region_y[3]+30 and
                cx >=start_region_x[2] and cx<=start_region_x[3])):
                #if (self.s1[0, id] == 0):

                # if( id>100 ):
                #     self.s1[0, id%100] = time.time()
                # else:
                
                if self.s1[0, id]<=0:
                    self.y1[0, int(id)] = cy
                    self.s1[0, int(id)] = time.time()
                    
                #if (self.s1[0, id] != 0):
                #self.s2[0, id] = time.time()
                #self.s[0, id] = self.s2[0, id] - self.s1[0, id]
                # if (y >= 380 and y <= 410 and x >=450 and x<=960):
                #     self.s1[0, id] = time.time()

            # STOP TIMER and FIND DIFFERENCE
            if ((cy >= end_region_y[0] and cy <= end_region_y[0]+30 and
                cy >= end_region_y[1] and cy <= end_region_y[1]+30 and
                cx>=end_region_x[0] and cx<=end_region_x[1]) or
                (cy >= end_region_y[2] and cy <= end_region_y[2]+30 and
                cy >= end_region_y[3] and cy <= end_region_y[3]+30 and
                cx>=end_region_x[2] and cx<=end_region_x[3])):
                #if (self.s1[0, id] == 0):
                    #self.s1[0, id] = time.time()
                #if (self.s1[0, id] != 0):
                    #self.s2[0, id] = time.time()
                    #self.s[0, id] = self.s2[0, id] - self.s1[0, id]
                
                if self.s2[0, id]<=0:
                    self.y2[0, int(id)] = cy
                    self.s2[0, id] = time.time()
                    

                self.s[0, id] = self.s2[0, id] - self.s1[0, id]-self.vpt[0, id]
                # if int(id)==7:
                #         print("id: "+str(id)+" total: "+str(self.s[0, id])+
                #         " vpt: "+str(self.vpt[0, id]))
                #print("ID: "+ str(id)+" Time Diff : "+ str(self.s[0,id])+" Start Time: " + str(self.s1[0,id])+" End Time: " + str(self.s2[0,id]))
                    # STOP TIMER and FIND DIFFERENCE
                    # if (y >= 250 and y <= 280 and x>=450 and x<=800):
                    #     #if (self.s1[0, id] == 0):
                    #         #self.s1[0, id] = time.time()
                    #     #if (self.s1[0, id] != 0):
                    #         #self.s2[0, id] = time.time()
                    #         #self.s[0, id] = self.s2[0, id] - self.s1[0, id]
                    #     self.s2[0, id] = time.time()

                    #     self.s[0, id] = self.s2[0, id] - self.s1[0, id]
                        #print("ID: "+ str(id)+" Time Diff : "+ str(self.s[0,id])+" Start Time: " + str(self.s1[0,id])+" End Time: " + str(self.s2[0,id]))
                    #if (y >= 410 and y <= 420):
                    #    self.s2[0, id] = time.time()
                    #    self.s[0, id] = self.s2[0, id] - self.s1[0, id]

                    # CAPTURE FLAG
                   
            if ((cy < start_region_y[0]+30 and cy > end_region_y[0]+30 and
                cx >=start_region_x[0] and cx<=start_region_x[1]) or
                (cy > start_region_y[2] and cy < end_region_y[2]+30 and 
                cx >=start_region_x[2] and cx<=start_region_x[3])):
                
               
                if(self.vpt[0, id]>=0):
                    
                    self.vpt[0, id] =self.vpt[0, id]+frame_processing_time
            if (y < 235):
                self.f[id] = 1


    # SPEEED FUNCTION
    def getsp(self, id):
        #print("elapsed time: "+str(elapsed_time_ms)+" id: "+str(id))
        #elapsed_time_ms=float(elapsed_time_ms)/1000
        id=int(id)
        
        if (self.s[0, id] != 0):
            #elap_vehicle_time=self.s[0, id]+elapsed_time_ms
            dis=abs(float(self.y1[0, id])-float(self.y2[0, id]))
            
            dis=dis/ppm[0]
            #time=((self.s[0, id]*1000)-elapsed_time_ms)/1000
            s = dis / (self.s[0, id]) #change the value according to fps
            s=(s*3600)/1000
            #s= FPSCalc / (self.s[0, id]-(0.00846153846*elapsed_time_ms))
            # print("total elap "+str((elap_vehicle_time-(0.00846153846*elapsed_time_ms))))
            # print("elap "+str(self.s[0, id]))
            # print("y1 "+str(self.y1[0, id]))
            # print("y2 "+str(self.y2[0, id]))
            # yelap = abs(self.y2[0, id] - self.y1[0, id])
            # print("yelap "+str(yelap))
            # print("s "+str(s))
        else:
            s = 0

        return int(s)

    # SAVE VEHICLE DATA
    def capture(self, img, x, y, h, w, sp, id):
        x, y, h, w, sp, id=int(x), int(y), int(h), int(w), int(sp), int(id)
        if (self.capf[id] == 0):
            self.capf[id] = 1
            self.f[id] = 0
            crop_img = img[y - 10:y + h + 10, x - 10:x + w + 10]
            n = str(id) + "_speed_" + str(sp)
            file = traffic_record_folder_name + '//all//' + n + '.jpg'
            cv2.imwrite(file, crop_img)
            
    

    # SAVE VEHICLE DATA
    def exceededCapture(self, img, x, y, h, w, sp, id):
        x, y, h, w, sp, id=int(x), int(y), int(h), int(w), int(sp), int(id)
        if (self.capf[id] == 0):
            if (sp > limit[0]):
                self.capf[id] = 1
                self.f[id] = 0
                crop_img = img[y - 10:y + h + 10, x - 10:x + w + 10]
                n = str(id) + "_speed_" + str(sp)
                file = traffic_record_folder_name + '//exceeded//' + n + '.jpg'
                cv2.imwrite(file, crop_img)
            
    # SAVE VEHICLE DATA
    def dataTrack(self, sp, id):
        sp, id= int(sp), int(id)
        if (self.capd[id] == 0):
            self.capd[id] = 1
            self.f[id] = 0
            self.count += 1
            filet = open(speed_record_file_location, "a")
            if (sp > limit[0]):
                filet.write(str(id) + " \t " + str(sp) + "<---exceeded\n")
                self.exceeded += 1
            else:
                filet.write(str(id) + " \t " + str(sp) + "\n")
            filet.close()

    # SPEED_LIMIT
    def limit(self):
        return limit[0]

    # TEXT FILE SUMMARY
    def end(self):
        file = open(speed_record_file_location, "a")
        file.write("\n-------------\n")
        file.write("-------------\n")
        file.write("SUMMARY\n")
        file.write("-------------\n")
        file.write("Total Vehicles :\t" + str(self.count) + "\n")
        file.write("Exceeded speed limit :\t" + str(self.exceeded))
        file.close()

    #Save config
    def changeconfig(self):
        file = open("./ConfigRecord/Config.txt", "w")
        file.write(str(limit[0])+"\n"+str(ppm[0])+"\n"+
        str(start_region_x[0])+"\n"+str(start_region_x[1])+"\n"+str(start_region_x[2])+"\n"+str(start_region_x[3])+"\n"
        +str(start_region_y[0])+"\n"+str(start_region_y[1])+"\n"+str(start_region_y[2])+"\n"+str(start_region_y[3])+"\n"
        +str(end_region_x[0])+"\n"+str(end_region_x[1])+"\n"+str(end_region_x[2])+"\n"+str(end_region_x[3])+"\n"
        +str(end_region_y[0])+"\n"+str(end_region_y[1])+"\n"+str(end_region_y[2])+"\n"+str(end_region_y[3])+"\n"
        +str(fx[0])+"\n"+str(fx[1])+"\n"+str(fy[0])+"\n"+str(fy[1])+"\n")
        file.close()


