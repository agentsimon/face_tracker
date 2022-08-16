# Convert video input to a list of 1 and 0 for sending via OSC
import cv2
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import argparse  
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IPAddr = s.getsockname()[0]
print(IPAddr)
# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
      
    # Capture the video frame
    # by frame
    
    ret, frame = vid.read()
    frame =cv2.resize(frame,(8, 8), interpolation = cv2.INTER_LINEAR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _,thres_image = cv2.threshold(gray, 120,255,0)
    # Display the resulting frame
    #print(thres_image)
    cv2.imshow('frame', thres_image)

    res =thres_image
    for line in enumerate(thres_image):
        for index2 in enumerate(thres_image[line[0]]):
            if thres_image[line[0]][index2[0]] > 0:
                res[line[0]][index2[0]] = 1

    print(res) 
    #print(type(res))  
    list1 = res.tolist()
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=IPAddr,
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8888,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    client.send_message("/ledlist",list1)










                
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
