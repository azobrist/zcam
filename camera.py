import numpy as np
import argparse

max_picam_resolution = (3240,2464)
resolutions = { "max": max_picam_resolution, 
                "high": np.multiply(max_picam_resolution,0.75), 
                "medium": np.multiply(max_picam_resolution,0.50), 
                "low": np.multiply(max_picam_resolution,0.25)}

def calc_resolution_factor(resolutionY):
    return resolutionY*3.04/2.76

#this is the pipeline used to communicate with the V2 picam module using jetson
def gstreamer_pipeline(
    capture_width=3240,
    capture_height=2464,
    display_width=3240,
    display_height=2464,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def cmdline_args():
    # Make parser object
    p = argparse.ArgumentParser(description=
        """
        Simple camera module.
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    p.add_argument("--use-integrated","-i", action="store_true", default=False,
                    help= "Use laptop camera")
    p.add_argument("--use-picamera","-p", action="store_true", default=False,
                    help= "Use laptop camera")
    p.add_argument("--snap-shot","-t", action="store_true", default=False,
                    help="Take a snap shot and save it to file")
    p.add_argument("--resolution","-r", type=str, default="low", 
                    help="Resolution can be max, high, medium, or low.")
    p.add_argument("--length", "-l", type=int, default=10, 
                    help="Record video length in seconds")
    p.add_argument("--show","-s", action="store_true", default=False,
                help="Show video or image taken in window")

    return(p.parse_args())

if __name__ == "__main__":
    args = cmdline_args()

    if args.use_picamera:
        import picamera
        import time
        cam = picamera.PiCamera()
        #cam.resolution = resolutions[args.resolution]
        out = open('picam.h264', 'wb')
        cam.start_recording(out)
        time.sleep(args.length)
        cam.stop_recording()
        out.close()
        exit()

    import cv2

    res = resolutions[args.resolution]
    if args.use_integrated == False:
        cam = cv2.VideoCapture(gstreamer_pipeline(flip_method=2,display_width=res[0],display_height=res[1]), cv2.CAP_GSTREAMER)
    else:
        cam = cv2.VideoCapture(1) 
        if cam is None or not cam.isOpened():
            cam = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))

    if args.show:
        cv2.namedWindow('Camera Module', cv2.WINDOW_AUTOSIZE)

    capture = True
    while(capture):
        # Capture frame-by-frame
        ret, frame = cam.read()

        # Our operations on the frame come here

        # Display the resulting frame
        if args.show:
            cv2.imshow('frame',frame)

        # Save frame
        out.write(frame)

        # Exit loop?
        if cv2.waitKey(1) & 0xFF == ord('q'):
            capture = False

        if args.snap_shot:
            capture = False

    # When everything done, release the capture
    cam.release()
    out.release()
    cv2.destroyAllWindows()