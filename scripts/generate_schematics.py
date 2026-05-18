"""Generate professional schematic diagrams for all STEMAIDE missions.

Uses schemdraw to produce SVG files stored in docs/assets/schematics/.
Pin assignments follow the Gold Standard from photoshoot_plan.md.

Usage:
    python scripts/generate_schematics.py
"""

import os
import schemdraw
import schemdraw.elements as elm

OUT_DIR = os.path.join("docs", "assets", "schematics")
os.makedirs(OUT_DIR, exist_ok=True)

FONT_SIZE = 13
ARDUINO_COLOR = "#0068B5"
POWER_COLOR = "#CC0000"
GND_COLOR = "#333333"
SIGNAL_COLOR = "#0068B5"


def _save(d: schemdraw.Drawing, name: str) -> None:
    path = os.path.join(OUT_DIR, f"{name}.svg")
    d.save(path)
    print(f"  Created: {path}")


# ---------------------------------------------------------------------------
# Level 1 — Base component schematics
# ---------------------------------------------------------------------------

def gen_led_circuit(n_leds: int, pins: list[int], name: str, title: str) -> None:
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=FONT_SIZE, unit=3)

        # Title
        d.add(elm.Label().at((-1, 2)).label(title))

        # Arduino block
        box_h = max(4, n_leds * 1.5 + 1)
        d.add(elm.RBox(w=3, h=box_h).at((0, -box_h / 2))
              .label("Arduino\nUno").color(ARDUINO_COLOR))

        for i, pin in enumerate(pins):
            y_pos = -i * 1.2
            d.add(elm.Line().at((1.5, y_pos)).right(1)
                  .label(f"Pin {pin}", loc="left").color(SIGNAL_COLOR))
            d.add(elm.Resistor().right().label("220\u03A9", loc="top"))
            d.add(elm.LED().right().label(f"LED{i+1}", loc="top"))
            d.add(elm.Line().right(0.5))
            d.add(elm.Ground())

    _save(d, name)


def gen_buzzer() -> None:
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=FONT_SIZE, unit=3)
        d.add(elm.Label().at((-1, 2)).label("Buzzer Circuit"))

        d.add(elm.RBox(w=3, h=3).at((0, -1.5))
              .label("Arduino\nUno").color(ARDUINO_COLOR))

        d.add(elm.Line().at((1.5, 0)).right(1)
              .label("Pin 3", loc="left").color(SIGNAL_COLOR))
        d.add(elm.Speaker().right().label("Buzzer"))
        d.add(elm.Line().right(0.5))
        d.add(elm.Ground())

    _save(d, "schematic_1.2_buzzer")


def gen_button_led() -> None:
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=FONT_SIZE, unit=3)
        d.add(elm.Label().at((-1, 3)).label("Push Button + LED"))

        d.add(elm.RBox(w=3, h=4).at((0, -2))
              .label("Arduino\nUno").color(ARDUINO_COLOR))

        # Button input
        d.add(elm.Line().at((-1.5, 0)).left(1)
              .label("Pin 2", loc="right").color(SIGNAL_COLOR))
        d.add(elm.Button().left().label("Button", loc="top"))
        d.add(elm.Line().left(0.5))
        d.add(elm.Ground())

        # LED output
        d.add(elm.Line().at((1.5, -1)).right(1)
              .label("Pin 6", loc="left").color(SIGNAL_COLOR))
        d.add(elm.Resistor().right().label("220\u03A9", loc="top"))
        d.add(elm.LED().right().label("LED"))
        d.add(elm.Line().right(0.5))
        d.add(elm.Ground())

        d.add(elm.Label().at((-3, -4))
              .label("INPUT_PULLUP\n(no external resistor)"))

    _save(d, "schematic_1.3_button_led")


def gen_traffic_light() -> None:
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=FONT_SIZE, unit=3)
        d.add(elm.Label().at((-1, 2.5)).label("Traffic Light Module"))

        d.add(elm.RBox(w=3, h=5).at((0, -2.5))
              .label("Arduino\nUno").color(ARDUINO_COLOR))

        colors = [("Pin 5", "Red", "#CC0000"),
                  ("Pin 6", "Yellow", "#CCAA00"),
                  ("Pin 7", "Green", "#00AA00")]

        for i, (pin, clr_name, clr) in enumerate(colors):
            y = -i * 1.3
            d.add(elm.Line().at((1.5, y)).right(1)
                  .label(pin, loc="left").color(SIGNAL_COLOR))
            d.add(elm.LED().right().label(clr_name, loc="top").color(clr))
            d.add(elm.Line().right(0.5))
            d.add(elm.Ground())

    _save(d, "schematic_1.4_traffic_light")


