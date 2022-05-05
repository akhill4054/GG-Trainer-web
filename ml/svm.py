from operator import mod
from pickle import dump
import joblib
import numpy as np
from sklearn.svm import SVC

model = None

try:
    model = joblib.load('model.joblib')
except:
    # Classifier
    model = SVC()


def process_data(data):
    lines = []
    for l in data.split('\n'):
        if l != '':
            lines.append(l)
    for i, v in enumerate(lines):
        values = [float(c) for c in v.split(',')]
        assert(len(values) == 15)
        lines[i] = values
    return lines


def try_to_predict(data):
    values = process_data(data)
    return model.predict(values)


def reset():
    model = SVC()

    from .models import Gesture

    # Clear db
    Gesture.objects.all().delete()
    
    data = ''
    for i in range(15):
        data += '0'
        if i != 14:
            data += ','
        else:
            data += '\n'
    
    Gesture(data=data, mapped_text='NULL').save()
    Gesture(data=data, mapped_text='NULL1').save()

    retrain_model(Gesture.objects.all())


def retrain_model(gestures):
    x_rows = []
    y_col = []

    for gesture in gestures:
        mapping = gesture.mapped_text
        value_rows = process_data(gesture.data)

        for values in value_rows:
            x_rows.append(values)
            y_col.append(mapping)

    X_train = np.asarray(x_rows)
    Y_train = np.asarray(y_col)

    model.fit(X_train, Y_train)

    # Save the model
    joblib.dump(model, 'model.joblib')
