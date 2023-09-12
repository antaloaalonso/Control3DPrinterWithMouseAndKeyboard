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

# Screen dimensions
WIDTH, HEIGHT = 1000, 1000

# Initialize the Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse Control")

# Initial values of x and y
x, y = WIDTH // 2, HEIGHT // 2
monitor_mouse = True

running = True
while running:
    time.sleep(0.02)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button click
                ser.write(str.encode("M106\r\n"))  # Turn on laser
                print("laser on")
            elif event.button == 2:  # Middle mouse button click
                # Toggle the flag to stop/start monitoring the mouse position
                monitor_mouse = not monitor_mouse
                print("Mouse monitoring is", "on" if monitor_mouse else "off")
            elif event.button == 3:  # Right mouse button click
                ser.write(str.encode("M107\r\n"))  # Turn off laser
                print("laser off")

    keys = pygame.key.get_pressed()

    # Check for keyboard input or mouse movement and send corresponding G-code commands to 3D printer
    if keys[pygame.K_UP]:
        ser.write(str.encode("G91\r\n"))
        ser.write(str.encode("G1 Z1\r\n"))
        time.sleep(0.1)
        print("UP")
        ser.write(str.encode("G90\r\n"))
        time.sleep(0.1)
    if keys[pygame.K_DOWN]:
        ser.write(str.encode("G91\r\n"))
        ser.write(str.encode("G1 Z-1\r\n"))
        time.sleep(0.1)
        print("DOWN")
        ser.write(str.encode("G90\r\n"))
        time.sleep(0.1)
    if keys[pygame.K_SPACE]:
        ser.write(str.encode("M106 S20\r\n"))  # Turn on laser
        time.sleep(0.1)
        ser.write(str.encode("M107\r\n"))  # Turn off laser
        print("SPACE")
    if keys[pygame.K_q]:
        running = False
    if monitor_mouse:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Ensure x and y values stay within the range 0 to 250
        x = max(0, min(mouse_x, 1000))
        y = max(0, min(mouse_y, 1000))
        y = 1000-y
        orden = "G1 " + "X" + str(x / 4) + " Y" + str(y / 4) + "F5000\r\n"
        print(orden)
        ser.write(str.encode(orden))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw a circle at the current (x, y) position
    pygame.draw.circle(screen, (255, 0, 0), (x, 1000-y), 10)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
