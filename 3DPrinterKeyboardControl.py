import pygame
import time
import sys
import serial

# Establish a connection with the printer using the specified serial port and baud rate
# You'll need to replace "/dev/tty.usbserial-2120" with whatever your serial port ID is
# To find out the serial port ID, type "ls /dev/tty*" in the terminal and find the one that matches the format below
ser = serial.Serial("/dev/tty.usbserial-2120", 115200)

# Keep motors engaged
ser.write(str.encode("M84 X Y Z S12000\r\n"))


# Set the positioning to absolute
ser.write(str.encode("G90\r\n"))

# Home the device
ser.write(str.encode("G28\r\n"))

# Move to a reference point in the X, Y, and Z axes
ser.write(str.encode("G1 X125 Y125 Z75r\n"))

# Set the positioning to relative
ser.write(str.encode("G91\r\n"))

# Pause until the moves are completed
ser.write(str.encode("M400\r\n"))

# Send a message to the printer
ser.write(str.encode("M118 E1 Iamready\r\n"))

Tcat = ""
while "Iamready" not in Tcat:
    T = ser.read()  # Read data from the printer
    Tcat += T.decode()  # Convert the bytes to a string

# Initialize Pygame
pygame.init()

z = 0
x = 0
y = 0
tiempo1 = 0.1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Check for key presses and send corresponding G-code commands to the printer
    if keys[pygame.K_q]:
        running = False
    if keys[pygame.K_w]:
        # Move the Z-axis up
        time.sleep(0.02)
        ser.write(str.encode("G1 Z0.5 F5000\r\n"))
    if keys[pygame.K_s]:
        # Move the Z-axis down
        time.sleep(0.02)
        ser.write(str.encode("G1 Z-0.5 F5000\r\n"))
    if keys[pygame.K_LEFT]:
        # Move the X-axis to the left
        time.sleep(0.02)
        ser.write(str.encode("G1 X-0.5 F5000\r\n"))
    if keys[pygame.K_RIGHT]:
        # Move the X-axis to the right
        time.sleep(0.02)
        ser.write(str.encode("G1 X0.5 F5000\r\n"))
    if keys[pygame.K_UP]:
        # Move the Y-axis up
        time.sleep(0.02)
        ser.write(str.encode("G1 Y0.5 F5000\r\n"))
    if keys[pygame.K_DOWN]:
        # Move the Y-axis down
        time.sleep(0.02)
        ser.write(str.encode("G1 Y-0.5 F5000\r\n"))
    if keys[pygame.K_o]:
        # Turn on the laser
        time.sleep(0.02)
        ser.write(str.encode("M106\r\n"))
    if keys[pygame.K_p]:
        # Turn on the laser
        time.sleep(0.02)
        ser.write(str.encode("M107\r\n"))
    if keys[pygame.K_SPACE]:
        # Turn off the laser, then turn it on briefly, and turn it off again
        time.sleep(0.02)
        ser.write(str.encode("M107\r\n"))
        ser.write(str.encode("M106 S20\r\n"))
        time.sleep(tiempo1)
        ser.write(str.encode("M107\r\n"))

# Quit Pygame
pygame.quit()
sys.exit()