def gen_rgb_module() -> None:
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=FONT_SIZE, unit=3)
        d.add(elm.Label().at((-1, 2.5)).label("RGB LED Module (PWM)"))

        d.add(elm.RBox(w=3, h=5).at((0, -2.5))
              .label("Arduino\nUno").color(ARDUINO_COLOR))

        colors = [("Pin ~3", "Red", "#CC0000"),
                  ("Pin ~5", "Green", "#00AA00"),
                  ("Pin ~6", "Blue", "#0000CC")]

        for i, (pin, clr_name, clr) in enumerate(colors):
            y = -i * 1.3
            d.add(elm.Line().at((1.5, y)).right(1)
                  .label(pin, loc="left").color(SIGNAL_COLOR))
            d.add(elm.LED().right().label(clr_name, loc="top").color(clr))
            d.add(elm.Line().right(0.5))

        d.add(elm.Ground())

    _save(d, "schematic_1.5_rgb_module")


def gen_module_schematic(name: str, title: str, mod_label: str,
                         pin_lines: list[tuple[str, str]]) -> None:
    """Generic 3-4 pin module (LDR, Sound, Servo)."""
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=FONT_SIZE, unit=3)
        d.add(elm.Label().at((-1, 2.5)).label(title))

        n = len(pin_lines)
        box_h = max(3.5, n * 1.2 + 1)
        d.add(elm.RBox(w=3, h=box_h).at((0, -box_h / 2))
              .label("Arduino\nUno").color(ARDUINO_COLOR))

        for i, (lbl, clr) in enumerate(pin_lines):
            y = -i * 1.0
            d.add(elm.Line().at((1.5, y)).right(1.5)
                  .label(lbl, loc="left").color(clr))

        mod_h = n * 1.0 + 0.5
        d.add(elm.RBox(w=2.5, h=mod_h)
              .at((4.75, -(n - 1) * 0.5))
              .label(mod_label).color("#666666"))

    _save(d, name)


