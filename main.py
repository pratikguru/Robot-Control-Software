"""
The purpose of this script is for controlling servo accutators with a GUI.

Forward kinematics of an arm can be simulated with this controller software.
The script uses the serial library for communicating over the serial monitor of the host
computer.

@author: Pratik Gurudatt
@date  : 19/04/2019
"""
import copy
import time
import sys
import serial
import json

try:
    from   PyQt5             import QtCore
    from   PyQt5.QtCore    import pyqtSlot
    from   PyQt5           import QtWidgets, QtGui
    from   PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
    from   PyQt5.QtWidgets import *
    from   PyQt5.uic       import loadUi
except Exception as e:
    print ("Requirement Error! The PyQt Libs are not installed.")
    import os
import math

class App(QDialog):
    def __init__(self):
        super(App, self).__init__()
        try:
            loadUi('interface.ui', self)
        except Exception as e:
            print (e)
            print ("Interface.ui could not be found!")
        self.serial = serial.Serial()
        self.connectionStatus = False
        self.servo_speed = 0
        self.frame_speed = 0
        self.frame_count = 0
        self.loop_count  = 0
        self.frames = []

        self.activated_sliders = []
        for x in range(12): self.activated_sliders.append(0)
        self.slider_list = []
        self.slider_list.append(self.horizontalSlider)
        self.slider_list.append(self.horizontalSlider_2)
        self.slider_list.append(self.horizontalSlider_3)
        self.slider_list.append(self.horizontalSlider_4)
        self.slider_list.append(self.horizontalSlider_5)
        self.slider_list.append(self.horizontalSlider_6)
        self.slider_list.append(self.horizontalSlider_7)
        self.slider_list.append(self.horizontalSlider_8)
        self.slider_list.append(self.horizontalSlider_9)
        self.slider_list.append(self.horizontalSlider_10)
        self.slider_list.append(self.horizontalSlider_11)
        self.slider_list.append(self.horizontalSlider_12)


        self.checkbox_list = []
        self.checkbox_list.append(self.checkBox)
        self.checkbox_list.append(self.checkBox_2)
        self.checkbox_list.append(self.checkBox_3)
        self.checkbox_list.append(self.checkBox_4)
        self.checkbox_list.append(self.checkBox_5)
        self.checkbox_list.append(self.checkBox_6)
        self.checkbox_list.append(self.checkBox_7)
        self.checkbox_list.append(self.checkBox_8)
        self.checkbox_list.append(self.checkBox_9)
        self.checkbox_list.append(self.checkBox_10)
        self.checkbox_list.append(self.checkBox_11)
        self.checkbox_list.append(self.checkBox_12)
        self.disable_sliders()
        self.groupBox_3.setEnabled(False)

        self.servo_label_list=[]
        self.servo_label_list.append(self.angle_1)
        self.servo_label_list.append(self.angle_2)
        self.servo_label_list.append(self.angle_3)
        self.servo_label_list.append(self.angle_4)
        self.servo_label_list.append(self.angle_5)
        self.servo_label_list.append(self.angle_6)
        self.servo_label_list.append(self.angle_7)
        self.servo_label_list.append(self.angle_8)
        self.servo_label_list.append(self.angle_9)
        self.servo_label_list.append(self.angle_10)
        self.servo_label_list.append(self.angle_11)
        self.servo_label_list.append(self.angle_12)


    def run(self):
        print ("Main loop running!")
        self.connect_button.clicked.connect(self.connect_board)
        self.checkBox.toggled.connect(lambda:self.enable_sliders(self.checkBox))
        self.checkBox_2.toggled.connect(lambda:self.enable_sliders(self.checkBox_2))
        self.checkBox_3.toggled.connect(lambda:self.enable_sliders(self.checkBox_3))
        self.checkBox_4.toggled.connect(lambda:self.enable_sliders(self.checkBox_4))
        self.checkBox_5.toggled.connect(lambda:self.enable_sliders(self.checkBox_5))
        self.checkBox_6.toggled.connect(lambda:self.enable_sliders(self.checkBox_6))

        self.checkBox_7.toggled.connect(lambda:self.enable_sliders(self.checkBox_7))
        self.checkBox_8.toggled.connect(lambda:self.enable_sliders(self.checkBox_8))
        self.checkBox_9.toggled.connect(lambda:self.enable_sliders(self.checkBox_9))
        self.checkBox_10.toggled.connect(lambda:self.enable_sliders(self.checkBox_10))
        self.checkBox_11.toggled.connect(lambda:self.enable_sliders(self.checkBox_11))
        self.checkBox_12.toggled.connect(lambda:self.enable_sliders(self.checkBox_12))

        self.horizontalSlider.valueChanged.connect(lambda:self.print_slider(self.horizontalSlider))
        self.horizontalSlider.sliderReleased.connect(lambda:self.slider_control(self.horizontalSlider))
        self.horizontalSlider_2.sliderReleased.connect(lambda:self.slider_control(self.horizontalSlider_2))
        self.horizontalSlider_3.sliderReleased.connect(lambda:self.slider_control(self.horizontalSlider_3))
        self.horizontalSlider_4.valueChanged.connect(lambda:self.slider_control(self.horizontalSlider_4))
        self.horizontalSlider_5.valueChanged.connect(lambda:self.slider_control(self.horizontalSlider_5))
        self.horizontalSlider_6.valueChanged.connect(lambda:self.slider_control(self.horizontalSlider_6))
        self.horizontalSlider_7.valueChanged.connect(lambda:self.slider_control(self.horizontalSlider_7))
        self.horizontalSlider_8.valueChanged.connect(lambda:self.slider_control(self.horizontalSlider_8))
        self.horizontalSlider_9.valueChanged.connect(lambda:self.slider_control(self.horizontalSlider_9))
        self.horizontalSlider_10.valueChanged.connect(lambda:self.slider_control(self.horizontalSlider_10))
        self.horizontalSlider_11.valueChanged.connect(lambda:self.slider_control(self.horizontalSlider_11))
        self.horizontalSlider_12.valueChanged.connect(lambda:self.slider_control(self.horizontalSlider_12))


        self.horizontalSlider_14.valueChanged.connect(self.setServoSpeed)
        self.horizontalSlider_13.valueChanged.connect(self.setFrameSpeed)
        self.add_frame_button.clicked.connect(self.add_frame)
        self.play_button.clicked.connect(self.play_positions)
        self.dial.valueChanged.connect(self.setLoops)
        self.clear_frame_button.clicked.connect(self.clear_frames)

    def clear_frames(self):
        self.frames = []
        self.frame_count = 0

    def setLoops(self):
        self.loop_count = self.dial.value()
        self.label_18.setText(str(self.loop_count))

    def setServoSpeed(self):
        self.servo_speed = self.horizontalSlider_14.value()
        self.label_16.setText(str(self.servo_speed*10))

    def setFrameSpeed(self):
        self.frame_speed = self.horizontalSlider_13.value()
        self.label_15.setText(str(self.frame_speed*10))

    def print_slider(self, slider):
        for count, sliderObj in enumerate(self.slider_list):
            if sliderObj == slider:
                self.servo_label_list[count].setText(str(slider.value()))

    def add_frame(self):
        self.frame_count = self.frame_count + 1
        print ("Frame count: " + str(self.frame_count))
        # data["servo_count"] = len(self.activated_sliders)
        # data["frame_count"] = self.frame_count
        # data["frame_speed"] = 300
        # data["servo_iteration_speed"] = 5
        # data["dimension"]   = 2
        # data["loop"]        = 1
        # data["frame"]       = [[45,120,45], [120, 120, 90]]
        current_frame = []
        current_frame.append(self.horizontalSlider.value())
        current_frame.append(self.horizontalSlider_2.value())
        current_frame.append(self.horizontalSlider_3.value())
        self.frames.append(current_frame)



    def play_positions(self):
        print ("Playing positions...")
        response = {}
        count = 1
        for x in self.activated_sliders:
            if x != 0:
                count = 1 + count

        error = False
        if self.frame_count == 0:
            print ("Add frames")
            error = True

        if self.frame_speed == 0:
            print ("Add frame speed gre 250.")
            error = True

        if self.servo_speed == 0:
            print ("Add frame speed gre 250.")
            error = True

        if self.loop_count == 0:
            print ("Add min loops: 1")
            error = True

        if count == 0:
            print ("Activate servos")
            error = True

        if error:
            return
        response["operation"] = "sequence"
        response["servo_count"] = count
        response["frame_count"] = self.frame_count
        response["frame_speed"] = self.frame_speed * 10
        response["servo_iteration_speed"] = self.servo_speed * 10
        response["dimension"] = 2
        response["loop"]     = self.loop_count
        response["frame"] = self.frames
        response = json.dumps(response)
        print (response)
        ser_obj = self.getSerial()
        ser_obj.write(response.encode('ascii'))
        print (ser_obj.readline())



    def slider_control(self, slider):
        for count, sliderObj in enumerate(self.slider_list):

            if sliderObj == slider:
                self.servo_label_list[count].setText(str(slider.value()))
                serial_obj = self.getSerial()
                buf = {}
                buf["operation"] = "run"
                servo =  ""
                servo = (self.activated_sliders[count])
                buf["servo"] = servo
                buf["position"] = int(slider.value())
                buf = json.dumps(buf)
                serial_obj.write(buf.encode('ascii'))


    def disable_sliders(self):
        for count, slider in enumerate(self.slider_list):
            slider.setEnabled(False)

    def enable_sliders(self, checkBox_obj):

        for count, checkBox in enumerate(self.checkbox_list):
            if checkBox_obj == checkBox:
                self.slider_list[count].setEnabled(checkBox.isChecked())
                self.activated_sliders[count] = count


    def getSerial(self):
        serial_obj = serial.Serial( str(self.com_port_input.text()),
                            baudrate = 9600,
                            timeout  = 2,
                            parity=serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS,
                            stopbits=serial.STOPBITS_ONE
                            )
        return serial_obj

    def connect_board(self):
        """
        The function is intended to initiate the connection to the controller board.

        The function uses a standard JSON format for message delivery. Based on the ACK
        received from the controller board the Labels are updated.
        outgoing_buffer = {"operation" : "Connect"}
        incoming_buffer = {"Success" : True} or {"Success" : False}
        """
        print ("Connecting board...")
        if self.com_port_input.text() == "":
            print ("Enter com port details")
            return
        try:
            serial_obj = self.getSerial()
        except Exception as e:
            print (e)
            return
        buf = {}
        buf["operation"] = "Connect"
        buf = json.dumps(buf)
        if serial_obj.isOpen():
            try:
                serial_obj.write(buf.encode('ascii'))
                serial_obj.flush()
            except Exception as e:
                print (e)
            try:
                incoming = serial_obj.readline().decode("utf-8")
                incoming = json.loads(incoming)

                if (incoming["Success"] == True):
                    print ("Connection Success")
                    self.status_label.setText("Success")
                    self.connectionStatus = incoming["Success"]
                    self.groupBox_3.setEnabled(incoming["Success"])


                elif(incoming["Success"] == False):
                    print ("Connection Failure")
                    self.status_label.setText("Failure")
                    self.connectionStatus = incoming["Success"]
                    self.groupBox_3.setEnabled(incoming["Success"])
            except Exception as e:
                print (e)
            serial_obj.close()
        else:
            print ("Connection seems to be closed...")

def main():
    app = QApplication(sys.argv)
    widget = App()
    widget.show()
    widget.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
