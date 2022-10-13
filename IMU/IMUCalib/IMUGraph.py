import smbus2
import time
import matplotlib.pyplot as plt
import numpy as np

#List initialisation
gx_array=[]
gy_array=[]
gz_array = []
ax_array=[]
az_array=[]
ay_array=[]
time_taken = 0

 
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
 
def MPU_Init():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data (Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)
 
def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)
    value = ((high << 8)| low)
    if (value > 32768):
        value = value - 65536
    return value
 
bus = smbus2.SMBus(1)
Device_Address = 0x68
 
MPU_Init()
print("Reading Data of Gyroscope and Accelerometer")
time1 = time.time()
while True:

    try:
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)
    
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)
    
        Ax = (acc_x/16384.0)
        Ay = (acc_y/16384.0)
        Az = (acc_z/16384.0)+0.08
    
        Gx = (gyro_x/131.0)+0.13
        Gy = (gyro_y/131.0)-0.18
        Gz = (gyro_z/131.0)+0.34
        

        gx_array.append(Gx)
        gy_array.append(Gy)
        gz_array.append(Gz)
        ax_array.append(Ax)
        az_array.append(Ay)
        ay_array.append(Az)
        time2 = time.time()
        print("Gx = %.2f" %Gx, "Gy = %.2f" %Gy, "Gz = %.2f" %Gz, "Ax = %.2f g" %Ax, "Ay = %.2f g" %Ay, "Az = %.5f g" %Az)
        time.sleep(1)

    except KeyboardInterrupt:
        time_taken = time2-time1
        print("Final IMU values: "+"Gx = %.2f" %Gx, "Gy = %.2f" %Gy, "Gz = %.2f" %Gz, "Ax = %.2f g" %Ax, "Ay = %.2f g" %Ay, "Az = %.5f g" %Az)
        time_scale = np.linspace(0, 20, 20//time_taken)
        plt.plot(time_scale,gx_array)
        plt.plot(time_scale,gy_array)
        plt.plot(time_scale,gz_array)
        plt.title("Gyroscope orientation")
        plt.ylabel("Gyroscope values")
        plt.xlabel("Time")
        plt.gca().legend(('Gx','Gy','Gz'))
        plt.grid()
  

