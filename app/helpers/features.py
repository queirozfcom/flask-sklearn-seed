import numpy as np


def make_feature_vector(attribute_dict):
    feature_vector = np.array([
        attribute_dict["score_3"],
        attribute_dict["score_4"],
        attribute_dict["score_5"],
        attribute_dict["score_6"]
    ])

    # return a row vector
    return feature_vector.reshape(1, -1)
