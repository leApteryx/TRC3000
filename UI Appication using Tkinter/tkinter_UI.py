import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

# functions
def load_cell():
    print("load_cell calibrated!")

def servo():
    print("servo calibrated!")

def imu():
    print("imu calibrated!")

def camera():
    print("camera calibrated!")

def lights():
    print("lights turned on!")

# define root window
root = tk.Tk()

# getting device screen size
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# format root window
root.title('Anaerobic Digestate Tester')
root.geometry(f"{str(width)}x{str(height)}")
root.resizable(False, False)

# create label frame
lf = ttk.LabelFrame(root, text='Calibration Options')
lf.grid(column=0, row=0, padx=20, pady=20, ipadx=20, ipady=20)

# add calibration buttons
button_dict = {"load cell": load_cell,
               "set servo position": servo,
               "check IMU readings": imu,
               "record image": camera,
               "turn on lights": lights}

for name, function in button_dict.items():
    tk.Button(lf, width=20, text=name, padx=5, pady=5, command=function).pack()


# def fahrenheit_to_celsius(f):
#     """ Convert fahrenheit to celsius
#     """
#     return (f - 32) * 5/9
#
#
# # frame
# frame = ttk.Frame(root)
#
#
# # field options
# options = {'padx': 5, 'pady': 5}
#
# # temperature label
# temperature_label = ttk.Label(frame, text='Fahrenheit')
# temperature_label.grid(column=0, row=0, sticky='W', **options)
#
# # temperature entry
# temperature = tk.StringVar()
# temperature_entry = ttk.Entry(frame, textvariable=temperature)
# temperature_entry.grid(column=1, row=0, **options)
# temperature_entry.focus()
#
# # convert button
#
#
# def convert_button_clicked():
#     """  Handle convert button click event
#     """
#     try:
#         f = float(temperature.get())
#         c = fahrenheit_to_celsius(f)
#         result = f'{f} Fahrenheit = {c:.2f} Celsius'
#         result_label.config(text=result)
#     except ValueError as error:
#         showerror(title='Error', message=error)
#
#
# convert_button = ttk.Button(frame, text='Convert')
# convert_button.grid(column=2, row=0, sticky='W', **options)
# convert_button.configure(command=convert_button_clicked)
#
# # result label
# result_label = ttk.Label(frame)
# result_label.grid(row=1, columnspan=3, **options)
#
# # add padding to the frame and show it
# frame.grid(padx=10, pady=10)


# start the app
root.mainloop()