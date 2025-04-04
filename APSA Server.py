from flask import Flask, render_template
import gpiod

app = Flask(__name__)

# Define the GPIO chip
chip = gpiod.Chip("gpiochip0")

# Map the output numbers to specific GPIO pin numbers
output_pin_mapping = {
    1: 16,
    2: 18,
    3: 22,
    4: 11,
    5: 13,
    6: 15,
    7: 29,
    8: 31,
}

# Create a dictionary to hold the line objects for each output
lines = {}

# Initialize the GPIO lines for each output pin
for output_num, pin in output_pin_mapping.items():
    line = chip.get_line(pin)
    line.request(consumer="webgpio", type=gpiod.LINE_REQ_DIR_OUT)
    lines[output_num] = line

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/output_<int:output_num>/on")
def gpio_on(output_num):
    if output_num in lines:
        print(f"Turning on GPIO {output_num} (Pin {output_pin_mapping[output_num]})")
        lines[output_num].set_value(1)
        return f"OUTPUT {output_num} ON"
    return f"Invalid output {output_num}"

@app.route("/output_<int:output_num>/off")
def gpio_off(output_num):
    if output_num in lines:
        print(f"Turning off GPIO {output_num} (Pin {output_pin_mapping[output_num]})")
        lines[output_num].set_value(0)
        return f"OUTPUT {output_num} OFF"
    return f"Invalid output {output_num}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
