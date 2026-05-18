"""Insert schematic diagram references into mission Markdown files.

Adds a schematic SVG reference ABOVE the existing breadboard photo
in each mission's Blueprint section, following the convention:
  ![Schematic Diagram](path/to/schematic.svg)
  *Schematic Diagram — Logical Wiring*

  ![Breadboard Photo](existing/photo.webp)
  *Breadboard Photo — Physical Assembly Reference*

Usage:
    python scripts/insert_schematics.py
"""

import os
import re

DOCS_DIR = "docs"
SCHEMATIC_DIR = "assets/schematics"

# Mapping: mission file path prefix -> schematic filename
# Keys are matched against the relative path from docs/
MAPPINGS: list[tuple[str, str]] = [
    # Level 1 — LED
    ("1.0/1.1.LED/1.1.1.", "schematic_1.1_single_led.svg"),
    ("1.0/1.1.LED/1.1.2.", "schematic_1.1_single_led.svg"),
    ("1.0/1.1.LED/1.1.3.", "schematic_1.1_double_led.svg"),
    ("1.0/1.1.LED/1.1.4.", "schematic_1.1_double_led.svg"),
    ("1.0/1.1.LED/1.1.5.", "schematic_1.1_triple_led.svg"),
    ("1.0/1.1.LED/1.1.6.", "schematic_1.1_triple_led.svg"),
    ("1.0/1.1.LED/1.1.7.", "schematic_1.1_quad_led.svg"),
    ("1.0/1.1.LED/1.1.8.", "schematic_1.1_quad_led.svg"),
    ("1.0/1.1.LED/1.1.9.", "schematic_1.1_five_led.svg"),
    ("1.0/1.1.LED/1.1.10.", "schematic_1.1_five_led.svg"),
    # Level 1 — Buzzer
    ("1.0/1.2.Buzzer/", "schematic_1.2_buzzer.svg"),
    # Level 1 — Push Button
    ("1.0/1.3.Push_Button/", "schematic_1.3_button_led.svg"),
    # Level 1 — Traffic Light
    ("1.0/1.4.Traffic_Light/", "schematic_1.4_traffic_light.svg"),
    # Level 1 — RGB
    ("1.0/1.5.RGB/", "schematic_1.5_rgb_module.svg"),
    # Level 1 — LDR
    ("1.0/1.6.LDR/", "schematic_1.6_ldr.svg"),
    # Level 1 — Servo
    ("1.0/1.7.Servo_Motor/", "schematic_1.7_servo.svg"),
    # Level 1 — Ultrasonic
    ("1.0/1.8.Ultrasonic_Sensor/", "schematic_1.8_ultrasonic_rgb.svg"),
    # Level 1 — Sound Sensor
    ("1.0/1.9.Sound_Sensor/", "schematic_1.9_sound_sensor.svg"),
    # Level 2
    ("2.0/2.1.Ultrasonic+LED/", "schematic_2.1_ultrasonic_led.svg"),
    ("2.0/2.2.Ultrasonic+Buzzer/", "schematic_2.2_ultrasonic_buzzer.svg"),
    ("2.0/2.3.Ultrasonic+TrafficLight/", "schematic_2.3_ultrasonic_traffic.svg"),
    ("2.0/2.4.Ultrasonic+RGB/", "schematic_2.4_ultrasonic_rgb.svg"),
    ("2.0/2.5.Push_Button+LED/", "schematic_2.5_button_led.svg"),
    ("2.0/2.6.Push_Button+Buzzer/", "schematic_2.6_button_buzzer.svg"),
    ("2.0/2.7.PushButton+TrafficLightModule/", "schematic_2.7_button_traffic.svg"),
    ("2.0/2.8.PushButton+RGB/", "schematic_2.8_button_rgb.svg"),
    ("2.0/2.9.LDR+LED/", "schematic_2.9_ldr_led.svg"),
    ("2.0/2.10.LDR+Buzzer/", "schematic_2.10_ldr_buzzer.svg"),
    ("2.0/2.11.LDR_RGB/", "schematic_2.11_ldr_rgb.svg"),
    ("2.0/2.12.Traffic_Light_STEMAIDE/", "schematic_2.12_ldr_traffic.svg"),
    ("2.0/2.13.SoundSensor+LED/", "schematic_2.13_sound_led.svg"),
    ("2.0/2.14.SoundSensor+Traffic/", "schematic_2.14_sound_traffic.svg"),
    # Level 3
    ("3.0/3.1.Smart_Gauge/", "schematic_3.1_smart_gauge.svg"),
    ("3.0/3.2.Smart_Security_System/", "schematic_3.2_security_system.svg"),
    ("3.0/3.3.Smart_Traffic_light_system/", "schematic_3.3_traffic_system.svg"),
    ("3.0/3.4.Smart_Bed_Light/", "schematic_3.4_bed_light.svg"),
    ("3.0/3.5.Smart_Car_Parking_System/", "schematic_3.5_parking_system.svg"),
    ("3.0/3.6.Smart_Clap_Device/", "schematic_3.6_clap_device.svg"),
    ("3.0/3.7.Smart_Irrigation/", "schematic_3.7_smart_irrigation.svg"),
]

