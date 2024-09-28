import cv2
import numpy as np
import labelbox

import json

# Настройка Labelbox API
API_KEY = "ВАШ_API_КЛЮЧ"  # Вставьте ваш API ключ
client = labelbox.Client(api_key=API_KEY)

# Путь к файлам YOLO
YOLO_CFG = "yolov3.cfg"
YOLO_WEIGHTS = "yolov3.weights"
COCO_NAMES = "coco.names"

# Загрузка классов COCO
with open(COCO_NAMES, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Загрузка модели YOLO
net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Функция для обработки видео и автоматической разметки
def process_video_and_annotate(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_annotations = []

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        height, width, channels = frame.shape

        # Подготовка изображения для YOLO
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        boxes = []
        confidences = []
        class_ids = []

        # Анализ результата детекции
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Разметка для кадра
        frame_annotations = {
            "frame": frame_idx,
            "objects": []
        }

        for i in range(len(boxes)):
            box = boxes[i]
            label = str(classes[class_ids[i]])
            frame_annotations["objects"].append({
                "class": label,
                "confidence": confidences[i],
                "bounding_box": {
                    "x": box[0],
                    "y": box[1],
                    "width": box[2],
                    "height": box[3]
                }
            })

        video_annotations.append(frame_annotations)
        frame_idx += 1

    cap.release()
    return video_annotations


# Функция для создания задания на разметку в Labelbox
def create_video_annotation_task(video_data, annotations):
    # Создание датасета
    dataset = client.create_dataset(name="My Video Dataset")

    # Загрузка видео в датасет
    video = dataset.create_data_row(
        row_data=video_data["video_url"],
        external_id=video_data["external_id"]
    )

    print(f"Видео загружено с ID: {video.uid}")

    # Создание проекта для разметки видео
    project = client.create_project(name="My Video Annotation Project", media_type="VIDEO")

    # Привязка датасета к проекту
    project.datasets.connect(dataset)

    # Назначение задания (например, разметка bounding boxes)
    ontology = {
        "tools": [
            {
                "tool": "bbox",
                "name": "Bounding Box",
                "color": "#FF0000"
            }
        ]
    }

    # Создание ontology для разметки
    project.setup_ontology(ontology)

    # Пример: Выгрузка аннотаций в JSON формате в Labelbox (условный шаг)
    # TODO: Отправка аннотаций в Labelbox через API
    print(f"Проект для разметки видео создан: {project.name}")
    return project, video


# Основная функция
def main():
    # Пример входных данных о видео
    video_input_json = {
        "external_id": "example_video.mp4",
        "video_url": "path_to_your_video.mp4"
    }

    # Шаг 1: Разметка видео
    annotations = process_video_and_annotate(video_input_json["video_url"])

    # Шаг 2: Создание задания разметки в Labelbox
    project, video = create_video_annotation_task(video_input_json, annotations)

    # Шаг 3: Сохранение аннотаций в JSON файл
    output_file = "video_annotations.json"
    with open(output_file, 'w') as f:
        json.dump(annotations, f, indent=4)

    print(f"Аннотации видео сохранены в файл {output_file}")


# Запуск программы
if __name__ == "__main__":
    main()
