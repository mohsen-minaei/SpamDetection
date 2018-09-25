# SpamDetection
This project detects spam emails using Naive Bayes and SVM.

The data source of this project is from CSDMC2010. 
The training folder has 3000 files and the testing folder has 1326 files.

To preprocess the emails run the ExtractContent.py file. This will extract the subject and body of the email. You can add more preprocessing steps in this file. As input it takes the path of the training/testing folder and the destination to export the preprocessed files (e.g., TRAINING_PREPROCESSING and TESTING_PREPROCESSING folder). 

This project has two methods of classification. One using the Naive Bayes approach, another the SVM.
To run the classification programs run the "python naive_bayes.py" and "svm.py" command.
