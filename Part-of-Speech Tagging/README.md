# Part-of-Speech Tagger

This repository contains the second assignment of CmpE 561 (Natural Language Processing, Boğaziçi University, Spring’16), which is about ‘Part of speech tagging using Hidden Markov Model’.

# Dataset

 turkish_metu_sabanci dataset is used, it contains different sets which can be used as training, test and validation sets.

# Before Starting

One needs to train the tagger by using a training file, which is "turkish_metu_sabanci_train.conll" as default.

`python train_hmm_tagger.py [--cpostag | --postag ] training_file_path`

Positional arguments :
```
training_file_path		: Path to training file. Default : ./training_file.conll
```

Optional arguments :
```
--cpostag : Constructs the model by using cpostag.

--postag : Constructs the model by using postag.
```

(There is no need to do this part in case of having a model file with name "hmm_model".)

# How to Use ?

Once the model is constructed, the one thing needs to be done is to run `hmm_tagger.py` script (python3 should be used.).

`python hmm_tagger.py test_file_path output_file_path`

There are two positional arguments :
```
test_file_path 		: Path to test file. Default : ./blind_file.conll

output_file_path	: Path to output file. Default : ./output.txt
```

ex.

`python hmm_tagger.py ./blind_file.conll ./output.txt`

# Evaluate tagger

After tagging given words, one who want to evaluate the accuracy of the tagger may use "evaluate_hmm_tagger.py" script.
It prints some statistics about the tagger.

`python evaluate_hmm_tagger.py output_file_path gold_file_path`

There are two positional arguments :
```
output_file_path 	: Path to output file. Default : ./output.txt

gold_file_path		: Path to gold file. Default : ./gold_file.conll
```

ex.

`python evaluate_hmm_tagger.py ./output.txt ./gold_file.conll`
