import csv
import datetime
import h5py
import numpy as np
import os
import pandas as pd
import sklearn.metrics
import sys
import time

import localmodule


# Read command-line arguments.
args = sys.argv[1:]
aug_kind_str = args[0]


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
folds = localmodule.fold_units()
models_dir = localmodule.get_models_dir()
units = localmodule.get_units()
model_name = "icassp-convnet"
if not aug_kind_str == "none":
    model_name = "_".join([model_name, "aug-" + aug_kind_str])
model_dir = os.path.join(models_dir, model_name)


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Evaluating Salamon's ICASSP 2017 convnet for binary classification in " +
    dataset_name + " clips. ")
print("")
print('h5py version: {:s}'.format(h5py.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('pandas version: {:s}'.format(pd.__version__))
print('scikit-learn version: {:s}'.format(sklearn.__version__))
print("")


# Loop over recording units.
for test_unit_str in units:

    # Define directory for test unit.
    unit_dir = os.path.join(model_dir, test_unit_str)

    # Create CSV file for metrics.
    metrics_name = "_".join([
        dataset_name,
        model_name,
        test_unit_str,
        "clip-metrics"
    ])
    metrics_path = os.path.join(unit_dir, metrics_name + ".csv")
    csv_file = open(metrics_path, 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')

    # Write CSV header.
    csv_header = [
    "Dataset",
    "Augmentation kind",
    "Test unit",
    "Trial",
    "Ad hoc threshold",
    "Ad hoc validation TP",
    "Ad hoc validation FP",
    "Ad hoc validation TN",
    "Ad hoc validation FN",
    "Ad hoc validation accuracy (%)",
    "Ad hoc test TP",
    "Ad hoc test FP",
    "Ad hoc test TN",
    "Ad hoc test FN",
    "Ad hoc test accuracy (%)",
    "Cross-validated threshold",
    "Cross-validated validation TP",
    "Cross-validated validation FP",
    "Cross-validated validation TN",
    "Cross-validated validation FN",
    "Cross-validated validation accuracy (%)",
    "Cross-validated test TP",
    "Cross-validated test FP",
    "Cross-validated test TN",
    "Cross-validated test FN",
    "Oracle threshold",
    "Test oracle TP",
    "Test oracle FP",
    "Test oracle TN",
    "Test oracle FN",
    "Test oracle accuracy (%)",
    "Validation AUC",
    "Test AUC"]
    csv_writer.writerow(csv_header)

    # Loop over trials.
    for trial_id in range(10):
        # Define directory for trial.
        trial_str = "trial-" + str(trial_id)
        trial_dir = os.path.join(unit_dir, trial_str)

        # Fold units.
        fold = [f for f in folds if test_unit_str in f[0]][0]
        validation_units = fold[2]

        # Load prediction for validation set as Pandas DataFrame.
        val_df_list = []
        for val_unit_str in validation_units:
            val_pred_name = "_".join([
                dataset_name,
                model_name,
                "test-" + test_unit_str,
                trial_str,
                "predict-" + val_unit_str,
                "clip-predictions.csv"])
            val_pred_path = os.path.join(trial_dir, val_pred_name)
            val_df = pd.read_csv(val_pred_path)
            val_df_list.append(val_df)
        val_df = pd.concat(val_df_list, ignore_index=True)
        val_y_true = list(val_df["Ground truth"])
        val_y_score = list(val_df["Predicted probability"])

        # Get ROC curve of validation set.
        val_fprs, val_tprs, val_thresholds =\
            sklearn.metrics.roc_curve(val_y_true, val_y_score)

        # Compute accuracies.
        #     ACC = (TN + TP) / (NEG + POS)
        # The dataset is balanced (NEG = POS) so
        #     ACC = 0.5 * (TN/NEG + TP/POS)
        # We have NEG = FP + TN so
        #     ACC = 0.5 * ((NEG-FP)/NEG + TP/POS)
        # We have FPR = FP/NEG and TPR = TP/POS so
        #     ACC = 0.5 * (1.0 - FPR + TPR)
        val_accuracies = 0.5 * (1.0 - val_fprs + val_tprs)

        # Find threshold that maximizes validation accuracy.
        cv_best_threshold_id = np.argmax(val_accuracies)
        cv_threshold = val_thresholds[cv_best_threshold_id]

        # Compute confusion matrix on validation set with optimal threshold.
        val_cv_y_pred = np.greater(val_y_score, cv_threshold)
        val_cv_cm = sklearn.metrics.confusion_matrix(
            val_y_true, val_cv_y_pred)
        val_cv_tp = val_cv_cm[0][0]
        val_cv_fp = val_cv_cm[0][1]
        val_cv_fn = val_cv_cm[1][0]
        val_cv_tn = val_cv_cm[1][1]

        # Compute validation accuracy with optimal threshold.
        val_tnr = 1.0 - val_fprs[cv_best_threshold_id]
        val_tpr = val_tprs[cv_best_threshold_id]
        val_cv_acc = val_accuracies[cv_best_threshold_id]

        # Compute confusion matrix on validation set with ad hoc threshold.
        val_adhoc_y_pred = np.greater(val_y_score, 0.5)
        val_adhoc_cm = sklearn.metrics.confusion_matrix(
            val_y_true, val_adhoc_y_pred)
        val_adhoc_tp = val_adhoc_cm[0][0]
        val_adhoc_fp = val_adhoc_cm[0][1]
        val_adhoc_fn = val_adhoc_cm[1][0]
        val_adhoc_tn = val_adhoc_cm[1][1]

        # Compute validation acuracy with ad hoc threshold.
        val_adhoc_acc =\
            (val_adhoc_tn+val_adhoc_tp) /\
            (val_adhoc_tp+val_adhoc_fp+val_adhoc_fn+val_adhoc_tp)

        # Compute area under ROC curve on validation set.
        val_auc = sklearn.metrics.roc_auc_score(
            val_y_true, val_y_score)

        # Load predictions for test set as Pandas Dataframe.
        test_pred_name = "_".join([
            dataset_name,
            model_name,
            "test-" + test_unit_str,
            trial_str,
            "predict-" + test_unit_str,
            "clip-predictions.csv"])
        test_pred_path = os.path.join(trial_dir, test_pred_name)
        test_df = pd.read_csv(test_pred_path)
        test_y_true = list(test_df["Ground truth"])
        test_y_score = list(test_df["Predicted probability"])

        # Compute confusion matrix on test set with cross-validated threshold.
        test_cv_y_pred = np.greater(test_y_score, cv_threshold)
        test_cv_cm = sklearn.metrics.confusion_matrix(
            test_y_true, test_cv_y_pred)
        test_cv_tp = test_cv_cm[0][0]
        test_cv_fp = test_cv_cm[0][1]
        test_cv_fn = test_cv_cm[1][0]
        test_cv_tn = test_cv_cm[1][1]

        # Compute test accuracy with cross-validated threshold.
        test_cv_acc =\
            (test_cv_tn+test_cv_tp) /\
            (test_cv_tp+test_cv_fp+test_cv_fn+test_cv_tp)

        # Compute confusion matrix on test set with ad hoc threshold.
        test_adhoc_y_pred = np.greater(test_y_score, 0.5)
        test_adhoc_cm = sklearn.metrics.confusion_matrix(
            test_y_true, test_adhoc_y_pred)
        test_adhoc_tp = test_adhoc_cm[0][0]
        test_adhoc_fp = test_adhoc_cm[0][1]
        test_adhoc_fn = test_adhoc_cm[1][0]
        test_adhoc_tn = test_adhoc_cm[1][1]

        # Compute test accuracy with ad hoc threshold.
        test_adhoc_acc =\
            (test_adhoc_tn+test_adhoc_tp) /\
            (test_adhoc_tp+test_adhoc_fp+test_adhoc_fn+test_adhoc_tp)

        # Get ROC curve of test set.
        test_fprs, test_tprs, test_thresholds =\
            sklearn.metrics.roc_curve(test_y_true, test_y_score)
        test_accuracies = 0.5 * (1.0 - test_fprs + test_tprs)

        # Find "oracle" threshold maximizing test accuracy.
        oracle_best_threshold_id = np.argmax(test_accuracies)
        oracle_threshold = test_thresholds[oracle_best_threshold_id]
        test_oracle_y_pred = np.greater(test_y_score, oracle_threshold)

        # Compute confusion matrix on test set with oracle threshold.
        test_oracle_cm = sklearn.metrics.confusion_matrix(
            test_y_true, test_oracle_y_pred)
        test_oracle_tp = test_oracle_cm[0][0]
        test_oracle_fp = test_oracle_cm[0][1]
        test_oracle_fn = test_oracle_cm[1][0]
        test_oracle_tn = test_oracle_cm[1][1]

        # Compute test accuracy with oracle threshold.
        test_oracle_acc =\
            (test_oracle_tn+test_oracle_tp) /\
            (test_oracle_tp+test_oracle_fp+test_oracle_fn+test_oracle_tp)

        # Compute area under ROC curve for test set.
        test_auc = sklearn.metrics.roc_auc_score(test_y_true, test_y_score)

        # Format all metrics into a string of comma-separated values.
        row = [
            dataset_name,
            aug_kind_str.rjust(7),
            test_unit_str,
            trial_str,
            "{:.16f}".format(0.5),
            "{:5d}".format(val_adhoc_tp),
            "{:5d}".format(val_adhoc_fp),
            "{:5d}".format(val_adhoc_tn),
            "{:5d}".format(val_adhoc_fn),
            "{:7.3f}".format(val_adhoc_acc*100),
            "{:5d}".format(test_adhoc_tp),
            "{:5d}".format(test_adhoc_fp),
            "{:5d}".format(test_adhoc_tn),
            "{:5d}".format(test_adhoc_fn),
            "{:7.3f}".format(test_adhoc_acc*100),
            "{:.16f}".format(cv_threshold),
            "{:5d}".format(val_cv_tp),
            "{:5d}".format(val_cv_fp),
            "{:5d}".format(val_cv_tn),
            "{:5d}".format(val_cv_fn),
            "{:7.3f}".format(val_cv_acc*100),
            "{:5d}".format(test_cv_tp),
            "{:5d}".format(test_cv_fp),
            "{:5d}".format(test_cv_tn),
            "{:5d}".format(test_cv_fn),
            "{:.16f}".format(oracle_threshold),
            "{:5d}".format(test_oracle_tp),
            "{:5d}".format(test_oracle_fp),
            "{:5d}".format(test_oracle_tn),
            "{:5d}".format(test_oracle_fn),
            "{:7.3f}".format(test_oracle_acc*100),
            "{:7.3f}".format(val_auc*100),
            "{:7.3f}".format(test_auc*100)
            ]

        # Write row to CSV file.
        csv_writer.writerow(row)

    # Close CSV file.
    csv_file.close()


# Print elapsed time.
print(str(datetime.datetime.now()) + " Finish.")
elapsed_time = time.time() - int(start_time)
elapsed_hours = int(elapsed_time / (60 * 60))
elapsed_minutes = int((elapsed_time % (60 * 60)) / 60)
elapsed_seconds = elapsed_time % 60.
elapsed_str = "{:>02}:{:>02}:{:>05.2f}".format(elapsed_hours,
                                               elapsed_minutes,
                                               elapsed_seconds)
print("Total elapsed time: " + elapsed_str + ".")
