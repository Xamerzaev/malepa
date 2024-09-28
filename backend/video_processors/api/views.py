from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from video_processors.api.serializers import VideoLinkSerializer

import json
import cv2

import numpy as np
import labelbox

from video_processors.video_processing import (process_video_and_annotate,
                                               create_video_annotation_task)

API_KEY = "ВАШ_API_КЛЮЧ"
client = labelbox.Client(api_key=API_KEY)


class VideoLinkView(APIView):
    def post(self, request):
        serializer = VideoLinkSerializer(data=request.data)

        if serializer.is_valid():
            link = serializer.validated_data.get('link')
            links = serializer.validated_data.get('links')

            # Обработка одного видео
            if link:
                annotations = process_video_and_annotate(link)
                video_data = {
                    "external_id": link.split('/')[-1],  # Пример идентификатора
                    "video_url": link
                }
                project, video = create_video_annotation_task(video_data, annotations)
                return Response({"annotations": annotations}, status=status.HTTP_200_OK)

            # Обработка списка видео
            if links:
                all_annotations = {}
                for link in links:
                    annotations = process_video_and_annotate(link)
                    video_data = {
                        "external_id": link.split('/')[-1],
                        "video_url": link
                    }
                    project, video = create_video_annotation_task(video_data, annotations)
                    all_annotations[link] = annotations

                return Response({"annotations": all_annotations}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
