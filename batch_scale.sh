svm-scale -s libsvm_training_fold_1.range libsvm_training_fold_1 > scaled_libsvm_training_fold_1
svm-scale -s libsvm_training_fold_2.range libsvm_training_fold_2 > scaled_libsvm_training_fold_2
svm-scale -s libsvm_training_fold_3.range libsvm_training_fold_3 > scaled_libsvm_training_fold_3
svm-scale -s libsvm_training_fold_4.range libsvm_training_fold_4 > scaled_libsvm_training_fold_4
svm-scale -s libsvm_training_fold_5.range libsvm_training_fold_5 > scaled_libsvm_training_fold_5

svm-scale -r libsvm_training_fold_1.range libsvm_testing_fold_1 > scaled_libsvm_testing_fold_1
svm-scale -r libsvm_training_fold_2.range libsvm_testing_fold_2 > scaled_libsvm_testing_fold_2
svm-scale -r libsvm_training_fold_3.range libsvm_testing_fold_3 > scaled_libsvm_testing_fold_3
svm-scale -r libsvm_training_fold_4.range libsvm_testing_fold_4 > scaled_libsvm_testing_fold_4
svm-scale -r libsvm_training_fold_5.range libsvm_testing_fold_5 > scaled_libsvm_testing_fold_5