from ultralytics import YOLO
import cv2, sqlite3
from datetime import datetime

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

def save_log(count):
    conn = sqlite3.connect("traffic.db")
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO traffic_log(date, pedestrian_count) VALUES (?,?)",
                   (date, count))
    conn.commit()
    conn.close()
    print("Log Saved")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if model.names[cls] == "person":
                count += 1

    cv2.putText(frame,f"Pedestrians: {count}",
                (20,40), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.putText(frame,"Press 'S' to Save Log",
                (20,80), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2)

    cv2.imshow("Pedestrian Monitor", frame)

    key = cv2.waitKey(1)
    if key == ord('s'):
        save_log(count)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
