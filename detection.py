import cv2
import numpy as np
import csv
import time
import imutils
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs


#f_width = 640
#f_height = 480
write_count=0
detection_log=[]
anypercent_log=[]
time_log=[]
color=[]

def empty(a):
    pass

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#capture.set(3, f_width)
#capture.set(4, f_height)

print("Starting...")
startTime = time.time()
while True:
    
    _, img = capture.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #lower = np.array([hmin, smin, vmin])
    #upper = np.array([hmax, smax, vmax])

    #BEST VALUES
    #lower = np.array([6, 50, 0])
    #upper = np.array([23, 255, 255])

    lower = np.array([5, 0, 0])
    upper = np.array([50, 255, 255])

    mask = cv2.inRange(imgHSV, lower, upper)
    result = cv2.bitwise_and(img, img, mask = mask)

    #print (cv2.contourArea(contour))


    #cv2.imshow("original", img)
    #cv2.imshow("hsv", imgHSV)
    cv2.imshow("masked", mask)
    #cv2.imshow("result", result)

    white = np.sum(mask == 255)
    black = np.sum(mask == 0)
    
    
    percent = ((black/white)*100)
    print("white px: ", white)
    print("black px: ", black)
    print("percent", percent)
    #print("black/white percentage: " + str(percent)+"%")
    anypercent_log.append(percent)
    time_log.append(time.time()-startTime)
    #logs time here
    if (percent>1):
        write_count+=1
        detection_log.append((time.time()-startTime))
        

    key = cv2.waitKey(1)
    if key==ord('q') or key==ord('Q'):
        break


endTime = time.time()
end_start = time.time() - startTime
print("Start time: ", startTime)
print("End Time: ", endTime)
print("Elapsed", end_start)
print("rows printed: ", write_count)

"""
with open('logdata.csv', 'w', encoding='UTF8') as f:
    print("wrote to csv")
    writer = csv.writer(f)
    writer.writerow(csv)
"""
threshold = 50
for i in anypercent_log:
    if i>threshold:
        color.append("red")
    else:
        color.append("blue")

for i in range(len(time_log)):
    time_log[i] = time_log[i]*6.7


for i in range(len(anypercent_log)):
    plt.scatter(time_log[i], anypercent_log[i], c = color[i], s = 10,linewidth = 0)



dronespeed=6.7
clusteravg=0
clustercount=0
initialdistance=0
for i in range(len(anypercent_log)-1):
    #IF CLUSTER IDENTIFIED CALCULATE HOW MANY METERS AWAY FROM DOCKING STATION
    if (color[i] == color[i+1]) and (color[i]=="red"):
        if (clustercount==0):
            initialdistance = round(time_log[i])
        clusteravg = clusteravg+anypercent_log[i]
        clustercount+=1
    else:
        clustercount+=1
        clusteravg = clusteravg/clustercount
        if clustercount>7:
            print("CLUSTER DETECTED FROM", initialdistance, "meters to", round(time_log[i]), "meters from docking station at a confidence of: ", round(clusteravg), " percent")
        clustercount=0
        clusteravg=0
        initialdistance=0


plt.axhline(threshold, color='red', ls='dotted')
plt.xlabel('meters')
plt.ylabel('percent')
plt.title("meters vs black px %")
plt.show()
      
