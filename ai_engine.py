import cv2
import pyttsx3
import time
import random
from sklearn.tree import DecisionTreeClassifier

# ---------------- VOICE SETUP ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

last_alert_time = 0

def speak_alert(msg):
    global last_alert_time
    if time.time() - last_alert_time > 5:
        engine.say(msg)
        engine.runAndWait()
        last_alert_time = time.time()

# ---------------- ML MODEL ----------------
# Features: [temperature, violations]
X = [[30, 1], [40, 3], [50, 6], [60, 10]]
y = ["LOW", "MEDIUM", "HIGH", "HIGH"]

model = DecisionTreeClassifier()
model.fit(X, y)

# ---------------- OPENCV DETECTION ----------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera not working!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    violations = 0

    # ---------------- DETECTION LOOP ----------------
    for (x, y, w, h) in faces:

        # simple helmet logic (demo)
        if w > 100:
            helmet = True
        else:
            helmet = False

        if not helmet:
            violations += 1
            color = (0, 0, 255)
            text = "No Helmet"
        else:
            color = (0, 255, 0)
            text = "Helmet OK"

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, text, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # ---------------- SENSOR (SIMULATED) ----------------
    temperature = random.randint(30, 70)

    # ---------------- RISK CALCULATION ----------------
    risk_score = temperature * 0.5 + violations * 10

    # ---------------- ML RISK ----------------
    risk = model.predict([[temperature, violations]])[0]

    # ---------------- SEND DATA TO DASHBOARD ----------------
    with open("data.txt", "w") as f:
        f.write(f"{temperature},{violations},{risk}")

    # ---------------- DISPLAY ----------------
    if risk == "HIGH":
        color = (0, 0, 255)
        speak_alert("Danger! High risk detected")
    elif risk == "MEDIUM":
        color = (0, 255, 255)
        speak_alert("Warning! Medium risk")
    else:
        color = (0, 255, 0)

    cv2.putText(frame, f"Temp: {temperature}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(frame, f"Violations: {violations}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(frame, f"Risk: {risk}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.putText(frame, f"Score: {int(risk_score)}", (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # ---------------- WINDOW ----------------
    cv2.imshow("SafeSense AI", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()