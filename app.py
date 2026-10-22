from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

# Complete Smart Room & Study State
state = {
    "mode": "Balanced Study",
    "lights": "Natural Daylight (4500K)",
    "brightness": "75%",
    "noise_suppression": "Off",
    "timer_active": False,
    "temperature": "23.5°C",
    "air_quality": "Good (AQI 42)",
    "desk_lamp": "Auto-Adjust",
    "tasks": [
        {"task": "Complete Engineering Assignment", "priority": "High"},
        {"task": "Practice C Programming Loops", "priority": "Medium"},
        {"task": "Prepare Lab Records", "priority": "Normal"}
    ]
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/command", methods=["POST"])
def run_command():
    data = request.get_json() or {}
    cmd = data.get("command", "").lower().strip()

    if "focus" in cmd or "study" in cmd:
        state["mode"] = "Deep Focus Sprint"
        state["lights"] = "Cool White (6500K) - 100% Brightness"
        state["noise_suppression"] = "Active (White Noise)"
        state["timer_active"] = True
        state["desk_lamp"] = "Focused High Beam"
        msg = "Deep focus sprint initiated. Lights set to cool white and 25 minute timer started."

    elif "relax" in cmd or "ambient" in cmd or "break" in cmd:
        state["mode"] = "Ambient Break"
        state["lights"] = "Warm Amber (2700K) - 40% Dim"
        state["noise_suppression"] = "Lo-Fi Audio Channel"
        state["timer_active"] = False
        state["desk_lamp"] = "Soft Warm Glow"
        msg = "Switching to ambient relaxation mode. Enjoy your break."

    elif "exam" in cmd:
        state["mode"] = "Strict Exam Revision"
        state["lights"] = "High Contrast Daylight (5000K)"
        state["noise_suppression"] = "Binaural Beats (Beta Waves)"
        state["timer_active"] = True
        state["desk_lamp"] = "Full Intensity"
        msg = "Exam revision mode active. Background notifications silenced."

    elif "add" in cmd or "task" in cmd:
        clean_task = cmd.replace("add", "").replace("task", "").replace("alexa", "").strip().title()
        if not clean_task:
            clean_task = "Review Engineering Syllabus"
        state["tasks"].insert(0, {"task": clean_task, "priority": "Urgent"})
        msg = f"Logged new assignment: {clean_task} into your active academic board."

    else:
        msg = f"Processed command across your connected room hub."

    return jsonify({
        "alexa_reply": msg,
        "device_state": state,
        "time": datetime.datetime.now().strftime("%H:%M:%S")
    })

@app.route("/api/state")
def get_state():
    return jsonify(state)

if __name__ == "__main__":
    app.run(debug=True, port=5000)