# Pattern to find existing wiring diagram image lines
WIRING_IMG_RE = re.compile(
    r"^(!\[(Wiring Diagram|Circuit Diagram|.*Wiring|.*Circuit|.*Mount|"
    r"Push Button Circuit|RGB Mount|LDR Wiring|Servo Wiring|"
    r"Sound Sensor Wiring|Traffic Light Wiring)\]"
    r"\([^)]+\))$",
    re.MULTILINE,
)


def get_schematic_for_file(rel_path: str) -> str | None:
    """Return the schematic SVG filename for a mission file, or None."""
    normalized = rel_path.replace("\\", "/")
    for prefix, svg in MAPPINGS:
        if normalized.startswith(prefix):
            return svg
    return None


def compute_relative_path(md_file_dir: str, svg_name: str) -> str:
    """Compute the relative path from a mission file to the schematic."""
    schematic_abs = os.path.join(DOCS_DIR, SCHEMATIC_DIR, svg_name)
    return os.path.relpath(schematic_abs, md_file_dir).replace("\\", "/")


def insert_schematic(filepath: str, rel_path: str) -> bool:
    """Insert schematic reference above existing wiring diagram image."""
    svg_name = get_schematic_for_file(rel_path)
    if svg_name is None:
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if schematic already inserted
    if "Schematic Diagram" in content:
        return False

    md_dir = os.path.dirname(filepath)
    svg_rel = compute_relative_path(md_dir, svg_name)

    schematic_block = (
        f"![Schematic Diagram]({svg_rel})\n\n"
        f"*Schematic Diagram — Logical Wiring*\n\n"
    )

    # Try to find existing wiring image and insert before it
    match = WIRING_IMG_RE.search(content)
    if match:
        # Insert schematic block before the existing image
        insert_pos = match.start()
        # Add caption to existing photo
        existing_line = match.group(0)
        replacement = (
            schematic_block
            + existing_line + "\n\n"
            + "*Breadboard Photo — Physical Assembly Reference*"
        )
        new_content = content[:insert_pos] + replacement + content[match.end():]
    else:
        # No existing wiring image found — insert after Blueprint heading
        blueprint_re = re.compile(
            r"(##\s+\d*\.?\s*The Blueprint.*?\n(?:.*?\n)*?"
            r"(?=\n##\s|\Z))",
            re.MULTILINE,
        )
        bp_match = blueprint_re.search(content)
        if bp_match:
            # Insert at end of Blueprint section
            insert_pos = bp_match.end()
            new_content = (
                content[:insert_pos].rstrip() + "\n\n"
                + schematic_block
                + content[insert_pos:]
            )
        else:
            return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main() -> None:
    updated = 0
    skipped = 0

    print("Inserting schematic references into mission files...\n")

    for root, _, files in os.walk(DOCS_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue

            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, DOCS_DIR).replace("\\", "/")

            if get_schematic_for_file(rel_path) is None:
                continue

            if insert_schematic(filepath, rel_path):
                print(f"  Updated: {rel_path}")
                updated += 1
            else:
                skipped += 1

    print(f"\nDone. {updated} files updated, {skipped} skipped (already done or no match).")


if __name__ == "__main__":
    main()
