# cs7ns1_project2
Captcha Solving Using TensorFlow

## Overview 
We generated dataset and trained model for different captcha length, ranging from 1 to 6. We have created 6 models for each captcha length (1-6) and classified our dataset using this 6 models.

## Generate training and validating datasets for each captcha length (1-6)

### Training dataset
```
python3 ./scripts/generate.py --width 128 --height 64 --length <CAPTCHA_LENGTH> --symbols symbols.txt --count 64000 --output-dir training_data
```
### Validating dataset
```
python3 ./scripts/generate.py --width 128 --height 64 --length <CAPTCHA_LENGTH> --symbols symbols.txt --count 6400 --output-dir validating_data
```


## Training the model
#### Train model for each captcha length (1-6)
```
python3 ./scripts/train_org.py --width 128 --height 64 --length <CAPTCHA_LENGTH> --symbols symbols.txt --batch-size 32 --epochs 5 --output-model label6 --train-dataset training_data --validate-dataset validating_data
```

## Classifying the dataset
### Make sure to place all the model on parent directory. Classify the images for each image dirs with appropriate model based on captcha length.
### rename the image directory of the user to images/
```
python3 ./scripts/classify.py --model-name label6 --captcha-dir images/6 --output classified_6.csv --symbols symbols.txt

Here 6 denotes the captcha_length.

```

## Execute python script to club all generated csv files
```
python3 sort.py
```
