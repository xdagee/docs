# The Apprentice's Handbook

## Introduction

This handbook is your field guide to the **STEMAIDE Kit**. While the "Missions" (Level 1, 2, 3) teach you how to build specific projects, this guide provides the technical reference data you might need along the way.

---

## 1. Safety First

Before you build, remember the **Innovator's Code**:

1. **Never** connect wires while the board is plugged into the computer.
2. **Double-check** your wiring (especially VCC and GND) before powering up.
3. **Keep it tidy.** A messy circuit is hard to debug.

---

## 2. Component Cheatsheet

### Digital Outputs (Actuators)

* **LEDs**: Light Emitting Diodes. Beware of polarity (Long leg is +).
* **Buzzer**: Makes sound. Active buzzers need only 5V; Passive buzzers need a signal.
* **Traffic Light Module**: Pins are R, Y, G, GND.

### Analog Inputs (Sensors)

* **LDR (Light Dependent Resistor)**: Resistance changes with light. Good for "Smart Street Lights".
* **Potentiometer**: A knob that changes resistance. Good for dials and volume.

### Digital Inputs

* **Push Button**: Connects two points when pressed. Use `INPUT_PULLUP` to make wiring easier.

### Smart Modules

* **Ultrasonic Sensor (HC-SR04)**: Measures distance using sound. Echolocation!
* **Servo Motor**: Moves to a specific angle (0-180 degrees).

---

## 3. Common Troubleshooting

**"My Code Won't Upload!"**

* Check the USB Cable. Is it plugged in firmly?
* Check **Tools > Board**. Is "Arduino Uno" selected?
* Check **Tools > Port**. Is the correct COM port selected?

**"The circuit isn't working!"**

* Check **GND**. Is everything connected to Ground?
* Check **Pin Numbers**. Did you plug the LED into Pin 6 but program Pin 5?
* Check **Polarity**. Are your LEDs plugged in backwards?

---

## 4. Need Help?

* Ask a Mentor in your local STEMAIDE Lab.
* Check the [Online Community](https://stemaide.com).
