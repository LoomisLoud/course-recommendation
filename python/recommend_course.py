from enrolment_matrix import load_enrolment_matrix, get_last_year_registrations
from keras import models
import numpy as np
import pandas as pd

COURSES = [
"Distributed information systems",
"Information theory and coding",
"Pattern classification and machine learning",
"Mobile networks",
"Statistical signal and data processing through applications",
"TCP/IP networking",
"Digital education & learning analytics"
]

USERNAME = "random user"

def predict(courses=COURSES):
    courses_matrix = load_enrolment_matrix(from_pickle=True)
    my_courses = pd.DataFrame(data=0, columns=courses_matrix.columns, index=[USERNAME])
    my_courses[courses] = 1
    taken_courses = my_courses.loc[USERNAME][my_courses.loc[USERNAME] == 1].index.tolist()

    my_binary_courses = my_courses.as_matrix()
    binary_courses_format = np.array([[1]], dtype=np.int32)

    model = models.load_model('../data/cdae_model.hd5')
    prediction = model.predict(x=[my_binary_courses, binary_courses_format])
    prediction = np.argsort(prediction)

    predicted_courses = [courses_matrix.columns[i] for i in prediction[0]]
    last_year_courses = list(get_last_year_registrations(from_pickle=True).index)
    predicted_courses = [c for c in predicted_courses if c in last_year_courses and c not in taken_courses]

    return predicted_courses[::-1][:10]
