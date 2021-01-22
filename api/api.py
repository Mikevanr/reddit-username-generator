from flask import Flask
from flask_cors import CORS, cross_origin
from time import sleep

import tensorflow as tf
import numpy as np

app = Flask(__name__)
cors = CORS(app)


@app.route('/time')
@cross_origin()
def get_current_time():
    sleep(3)
    return {'time': time()}


@app.route('/generate')
@cross_origin()
def generate_usernames(num_generate=10, temperature=0.5, start_string='\n'):
    """ Given the model, the number of usernames to generate, and a temperature, create usernames """
    model = tf.keras.models.load_model('../assets/lstm-400k-100e-1.84l')

    char2idx = {"\n": 0, "-": 1, "0": 2, "1": 3, "2": 4, "3": 5, "4": 6, "5": 7, "6": 8, "7": 9, "8": 10, "9": 11, "A": 12, "B": 13, "C": 14, "D": 15, "E": 16, "F": 17, "G": 18, "H": 19, "I": 20, "J": 21, "K": 22, "L": 23, "M": 24, "N": 25, "O": 26, "P": 27, "Q": 28, "R": 29, "S": 30, "T": 31, "U": 32,
                "V": 33, "W": 34, "X": 35, "Y": 36, "Z": 37, "_": 38, "a": 39, "b": 40, "c": 41, "d": 42, "e": 43, "f": 44, "g": 45, "h": 46, "i": 47, "j": 48, "k": 49, "l": 50, "m": 51, "n": 52, "o": 53, "p": 54, "q": 55, "r": 56, "s": 57, "t": 58, "u": 59, "v": 60, "w": 61, "x": 62, "y": 63, "z": 64}
    idx2char = ['\n', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []
    curr_str = ''
    # Here batch size == 1
    model.reset_states()
    while num_generate > 0:
        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a categorical distribution to predict the character returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(
            predictions, num_samples=1)[-1, 0].numpy()

        # Pass the predicted character as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        if idx2char[predicted_id] == '\n':  # finished creating a new username
            num_generate -= 1
            text_generated.append(curr_str)
            curr_str = ''
        else:
            curr_str += idx2char[predicted_id]

    return text_generated
