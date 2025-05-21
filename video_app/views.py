from collections import deque, Counter

import cv2
import numpy as np
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from keras.models import load_model
from keras.src.utils.image_utils import img_to_array

from model_train.utils import preprocess_input

CLASS_LABELS = {
    0: "OK",
    1: "Aggression Detected"
}
WINDOW_SIZE = 9
PROB_THRESHOLD = 0.975

model = load_model('video_app/violence_v2_v1.keras')


def video_feed(request):
    video_url = request.GET.get('url')

    if video_url is None:
        video_url = "/home/veldergard/PycharmProjects/ViolenceDjango/video_app/vk_call.mp4"
        # video_url = "/home/veldergard/PycharmProjects/ViolenceDjango/video_app/NV_363.mp4"


    return StreamingHttpResponse(
        generate_frames(video_url),
        content_type='multipart/x-mixed-replace; boundary=frame')


def generate_frames(stream_url):
    cap = cv2.VideoCapture(stream_url)
    # recent_preds = deque(maxlen=WINDOW_SIZE)
    # recent_labels = deque(maxlen=WINDOW_SIZE)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    recent_labels = deque(maxlen=frame_rate)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Подготовка кадра
        input_frame = cv2.resize(frame, (224, 224))
        array = img_to_array(input_frame)
        array = np.expand_dims(array, axis=0)
        array = preprocess_input(array)

        preds = model.predict(array)

        prob = float(preds[0][0])  # Т как preds — массив вида [[0.93]]
        pred_index = int(prob >= PROB_THRESHOLD)

        # recent_preds.append(pred_index)
        # final_pred = int(sum(recent_preds) > len(recent_preds) / 2)
        # final_label = CLASS_LABELS[final_pred]

        pred_label = CLASS_LABELS[pred_index]
        recent_labels.append(pred_label)
        label_text = f"{pred_label} ({prob:.2f})"
        print(label_text)

        most_common_label = Counter(recent_labels).most_common(1)[0][0]
        print(most_common_label)

        color = (0, 255, 0) if most_common_label == CLASS_LABELS[0] else (0, 0, 255)
        cv2.putText(frame, most_common_label, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Отображение кадра
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def video_input_view(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        return redirect('video_feed' + f'?url={video_url}')
    return render(request, 'video_input.html')
