# SENTIMENT ANALYSIS BASED ON THE YELP DATASET

## BACKGROUND

In this project we build a regressor trying to predict the stars of a review from the text of the review itself.
It use the Reviews from the YELP Dataset.

## PREPARATORY WORK

### RETRIEVE THE DATASET

Retrieve the YELP Dataset here: https://www.yelp.com/dataset and extract the `reviews.json` file into a directory (we will call it <SOURCE-DIR>).

### CONFIGURE DIRECTORIES 

Define the directories where the YELP dataset is located in the `config.yaml` file. 

Alternative, set up symbolic links to your source and target directories from the program's home directory.

```
mkdir data
ln -s <SOURCE-DIR> data/source
ln -s <TARGET-DIR> data/target
```



### SET UP ENVIRONMENT

If you have Conda 

```
conda create -n yelp_review python=3.7
source activate yelp_review 
python -m pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
```

Alternatively, with Docker

```
docker build --tag yelp_sent . # BUILD
docker run -it -v <SOURCE-DIR>:/app/data/source/ -v <TARGET-DIR>:/app/data/target/ -v $(pwd)/config.yaml:/app/config.yaml --name yelp_sent yelp_sent:latest /bin/bash # RUN
docker run -it -v $(pwd)/data/source:/app/data/source/ -v $(pwd)/data/target:/app/data/target/ -v $(pwd)/config.yaml:/app/config.yaml --name yelp_sent yelp_sent:latest /bin/bash # RUN if you set symbolic links

docker stop yelp_sent # to STOP
docker container rm yelp_sent # to Remove the container

```



and then execute the commands described below, from the docker container.

## SCRIPTS EXECUTION

### CONVERT REVIEWS TO CSV

To make it easier to work with the dataset, we extract the relevant information about reviews into a CSV file, using the script

`python review_json_to_csv.py`

This will save a `reviews.csv` into the target directory. 
It is also available here: https://s3.eu-central-1.amazonaws.com/diegoamicabile-yelp/review.csv.tgz

### TRAIN MODEL

In `config.yaml`, set up REVIEWS_USED to the amount of reviews you want to use for your model.
Then execute

`python full_pipeline.py`

It will train and save a model in the target directory.

### USE MODEL

Execute:

`python run_model.py`

You can then use the model, typing your reviews after the command prompt, 



## MODEL DETAILS

### PREPROCESSING

Some effort has been done on preprocessing, but more experiments might give better results. 

- Standard NLTK tokenization is used
- Punctuation tokens got removed, 
- Tokens having no alphabetic characters are removed
- CountVectorization use 1 and 2 grams
- CountVectorization removes tokens that appear in more than 30% of the reviews corpus (corpus specific stop words)

### PIPELINE

The Pipeline is made of these components. As not much effort has been invested in this phase, improvements are certainly possible.

- CountVectorizer
- TfidfTransformer
- SGDRegressor

### RESULT

I trained a model using 1m reviews, using 80% of the samples for training and 20% for test. It is available at https://s3.eu-central-1.amazonaws.com/diegoamicabile-yelp/review.pipeline-1000000

The target variable is the amount of stars given during the review (from 1 to 5). The model predicts this value (from 1 to 5) and is therefore a regression.

For this model, the MSE is the following

- Training Set: 1.01
- Test Set: 1.01
