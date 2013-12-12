

fp_test_fold1 = open('scaled_libsvm_testing_fold_1', 'r')
fp_test_fold2 = open('scaled_libsvm_testing_fold_2', 'r')
fp_test_fold3 = open('scaled_libsvm_testing_fold_3', 'r')
fp_test_fold4 = open('scaled_libsvm_testing_fold_4', 'r')
fp_test_fold5 = open('scaled_libsvm_testing_fold_5', 'r')

fp_output_fold1 = open('scaled_libsvm_testing_fold_1.output', 'r')
fp_output_fold2 = open('scaled_libsvm_testing_fold_2.output', 'r')
fp_output_fold3 = open('scaled_libsvm_testing_fold_3.output', 'r')
fp_output_fold4 = open('scaled_libsvm_testing_fold_4.output', 'r')
fp_output_fold5 = open('scaled_libsvm_testing_fold_5.output', 'r')


test_fps = [fp_test_fold1,fp_test_fold2,fp_test_fold3,fp_test_fold4,fp_test_fold5]
output_fps = [fp_output_fold1,fp_output_fold2,fp_output_fold3,fp_output_fold4,fp_output_fold5]

for i in range(5):
    fp_test = test_fps[i]
    fp_output = output_fps[i]

    real_labels = []
    for line in fp_test:
        real_labels.append(int(line.split()[0]))

    predict_labels = []
    for line in fp_output:
        predict_labels.append(int(line))

    
    for predict_label, real_label in zip(predict_labels, real_labels):
        print predict_label, ' ', real_label

    pos = 0.0
    retr = 0.0
    tp = 0.0
    for predict_label, real_label in zip(predict_labels, real_labels):
        if predict_label == 1 and real_label == 1:
            tp += 1.0
            pos += 1.0
            retr += 1.0
        elif predict_label == 1 and real_label == 0:
            retr += 1.0
        elif predict_label == 0 and real_label == 1:
            pos += 1.0

    print 'precision=', tp/retr
    print 'recall=', tp/pos
    print '=======================================================\n\n'




