from machine import Pin, UART
import time

# Initialize UART communication between the two Picos
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# Initialize LEDs for traffic lights (Green, Yellow, Red)
green_led = Pin(18, Pin.OUT)
yellow_led = Pin(19, Pin.OUT)
red_led = Pin(20, Pin.OUT)

# Initialize buttons for car sensor and reset
button_car_sensor = Pin(10, Pin.IN, Pin.PULL_DOWN)  # Button for detecting cars
button_reset = Pin(11, Pin.IN, Pin.PULL_DOWN)  # Button to start/reset traffic light cycle

# Function to control the North/South traffic light cycle
def traffic_light_north_south():
    # Red light (all cars stop)
    red_led.value(1)  # Turn on Red
    green_led.value(0)  # Turn off Green
    yellow_led.value(0)  # Turn off Yellow
    time.sleep(3)  # Red light for 3 seconds

    # Green light A (cars move for 5 seconds)
    red_led.value(0)  # Turn off Red
    green_led.value(1)  # Turn on Green
    time.sleep(5)  # Green A for 5 seconds

    # Check for cars at Green B
    if button_car_sensor.value() == 0:  # If no cars detected, stay in Green B for 5 more seconds
        time.sleep(5)
    else:
        green_led.value(0)
        yellow_led.value(1)  # Switch to Yellow if cars detected
        time.sleep(3)  # Yellow light for 3 seconds

    # Return to Red after Yellow
    yellow_led.value(0)
    red_led.value(1)  # Turn on Red again
    time.sleep(3)

# Function to send a signal over UART
def send_signal(signal):
    uart.write(signal)  # Send the signal over UART

# Function to receive a signal over UART
def receive_signal():
    if uart.any():  # Check if any data is available to read
        return uart.read().decode('utf-8')  # Read and decode the incoming signal
    return None  # Return None if no data is available

# Main function to control the traffic lights
def main():
    while True:
        # Start the traffic light cycle when the reset button is pressed
        if button_reset.value() == 1:  # If the reset button is pressed
            send_signal('start')  # Notify the other Pico to start
            traffic_light_north_south()  # Run the traffic light sequence
        
        # Check for incoming signals from the other Pico
        signal = receive_signal()  # Receive signal
        if signal == 'start':  # If the signal is 'start', run the traffic light sequence
            traffic_light_north_south()

# Call the main function to start the program
main()
