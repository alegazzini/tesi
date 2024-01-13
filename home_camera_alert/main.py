import os
import time
import cv2
from deepface import DeepFace
import asyncio

from VideoCaptureThread import VideoCaptureThread
from Face import Face
import utils
from telegram import Bot


TOKEN_BOT = os.environ.get("TOKEN_BOT", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

cap = VideoCaptureThread(camera='rtsp://admin:GWOSPK@192.168.1.146:554/h264')

# cap = cv2.VideoCapture('rtsp://admin:GWOSPK@192.168.1.50:554/h264')
process_this_frame: bool = True
detector: str = "mtcnn"
known_face_db: str = './datasets/faces'
model_name: str = 'VGG-Face'
distance_metric: str = 'euclidean_l2'
threshold: float = 0.8
count_unknown_frame: int = 0

bot: Bot = Bot(token=TOKEN_BOT)


async def start_monitoring():
    while True:
        frame = cap.read()
        if frame is None:
            time.sleep(1)
            continue

        x_scale = y_scale = 1

        try:
            results = DeepFace.find(img_path=frame, db_path=known_face_db, model_name=model_name,
                                    detector_backend='mtcnn',
                                    enforce_detection=False, distance_metric=distance_metric)
            if len(results[0]):

                # Prendo il primo perché è quello con bounding box maggiore e quindi in teoria il più vicino alla telecamera
                result = results[0]
                # Chi ha distanza minore è quello con più alta probabilità
                res = result.sort_values(by=[f"{model_name}_{distance_metric}"])
                best_match = res.iloc[0]
                # Controlla se la distanza è sotto la soglia
                if best_match[f"{model_name}_{distance_metric}"] <= threshold:
                    face_name = "Alessandro Gazzini"
                    color = (0, 255, 0)
                    count_unknown_frame = 0
                else:
                    # Nessun match affidabile
                    face_name = "Unknown"
                    color = (0, 0, 255)
                    count_unknown_frame += 1

                x = int(best_match['source_x'])
                y = int(best_match['source_y'])
                w = int(best_match['source_w'])
                h = int(best_match['source_h'])

                face = Face(x_img=x / x_scale, y_img=y / y_scale, w_img=w / x_scale, h_img=h / y_scale)

                print(face_name)
                # Drawing: square around the face
                cv2.rectangle(frame, face.first_point(), face.fourth_point(), color, 3)

                # Drawing: text box with name
                utils.drawing_rect_name(face_name=face_name, face=face, frame=frame, color=color)

                if face_name == "Unknown" and count_unknown_frame == 2:
                    filename = f"./tmp/prova_{count_unknown_frame}.jpg"
                    cv2.imwrite(filename, frame)

                    try:
                        message = await bot.sendMessage(chat_id=CHAT_ID, text="rilevata intrusione!")
                        media = await bot.sendPhoto(chat_id=CHAT_ID, photo=filename)
                    except:
                        print("No telegram")
                if face_name == "Alessandro Gazzini":
                    filename = f"./tmp/ok.jpg"
                    cv2.imwrite(filename, frame)

            cv2.imshow("capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # wait for 1 millisecond
                break

        except Exception as e:
            print(f"Error: {e}")
            count_unknown_frame = 0



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(start_monitoring())
    loop.run_forever()
    loop.close()
