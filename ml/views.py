# Create your views here.
from django.http.response import HttpResponse, JsonResponse
from numpy import where
from rest_framework import status
from .serializers import GestureSerializer, TranslateRequestSerializer, ResetSerializer, RemoveSyncedGestureSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Gesture
from . import svm


def home(request):
    return HttpResponse("<h1>Hello World!</h1>")


@api_view(['POST'])
def translate(request):
    serializer = TranslateRequestSerializer(data=request.data)
    if serializer.is_valid():
        # Do translation
        try:
            translations = svm.try_to_predict(serializer.data['data'])

            f_map = {}
            for r in translations:
                if r in f_map: f_map[r] += 1
                else: f_map[r] = 1

            max_f = 0; translation = ''
            for r, f in f_map.items():
                if f > max_f:
                    max_f = f; translation = r

            return Response(translation, status=status.HTTP_200_OK)
        except:
            return Response('NULL', status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def gestures(request):
    gestures = Gesture.objects.exclude(mapped_text='NULL').all()
    serializer = GestureSerializer(gestures, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def sync(request):
    serializer = GestureSerializer(data=request.data)
    if serializer.is_valid():
        gesture_results = Gesture.objects.filter(
            mapped_text=serializer.data['mapped_text'])

        gesture = Gesture(
            data=serializer.data['data'],
            mapped_text=serializer.data['mapped_text'],
            rd=serializer.data['rd']
        )

        msg = None

        if len(gesture_results) > 0:
            # Already exists
            gesture = gesture_results[0]
            gesture.data = serializer.data['data']
            gesture.save()
            # Retrain model
            msg = 'Training successfull! [Old gesture replaced]'
        else:
            # Save gesture
            gesture.save()
            # Train model
            msg = 'Training successfull!'

        if not retrain_model():
            return Response('Couldn\'t train!', status=201)

        return Response(msg, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def remove_synced_gesture(request):
    serializer = RemoveSyncedGestureSerializer(data=request.data)
    if serializer.is_valid():
        gestures = Gesture.objects.filter(
            mapped_text=serializer.data['mapped_text'])

        if len(gestures) > 0:
            gestures.delete()
            retrain_model()
            return Response('Gesture removed successfully', status=status.HTTP_200_OK)
        else:
            return Response('Gesture not found', status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset(request):
    serializer = ResetSerializer(data=request.data)

    if serializer.is_valid():
        if serializer.data['pass_key'] == 'asdf1234':
            # Reset saved model
            svm.reset()

            return Response('Reset successful!', status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def retrain_model():
    gestures = Gesture.objects.all()
    # Train model
    if len(gestures) > 0:
        if len(gestures) == 1 and gestures[0].mapped_text != 'NULL':
            # Insert dummy class
            data = ''
            for i in range(15):
                data += '0'
                if i != 14:
                    data += ','
                else:
                    data += '\n'
            Gesture(data=data, mapped_text='NULL').save()
            gestures = Gesture.objects.all()

        try:
            svm.retrain_model(gestures)
            return True
        except:
            # Reset the model
            svm.reset()
    return False
