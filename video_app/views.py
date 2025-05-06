import cv2
import numpy as np
from django.http import StreamingHttpResponse
from django.shortcuts import render
from keras.api.models import load_model

CLASS_LABELS = {
    0: "OK",
    1: "Агрессия обнаружена"
}

model = load_model('path/to/your_model.keras')


def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


def video_page(request):
    return render(request, 'video_stream.html')


def generate_frames(stream_url):
    cap = cv2.VideoCapture(stream_url)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Подготовка кадра
        input_frame = cv2.resize(frame, (224, 224))
        array = img_to_array(input_frame)
        array = np.expand_dims(array, axis=0)
        array = preprocess_input(array)

        # Предсказание
        preds = model.predict(array)
        # Можно декодировать результат, но здесь — просто для демонстрации

        # Отображение кадра
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
