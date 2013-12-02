svm-train $1 $2 $3 $4 $5 $6 scaled_libsvm_training_fold_1
svm-train $1 $2 $3 $4 $5 $6 scaled_libsvm_training_fold_2
svm-train $1 $2 $3 $4 $5 $6 scaled_libsvm_training_fold_3
svm-train $1 $2 $3 $4 $5 $6 scaled_libsvm_training_fold_4
svm-train $1 $2 $3 $4 $5 $6 scaled_libsvm_training_fold_5

svm-predict scaled_libsvm_testing_fold_1 scaled_libsvm_training_fold_1.model scaled_libsvm_testing_fold_1.output | tee scaled_libsvm_testing_fold_1.accuracy
svm-predict scaled_libsvm_testing_fold_2 scaled_libsvm_training_fold_2.model scaled_libsvm_testing_fold_2.output | tee scaled_libsvm_testing_fold_2.accuracy
svm-predict scaled_libsvm_testing_fold_3 scaled_libsvm_training_fold_3.model scaled_libsvm_testing_fold_3.output | tee scaled_libsvm_testing_fold_3.accuracy
svm-predict scaled_libsvm_testing_fold_4 scaled_libsvm_training_fold_4.model scaled_libsvm_testing_fold_4.output | tee scaled_libsvm_testing_fold_4.accuracy
svm-predict scaled_libsvm_testing_fold_5 scaled_libsvm_training_fold_5.model scaled_libsvm_testing_fold_5.output | tee scaled_libsvm_testing_fold_5.accuracy