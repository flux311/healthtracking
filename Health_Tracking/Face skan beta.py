import cv2
import mediapipe as mp
from fer.fer import FER
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import fer

# ======== ИНИЦИАЛИЗАЦИЯ MEDIAPIPE 2.0 ========
MODEL_PATH = 'face_landmarker.task' #веса для нейронки

base_options = python.BaseOptions(model_asset_path=MODEL_PATH) #создание базовых настроек для работы нейронки(закидываем в неё данные с весами)
options = vision.FaceLandmarkerOptions(base_options=base_options,output_face_blendshapes=False,output_facial_transformation_matrixes=False,num_faces=1) #здесь окончательно коректируем основные настройки нейронки

detector = vision.FaceLandmarker.create_from_options(options) #создаём собственно сам детектор лиц

# ======== ИНИЦИАЛИЗАЦИЯ FER ========
emotion_detector = FER() #создаём детектор эмоций(по изображению от детектора лица)

# ======== ЗАПУСК КАМЕРЫ ========
cap = cv2.VideoCapture(0) #запуск камеры, в скобках индекс устройства
last_emotion = "Ожидание..."
frame_counter = 0

while True:
    ret, frame = cap.read() #данные с камеры(подтверждение получен ли кадр или нет, сам кадр)
    if not ret:
        break

    frame_counter += 1

    # Конвертируем в RGB для MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Определяем лица через MediaPipe 2.0
    detection_result = detector.detect(mp_image)

    # Если лица найдены
    if detection_result.face_landmarks: #здесь мы получаем целый масив со слоаврями внутри, с данными обо всё кадре
        for face_landmarks in detection_result.face_landmarks: #здесь открываем этот список
            # ===== ЗЕЛЕНЫЕ ТОЧКИ УБРАНЫ =====
            #for landmark in face_landmarks:
                #x = int(landmark.x * frame.shape[1])
                #y = int(landmark.y * frame.shape[0])
                #cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Анализируем эмоции через FER каждый 5-й кадр
            if frame_counter % 5 == 0:
                try:
                    # FER анализирует весь кадр и находит лица
                    emotions = emotion_detector.detect_emotions(frame)
                    if emotions:
                        # Берем первую эмоцию (если лиц несколько)
                        emotion_dict = emotions[0]['emotions']
                        last_emotion = max(emotion_dict, key=emotion_dict.get) #здесь выберает самая вероятная эмоция(в списке они раставлены коэффициентом)
                except Exception as e:
                    # Если FER не смог определить эмоцию
                    pass

            # Выводим эмоцию на экран
            cv2.putText(frame, f"Эмоция: {last_emotion}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Лицо не найдено", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('AI Психолог - Сканер эмоций', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()