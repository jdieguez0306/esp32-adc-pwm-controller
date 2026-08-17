# ESP32 ADC & PWM Controller

An embedded systems project built with an ESP32 and MicroPython that uses analog input, PWM output, hardware timers, and GPIO interrupts to dynamically control an LED.

A potentiometer provides analog input through the ESP32 ADC, while an onboard push button switches between LED frequency control and duty-cycle control modes.

## Features

* Reads analog potentiometer values using the ESP32 ADC
* Maps ADC values to PWM frequency
* Maps ADC values to PWM duty cycle
* Controls LED brightness using PWM
* Controls LED flashing frequency using PWM
* Uses a GPIO interrupt for mode switching
* Implements button debouncing using a one-shot timer
* Uses periodic hardware timers for ADC sampling
* Uses the ESP32 real-time clock
* Periodically outputs the current date and time
* Demonstrates event-driven embedded programming

## Hardware

### Components

* ESP32 development board
* Potentiometer
* LED
* Current-limiting resistor
* Push button
* Breadboard and jumper wires

### Pin Configuration

| ESP32 Pin | Function                |
| --------- | ----------------------- |
| GPIO 32   | Potentiometer ADC input |
| GPIO 25   | PWM LED output          |
| GPIO 38   | Push-button input       |
| 3.3V      | Potentiometer power     |
| GND       | Common ground           |

The potentiometer is connected between `3.3V` and `GND`, with its output connected to GPIO 32.

The LED is connected to GPIO 25 through a current-limiting resistor.

## System Behavior

The project operates using two primary LED control modes.

### Frequency Control

The potentiometer controls the PWM frequency.

Raw 12-bit ADC values from:

```text
0 – 4095
```

are mapped to a PWM frequency range of approximately:

```text
1 – 20 Hz
```

The conversion is performed using:

```python
def adc_to_freq(potent_val):
    potent_val = max(0, min(4095, potent_val))

    return int(
        1 + (potent_val / 4095) * (20 - 1)
    )
```

### Duty-Cycle Control

In duty-cycle mode, the potentiometer controls the LED's PWM duty cycle.

ADC values from:

```text
0 – 4095
```

are mapped to:

```text
0 – 1023
```

for the PWM duty cycle.

```python
def adc_to_duty(potent_val):
    potent_val = max(0, min(4095, potent_val))

    return int(
        (potent_val / 4095) * 1023
    )
```

## Interrupt-Driven Mode Selection

A push button connected to GPIO 38 is configured using a GPIO interrupt.

Each button press switches between:

```text
Frequency Control
        ↓
Duty Cycle Control
        ↓
Frequency Control
```

Rather than continuously polling the button, the ESP32 responds when a GPIO edge occurs.

## Button Debouncing

Mechanical buttons can generate multiple electrical transitions from a single physical press.

A one-shot hardware timer provides a 250 ms debounce period:

```python
debounce_timer.init(
    period=250,
    mode=Timer.ONE_SHOT,
    callback=debounce_callback
)
```

During this period, additional button interrupts are ignored.

## Periodic ADC Sampling

A hardware timer samples the potentiometer every 100 milliseconds:

```python
adc_timer.init(
    period=100,
    mode=Timer.PERIODIC,
    callback=read_potent_val
)
```

The ADC value is then passed to the LED-control logic.

This allows the system to continuously respond to changes in the potentiometer without using a blocking loop.

## Real-Time Clock

The ESP32 real-time clock is initialized using user-provided date and time values.

Another hardware timer prints the current time every 30 seconds.

This demonstrates concurrent use of multiple embedded peripherals and timers.

## Technologies and Concepts

* ESP32
* MicroPython
* Embedded Systems
* GPIO
* ADC
* PWM
* Hardware Timers
* Interrupts
* Interrupt Service Routines
* Button Debouncing
* Real-Time Clock
* Event-Driven Programming
* Analog Signal Processing

## Demo

A hardware demonstration of the project is available on YouTube:

[https://youtube.com/shorts/6F26hjBgWnc](https://youtube.com/shorts/6F26hjBgWnc?si=VXKE9Pn_JCJemtdp)

## Running the Project

This program is intended to run on an ESP32 using MicroPython.

Upload:

```text
main.py
```

to the ESP32 and execute it using a MicroPython-compatible development environment such as Thonny.

The program will first request the current date and time before initializing the hardware timers and LED controls.


## Skills

`ESP32` `MicroPython` `Embedded Systems` `ADC` `PWM` `Interrupts` `Timers` `GPIO`
