import numpy as np


def make_feature_vector(attribute_dict):
    feature_vector = np.array([
        attribute_dict["x_1"],
        attribute_dict["x_2"],
        attribute_dict["x_3"],
        attribute_dict["x_4"]
    ])

    # return a row vector
    return feature_vector.reshape(1, -1)