def gen_combo(name: str, title: str, sensor: dict, outputs: list[dict]) -> None:
    """Generic combo: one sensor + one or more output blocks."""
    total_pins = len(sensor["pins"]) + sum(len(o["pins"]) for o in outputs)
    box_h = max(5, total_pins * 0.85 + 2)

    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=FONT_SIZE, unit=3)
        d.add(elm.Label().at((-1, box_h / 2 + 0.5)).label(title))

        d.add(elm.RBox(w=3, h=box_h).at((0, -box_h / 2))
              .label("Arduino\nUno").color(ARDUINO_COLOR))

        y = 0.0
        # Sensor
        for lbl, clr in sensor["pins"]:
            d.add(elm.Line().at((1.5, y)).right(2)
                  .label(lbl, loc="left").color(clr))
            y -= 0.8

        s_h = len(sensor["pins"]) * 0.8 + 0.4
        d.add(elm.RBox(w=2.5, h=s_h)
              .at((5, -(len(sensor["pins"]) - 1) * 0.4))
              .label(sensor["label"]).color("#666666"))

        y -= 0.4

        # Outputs
        for out in outputs:
            y_start = y
            for lbl, clr in out["pins"]:
                d.add(elm.Line().at((1.5, y)).right(2)
                      .label(lbl, loc="left").color(clr))
                y -= 0.8

            o_h = len(out["pins"]) * 0.8 + 0.3
            d.add(elm.RBox(w=2.5, h=o_h)
                  .at((5, y_start - o_h / 2 + 0.4))
                  .label(out["label"]).color("#666666"))
            y -= 0.3

    _save(d, name)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Generating STEMAIDE schematics...\n")

    # ---- Level 1 ----
    print("[Level 1] Base components:")
    for n, pins, name, title in [
        (1, [6], "schematic_1.1_single_led", "Single LED Circuit"),
        (2, [5, 6], "schematic_1.1_double_led", "Double LED Circuit"),
        (3, [4, 5, 6], "schematic_1.1_triple_led", "Triple LED Circuit"),
        (4, [4, 5, 6, 7], "schematic_1.1_quad_led", "Quad LED Circuit"),
        (5, [3, 4, 5, 6, 7], "schematic_1.1_five_led", "Five LED Circuit"),
    ]:
        gen_led_circuit(n, pins, name, title)

    gen_buzzer()
    gen_button_led()
    gen_traffic_light()
    gen_rgb_module()

    gen_module_schematic("schematic_1.6_ldr", "LDR Light Sensor", "LDR\nModule", [
        ("5V \u2192 VCC", POWER_COLOR), ("A0 \u2192 AO", SIGNAL_COLOR),
        ("GND \u2192 GND", GND_COLOR)])

    gen_module_schematic("schematic_1.7_servo", "Servo Motor", "Micro\nServo", [
        ("Pin 10 \u2192 Signal", SIGNAL_COLOR),
        ("5V \u2192 Red wire", POWER_COLOR),
        ("GND \u2192 Brown", GND_COLOR)])

    gen_module_schematic("schematic_1.9_sound_sensor", "Sound Sensor", "Sound\nSensor", [
        ("5V \u2192 VCC", POWER_COLOR), ("A0 \u2192 OUT", SIGNAL_COLOR),
        ("GND \u2192 GND", GND_COLOR)])

    # Ultrasonic + RGB (compound L1)
    gen_combo("schematic_1.8_ultrasonic_rgb", "Ultrasonic + RGB",
              {"label": "HC-SR04", "pins": [
                  ("5V \u2192 VCC", POWER_COLOR), ("Pin 12 \u2192 Trig", SIGNAL_COLOR),
                  ("Pin 11 \u2192 Echo", SIGNAL_COLOR), ("GND", GND_COLOR)]},
              [{"label": "RGB\nLED", "pins": [
                  ("Pin ~3 \u2192 R", "#CC0000"), ("Pin ~5 \u2192 G", "#00AA00"),
                  ("Pin ~6 \u2192 B", "#0000CC"), ("GND \u2192 -", GND_COLOR)]}])

    # ---- Level 2 ----
    print("\n[Level 2] Combinations:")
    US = {"label": "HC-SR04", "pins": [
        ("5V \u2192 VCC", POWER_COLOR), ("Pin 12 \u2192 Trig", SIGNAL_COLOR),
        ("Pin 11 \u2192 Echo", SIGNAL_COLOR), ("GND", GND_COLOR)]}
    BTN = {"label": "Push\nButton", "pins": [
        ("Pin 2 \u2192 Leg A", SIGNAL_COLOR), ("GND \u2192 Leg B", GND_COLOR)]}
    LDR = {"label": "LDR\nModule", "pins": [
        ("5V \u2192 VCC", POWER_COLOR), ("A0 \u2192 AO", SIGNAL_COLOR),
        ("GND", GND_COLOR)]}
    SND = {"label": "Sound\nSensor", "pins": [
        ("5V \u2192 VCC", POWER_COLOR), ("A0 \u2192 OUT", SIGNAL_COLOR),
        ("GND", GND_COLOR)]}
    LED1 = {"label": "LED", "pins": [("Pin 6 \u2192 LED+", SIGNAL_COLOR)]}
    BUZZ = {"label": "Buzzer", "pins": [("Pin 3 \u2192 Buzzer+", SIGNAL_COLOR)]}
    TL = {"label": "Traffic\nLight", "pins": [
        ("Pin 5 \u2192 R", "#CC0000"), ("Pin 6 \u2192 Y", "#CCAA00"),
        ("Pin 7 \u2192 G", "#00AA00"), ("GND", GND_COLOR)]}
    RGB = {"label": "RGB\nLED", "pins": [
        ("Pin ~3 \u2192 R", "#CC0000"), ("Pin ~5 \u2192 G", "#00AA00"),
        ("Pin ~6 \u2192 B", "#0000CC"), ("GND \u2192 -", GND_COLOR)]}

    for fname, title, sensor, outputs in [
        ("schematic_2.1_ultrasonic_led", "Ultrasonic + LED", US, [LED1]),
        ("schematic_2.2_ultrasonic_buzzer", "Ultrasonic + Buzzer", US, [BUZZ]),
        ("schematic_2.3_ultrasonic_traffic", "Ultrasonic + Traffic Light", US, [TL]),
        ("schematic_2.4_ultrasonic_rgb", "Ultrasonic + RGB", US, [RGB]),
        ("schematic_2.5_button_led", "Button + LED", BTN, [LED1]),
        ("schematic_2.6_button_buzzer", "Button + Buzzer", BTN, [BUZZ]),
        ("schematic_2.7_button_traffic", "Button + Traffic Light", BTN, [TL]),
        ("schematic_2.8_button_rgb", "Button + RGB", BTN, [RGB]),
        ("schematic_2.9_ldr_led", "LDR + LED", LDR, [LED1]),
        ("schematic_2.10_ldr_buzzer", "LDR + Buzzer", LDR, [BUZZ]),
        ("schematic_2.11_ldr_rgb", "LDR + RGB", LDR, [RGB]),
        ("schematic_2.12_ldr_traffic", "LDR + Traffic Light", LDR, [TL]),
        ("schematic_2.13_sound_led", "Sound Sensor + LED", SND, [LED1]),
        ("schematic_2.14_sound_traffic", "Sound + Traffic Light", SND, [TL]),
    ]:
        gen_combo(fname, title, sensor, outputs)

    # ---- Level 3 ----
    print("\n[Level 3] Smart Systems:")
    for fname, title, sensor, outputs in [
        ("schematic_3.1_smart_gauge", "Smart Gauge",
         US, [{"label": "Red LED", "pins": [("Pin 6 \u2192 R", "#CC0000")]},
              {"label": "Green LED", "pins": [("Pin 7 \u2192 G", "#00AA00")]}]),
        ("schematic_3.2_security_system", "Smart Security System",
         US, [{"label": "Buzzer", "pins": [("Pin 3 \u2192 Buzzer", SIGNAL_COLOR)]},
              {"label": "Red LED", "pins": [("Pin 6 \u2192 Alarm", "#CC0000")]}]),
        ("schematic_3.3_traffic_system", "Smart Traffic System",
         US, [TL, {"label": "Servo", "pins": [
              ("Pin 10 \u2192 Signal", SIGNAL_COLOR), ("5V \u2192 Red", POWER_COLOR)]}]),
        ("schematic_3.4_bed_light", "Smart Bed Light",
         LDR, [{"label": "LEDs", "pins": [
              ("Pin 6 \u2192 LED1", SIGNAL_COLOR), ("Pin 7 \u2192 LED2", SIGNAL_COLOR)]}]),
        ("schematic_3.5_parking_system", "Smart Car Parking",
         US, [{"label": "Servo", "pins": [
              ("Pin 10 \u2192 Signal", SIGNAL_COLOR), ("5V \u2192 Red", POWER_COLOR)]},
              {"label": "LEDs", "pins": [
              ("Pin 6 \u2192 Red", "#CC0000"), ("Pin 7 \u2192 Green", "#00AA00")]}]),
        ("schematic_3.6_clap_device", "Smart Clap Device",
         SND, [{"label": "LEDs", "pins": [
              ("Pin 6 \u2192 LED1", SIGNAL_COLOR), ("Pin 7 \u2192 LED2", SIGNAL_COLOR)]}]),
        ("schematic_3.7_smart_irrigation", "Smart Irrigation",
         LDR, [{"label": "Servo\n(Valve)", "pins": [
              ("Pin 9 \u2192 Signal", SIGNAL_COLOR), ("5V \u2192 Red", POWER_COLOR)]},
              {"label": "Status\nLEDs", "pins": [
              ("Pin 6 \u2192 Red", "#CC0000"), ("Pin 7 \u2192 Green", "#00AA00"),
              ("Pin 8 \u2192 Blue", "#0000CC")]}]),
    ]:
        gen_combo(fname, title, sensor, outputs)

    # Cleanup test files
    for f in ("_test.svg", "_test2.svg"):
        p = os.path.join(OUT_DIR, f)
        if os.path.exists(p):
            os.remove(p)

    total = len([f for f in os.listdir(OUT_DIR) if f.endswith(".svg")])
    print(f"\nDone. {total} schematics generated in {OUT_DIR}/")


if __name__ == "__main__":
    main()
