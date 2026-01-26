# Welcome to STEMAIDE

**Your journey into STEM starts here!**

The **STEMAIDE Kit** is your toolkit for building the future. With over 200 possible projects, you will learn how to control lights, make sounds, sense the environment, and build smart systems.

This guide will help you set up your computer so you can start programming your STEMAIDE board immediately.

## What You Need

Before we begin, make sure you have:

1. **A Laptop or Desktop Computer** (Windows, Mac, or Linux).
2. **The STEMAIDE Kit** (specifically the Arduino Uno board and the blue USB cable).
3. **Curiosity!**

---

## 1. Setting Up the Software (Arduino IDE)

The **Arduino IDE** (Integrated Development Environment) is the software we use to write code and send it to the board. Think of it as a text editor that talks to hardware.

**Step 1: Open the Software**
Double-click the **Arduino IDE** icon on your computer.

![Arduino IDE logo](../assets/Arduino_IDE.png)

**Step 2: The Interface**
When it opens, you will see a window like this. This is where you will write your code.

![First interface of IDE](../assets/third_interface.png)

### Key Areas to Know

* **void setup()**: This runs **once** when you turn on the board. We use it to tell the board what devices are connected (like "I have an LED on pin 6").
* **void loop()**: This runs **forever** in a circle. This is where the magic happens (like "Turn LED on... wait... turn off").

---

## 2. Preparing the Code Space

To make coding easier, let's make some space.
Click before `void setup()` and press **Enter** a few times to create a blank space at the top.

**Why?**
We use this top space to give **names** to our pins (e.g., `int led = 6;`). It makes code easier to read!

![Creating space for variables](../assets/creating_space_1.png)

---

## 3. Comments (Notes for Humans)

You will often see lines starting with `//`. These are **Comments**.

* The computer ignores them.
* They are there to help **YOU** understand what the code does.

```cpp
// This is a comment. It does nothing to the board.
pinMode(6, OUTPUT); // This sets pin 6 as an output
```

---

## 4. Connecting Your Board

Now, let's connect your STEMAIDE board to the computer.

**Step 1: Plug it in**
Connect the blue USB cable to the Arduino and your USB port.

**Step 2: Select Board**
Go to **Tools** > **Board** > **Arduino Uno**.

![Select Board](../assets/select_board.png)

**Step 3: Select Port**
Go to **Tools** > **Port** and select the one that says **Arduino Uno** (e.g., COM3, COM5, /dev/tty...).

![Select Port](../assets/select_port.png)

> **Note:** If you don't see "Arduino Uno" next to a port, try unplugging and replugging the cable.

---

## 5. Saving & Uploading

Once you have written code (we'll do that in the next chapter!), you need to send it to the board.

1. **Verify (Check):** Click the **Checkmark** icon. This checks for spelling mistakes in your code.
    ![Verify](../assets/verify.png)
2. **Upload (Send):** Click the **Arrow** icon. This sends the code to the board.
    ![Upload](../assets/upload.png)

**Success!**
When you see "Done uploading" at the bottom, your code is running on the board!

![Done](../assets/done.png)

---

### Ready?

Let's build your first project!
👉 **[Start Mission 1.1: First Light](../1.0/1.1.LED/1.1.1.Mission_First_Light.md)**
