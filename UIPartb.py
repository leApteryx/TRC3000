@@ -43,6 +43,7 @@
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT) # GPIO.BOARD = 36 (load cell)
GPIO.setup(20, GPIO.OUT) # GPIO.BOARD = 38 (imu)
GPIO.setup(21, GPIO.OUT) # GPIO.BOARD = 40 (servo)


@@ -56,6 +57,7 @@ def setup(function):
def cleanup():
    # turn off all relays
    GPIO.output(16, GPIO.HIGH) # GPIO.BOARD = 36 (load cell)
    GPIO.output(20, GPIO.HIGH) # GPIO.BOARD = 38 (imu)
    GPIO.output(21, GPIO.HIGH) # BOARD no. = 40 (servo)

    Output.insert(END, "\nGoodbye!")
@@ -169,6 +171,7 @@ def read_raw_data(addr):

def imu():
    setup("IMU")
    GPIO.output(20, GPIO.LOW) # GPIO.BOARD = 38

    MPU_Init()
    acc_x = read_raw_data(ACCEL_XOUT_H)
@@ -190,6 +193,7 @@ def imu():
    Output.insert(END, "\nGyrocope (degrees/s): \nGx = " + str(Gx) + " | Gy = " + str(Gy) + " | Gz = " + str(Gz))
    Output.insert(END, "\nAcceleration (g): \nAx = " + str(Ax) + " | Ay = " + str(Ay) + " | Az = " + str(Az))
    Output.update()
    cleanup()
    # print("Gx = %.2f" %Gx, "Gy = %.2f" %Gy, "Gz = %.2f" %Gz, "Ax = %.2f g" %Ax, "Ay = %.2f g" %Ay, "Az = %.5f g" %Az)


def take_image():
    setup("take image")
    global current_frame
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    name = 'image' + str(current_frame) + '.jpg'
    cv2.imwrite(name, frame)
    im = Image.open(name)
#     img = ImageTk.PhotoImage(im)
#     canvas = Label(output_frame, image=img)
#     canvas.pack()
#     im_cropped = im.resize((400, 400), Image.ANTIALIAS)
#     im_cropped.show()
    im.show()
    current_frame += 1
    cap.release()
    cv2.destroyAllWindows()
    
    
def take_three_images():
    setup("take 3 images from 3 different angles")
    
    global current_frame
    
    # Turn on servo relay
    GPIO.output(21, GPIO.LOW) # GPIO.BOARD = 40
    # Set pin 11 as an output, and set servo1 as pin 11 as PWM
    GPIO.setup(17, GPIO.OUT) # BOARD no. = 11
    servo1 = GPIO.PWM(17, 50) # pin 17, 50Hz pulse
    #start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    
    servo1.ChangeDutyCycle(2)
    take_image()
    servo1.ChangeDutyCycle(7)
    take_image()
    servo1.ChangeDutyCycle(12)
    take_image()
def stream_camera():
    setup("stream camera")
    Output.insert(END, "\nCamera closing in 5s...")
    Output.update()
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
## UI ##
# define root window
root = tk.Tk()
# getting device screen size
width = math.floor(root.winfo_screenwidth())
height = math.floor(root.winfo_screenheight())
# format root window
root.title('Anaerobic Digestate Tester')
root.geometry(f"{str(width)}x{str(height)}")
root.resizable(False, False)
root.option_add("*font", "arial 25")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
# root.grid_columnconfigure(2, weight=8)
# create calibration label frame
calib_frame = ttk.LabelFrame(root, text='Calibration Options')
calib_frame.grid(column=0, row=0, padx=10, pady=20, ipadx=20, ipady=20, sticky="se")
# create operations label frame
ops_frame = ttk.LabelFrame(root, text='Operations')
ops_frame.grid(column=1, row=0, padx=10, pady=20, ipadx=20, ipady=20, sticky="sw")
# add calibration buttons
calib_dict = {"check IMU readings": imu,
              "read load cell": load_cell,
              "reset servo position": servo
              }
ops_dict = {"take image": take_image,
            "take 3 images" : take_three_images,
            "stream camera": stream_camera
            }
# myfont = font.Font(size=30)
for name, function in calib_dict.items():
    tk.Button(calib_frame, width=20, text=name, padx=5, pady=5, command=function).pack()
#     button = tk.Button(calib_frame, width=20, text=name, padx=5, pady=5, command=function).pack()
#     button['font'] = myfont
    
for name, function in ops_dict.items():
    tk.Button(ops_frame, width=20, text=name, padx=5, pady=5, command=function).pack()
    
# create output label frame
output_frame = ttk.LabelFrame(root, text='Output')
output_frame.grid(column=0, row=1, columnspan=2, padx=20, pady=0, ipadx=20, ipady=20, sticky="n")
# set output text box
Output = Text(output_frame, height=10, width=50)
Output.pack()
# set canvas for image
# canvas = Canvas(output_frame, height=50, width=50)
# canvas.pack()
# start the app
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
