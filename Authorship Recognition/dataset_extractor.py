#!/usr/bin/env python
# -*- coding: UTF-8-*-
import sys, os
from shutil import copyfile
from random import randrange

# Copies the given article into the given path.
def copy_article(src_path, destination_base_path, author_dir, article):
	article_path = src_path + author_dir + "/" + article
	destination_path = destination_base_path + author_dir + "/" + article

	copyfile(article_path, destination_path)

# Creates training and test dataset by selecting articles from the given dataset randomly
def dataset_extractor(src_path, training_dest_path, test_dest_path):

	# Iterates over all directories in the given path of the dataset.
	for author_dir in os.listdir(src_path):

		# If there is a file, pass it.
		if not os.path.isdir(src_path + author_dir):
			continue

		article_list = os.listdir(src_path + author_dir) 		# Stores all article names of an author into a list.
		article_number = len(article_list)
		training_article_number = int(article_number * 0.6)		# Computes how many of the articles will be selected as training data.

		if not os.path.exists(training_dest_path + author_dir):
			os.makedirs(training_dest_path + author_dir) 		# Makes a directory for the author in the training directory.

		if not os.path.exists(test_dest_path + author_dir):
			os.makedirs(test_dest_path + author_dir) 			# Makes a directory for the author in the test directory.

		training_article_count = 0
		randrange_limit = article_number 
		for training_article_count in range(0,training_article_number):

			random_selected_index = randrange(0,randrange_limit)			# Generates a random number in order to select a random index.
			randrange_limit -= 1											# Decreases the limit of the range of random numbers
																			# Since with this iteration an element of the list will be deleted.
			random_selected_article = article_list[random_selected_index]	# Gets randomly selected article name.
			del article_list[random_selected_index]							# Removes the selected article name from the list.

			copy_article(src_path, training_dest_path, author_dir, random_selected_article)	# Copies the selected article into training directory.

		# Copies the remaining articles into test directory.
		for article in article_list:
			copy_article(src_path, test_dest_path, author_dir, article)


# Default paths.
src_path = 'dataset/'
training_dest_path = 'training_dataset/'
test_dest_path = 'test_dataset/'

if __name__ == "__main__":

	# If the path of the dataset is given as a parameter.
	if len(sys.argv) > 1:
		src_path = os.path.normpath(sys.argv[1])
		base_dest_path = os.path.dirname(src_path)
		base_dest_path += "/" if base_dest_path is not "" else ""

		training_dest_path = base_dest_path + 'training_dataset/'
		test_dest_path = base_dest_path + 'test_dataset/'
		src_path += "/"

	dataset_extractor(src_path, training_dest_path, test_dest_path)