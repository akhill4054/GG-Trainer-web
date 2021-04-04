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

# def train_model(gesture):
#     values = process_data(gesture.data)
#     X_train = np.asarray(values)
#     Y_train = np.asarray([gesture.mapped_test])

#     model.fit(X_train, Y_train)

#     # Save the model?
#     joblib.dump(model, 'model2.joblib')
def reset():
    model = SVC()
    dump(model, 'model.joblib')

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
