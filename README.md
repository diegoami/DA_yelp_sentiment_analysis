# SENTIMENT ANALYSIS BASED ON THE YELP DATASET

## BACKGROUND

In this project we build a regressor trying to predict the stars of a review from the text of the review itself.
It use the Reviews from the YELP Dataset.

## PREPARATORY WORK

### RETRIEVE THE DATASET

Retrieve the YELP Dataset here: https://www.yelp.com/dataset and extract the `reviews.json` file into a source directory.

### CONFIGURE DIRECTORIES 

Define the source (where data from yelp is located) and target directory (where to save results) in the `config.yaml` file.

### SET UP ENVIRONMENT

If you have conda, you can install an environment this way

Assuming Conda is installed

```
conda create -n yelp_review python=3.7
source activate yelp_review 
python -m pip install -r requirements.txt
```

## SCRIPTS EXECUTION

### CONVERT REVIEWS TO CSV

To make it easier to work with the dataset, we extract the relevant information about reviews into a CSV file, using the script

`python review_json_to_csv.py`

This will save a `reviews.csv` into the target directory

### TRAIN MODEL

In `config.yaml`, set up REVIEWS_USED to the amount of reviews you want to use for your model.
Then execute

`python full_pipeline.py`

It will train and save a model in the target directory

### USE MODEL

You can use the model, typing your reviews after the command prompt, executing

`python run_model.py`




