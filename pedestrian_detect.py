from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

    person_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "person":
                person_count += 1
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.putText(frame,f"Pedestrians: {person_count}",
                (20,40), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("Pedestrian Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
