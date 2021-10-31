#!/usr/bin/env python3

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import numpy
import glob
import re
import string
import random
import collections
import argparse
import tensorflow as tf
import tensorflow.keras as keras


def decode(characters, y):
    y = numpy.argmax(numpy.array(y), axis=2)[:, 0]
    return ''.join([characters[x] for x in y])


def eliminate_space_or_duplicate(decoded_str):
    if ' ' in decoded_str:
        decoded_str = decoded_str.replace(" ", "")
    else:
        decoded_str = decoded_str[:-1]
    return decoded_str


def get_models_list(model_path):
    models = []
    for i in glob.glob(f'{model_path}/*.h5'):
        models.append(re.split(r'/|\\', i)[-1].split('.')[0])
    return models


def get_models(model_path):
    keras_models = {}
    models = get_models_list(model_path)
    for model_name in models:
        json_file = open(f'{model_path}/{model_name}.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = keras.models.model_from_json(loaded_model_json)
        print(f'{model_path}/{model_name}.h5')
        model.load_weights(f'{model_path}/{model_name}.h5')
        model.compile(loss='categorical_crossentropy',
                      optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                      metrics=['accuracy'])
        keras_models[model_name] = model
    return keras_models


def get_model(model_name, model_path):
    json_file = open(f'{model_path}/{model_name}.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model_path = f'{model_path}/{model_name}.h5'
    model = keras.models.model_from_json(loaded_model_json)
    print(model_path)
    model.load_weights(model_path)
    model.compile(loss='categorical_crossentropy',
                  optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                  metrics=['accuracy'])
    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', help='Path to the CNN models to use for classification', type=str)
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    parser.add_argument('--label_symbol', help='File with the symbol for the label1 to use in captchas', type=str)
    parser.add_argument('--userid', help='userid of the student', type=str)
    args = parser.parse_args()

    if args.model_path is None:
        print("Please specify the path to CNN model")

    if args.label_symbol is None:
        print("Please specify the captcha symbol file for label1")
        exit(1)

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    if args.userid is None:
        print("Please specify the userid")
        print("Please specify the userid")
        exit(1)

    label_symbol_file = open(args.label_symbol)
    label_symbol = open(args.label_symbol).readline().strip()
    print(f'label_symbol: {label_symbol}')
    label_symbol_file.close()

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Classifying captcha with symbol set {" + captcha_symbols + "}")

    with tf.device('/cpu:0'):
        with open(args.output, 'w') as output_file:
            predicted_values = {}
            # get_keras_model = get_models(args.model_path)
            for dir in range(1, 7):
                model_name = f'label{dir}'
                model = get_model(model_name, args.model_path)
                image_dir = f'{args.captcha_dir}/{dir}'
                print(model_name, image_dir)
                for x in sorted(os.listdir(image_dir)):
                    print(f'for directory {image_dir}')
                    # load image and preprocess it
                    raw_data = cv2.imread(os.path.join(image_dir, x))
                    rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
                    image = numpy.array(rgb_data) / 255.0
                    (c, h, w) = image.shape
                    image = image.reshape([-1, c, h, w])
                    prediction = model.predict(image)
                    if dir != 1:
                        decoded_captcha = decode(captcha_symbols, prediction)
                    else:
                        print(dir)
                        decoded_captcha = eliminate_space_or_duplicate(decode(label_symbol, prediction))
                    print(f'{x} , {decoded_captcha}')
                    predicted_values[x] = decoded_captcha
                    # output_file.write(x + "," + decode(captcha_symbols, prediction) + "\n")
                    print('Classified ' + x + str(len(decoded_captcha)))
                del model
            print(f'\n\n\n\n predicted values \n\n\n\n {type(predicted_values)} {len(predicted_values)}')

            for key, item in sorted(predicted_values.items()):
                output_file.write(key + "," + item + "\n")


if __name__ == '__main__':
    main()
