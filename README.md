# authorRecognizer

This repository contains the first assignment of CmpE 561 (Natural Language Processing, Boğaziçi University, Spring’16), which is about ‘Authorship Recognition using Naive Bayes’.

# Dataset

 69 Authors dataset, it contains 910 articles from 69 different Turkish authors. (http://www.kemik.yildiz.edu.tr/?id=28)

# Before Starting

One needs to extract the training and test sets from given dataset by using `dataset_extractor.py` script, which takes path to the dataset (default path : dataset/) and then produces a training and test set by randomly choosing 60% of the articles for training (the remaining ones for test) for each author. This process results in creating two directories(training_dataset and test_dataset) with chosen articles.

`python ./dataset_extractor.py /path/to/dataset/`

(There is no need to do this part in case of having training and test sets.)

# How to Use ?

Once the training and test sets are ready, the one thing needs to be done is to run `author_recognizer.py` script (Both python2 and python3 can be used.).

`python author_recognizer.py [-r| -ns] training_path test_path`

There are two optional and two positional arguments :

-r (result) 		: Prints the result of the recognizer. (If parent directories of the articles are named as authors' names, it gives rational results.)

-ns (nostatistics) 	: Does not print the statistics about recognition process.

training_path 		: Path to training dataset.

test_path		: Path to test dataset.

ex.

`python author_recognizer.py -r training_dataset test_dataset`

If path to training or test datasets are not given, ’training_dataset/’ and ‘test_dataset’ are used as default. On the other hand, if one wants to give the paths, it is essential to write them in the given order.