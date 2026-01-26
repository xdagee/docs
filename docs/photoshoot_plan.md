# Photoshoot Plan: Updating Visuals for Gold Standard

This document outlines the images that need to be re-taken or re-created to match the new **Standard Wiring** in the documentation. The code has been updated to enforce these standards, so the "Physical Wiring" images are now the only thing out of sync.

## 1. The New "Gold Standard" Pinout

Ensure all photos follow this master key. **Do not deviate.**

| Component | Pin Label | **Standard Arduino Pin** | Color |
| :--- | :--- | :--- | :--- |
| **RGB LED** | **R** | **Pin 3** | Red Wire |
| | **G** | **Pin 5** | Green Wire |
| | **B** | **Pin 6** | Blue Wire |
| | **-** | **GND** | Black Wire |
| **Traffic Light** | **R** | **Pin 5** | Red Wire |
| | **Y** | **Pin 6** | Yellow Wire |
| | **G** | **Pin 7** | Green Wire |
| | **GND** | **GND** | Black Wire |
| **Push Button** | **Leg A** | **Pin 2** | Red Wire |
| | **Leg B** | **GND** | Black Wire |
| **Servo Motor** | **Signal** | **Pin 10** | Orange Wire |
| **Ultrasonic** | **Trig** | **Pin 12** | Green Wire |
| | **Echo** | **Pin 11** | Yellow Wire |

---

## 2. Shot List (Priority Order)

### Priority A: Level 1 Basics

*These are the foundation. If these are wrong, beginners will get confused immediately.*

#### 1. RGB Module (Ref: `1.5.0` & `1.5.1`)

* **Target Image**: Breadboard view of RGB Module connected to **3, 5, 6**.
* **Why**: Old images show random pins (2,7,10 or 9,10,11) which breaks Color Mixing code.
* **Shot**: Close up of the 4 wires going into Digital ~3, ~5, ~6 and GND.

#### 2. Traffic Light (Ref: `1.4.0`)

* **Target Image**: Traffic Light Module connected to **5, 6, 7**.
* **Why**: Standardizing this makes Level 2 easier.
* **Shot**: Red to 5, Yellow to 6, Green to 7.

#### 3. Push Button (Ref: `1.3.1`)

* **Target Image**: One leg to **Pin 2**, One leg to **GND**.
* **Why**: We removed the complex resistor wiring. The photo should show the *Simplified* 2-wire setup (using `INPUT_PULLUP`).
* **Shot**: Very clean, just 2 wires.

---

### Priority B: Level 2 Combinations

*These are critical because they combine components. The wiring MUST support both parts.*

#### 4. Ultrasonic + RGB (Ref: `2.4.1`)

* **Target Image**:
  * Ultrasonic on **11, 12**.
  * RGB on **3, 5, 6**.
* **Why**: The old project had conflicts. This is the new conflict-free spacing.

#### 5. Ultrasonic + Traffic Light (Ref: `2.3.1`)

* **Target Image**:
  * Ultrasonic on **11, 12**.
  * Traffic Light on **5, 6, 7**.
* **Why**: Previously, Ultrasonic was on 2,3 which blocks the Button. This new layout is "Future Proof".

#### 6. PushButton + RGB (Ref: `2.8.1`)

* **Target Image**:
  * Button on **Pin 2**.
  * RGB on **3, 5, 6**.
* **Why**: Demonstrates input (2) and PWM output (3,5,6) working together.

---

## 3. Style Guidelines

* **Angle**: Top-down or high 45-degree angle.
* **Background**: Clean white or gray background (no cluttered desks).
* **Wire Colors**: Match the wire colors to the component if possible (Red wire for Red Pin, etc.) to make it "Glanceable".
* **Focus**: Sharp focus on the **Arduino Pins** so users can count the holes.
