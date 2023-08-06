from rura.pipeline.processes.temp import TempProcess
from rura.utils.paths import RESULTS
from rura.tracker import Tracker
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np
import mlflow
import os


class SuicideProcess(TempProcess):
    @staticmethod
    def __get_output_path(model, file=''):
        return os.path.join(RESULTS, *model.path, file)

    def extra_metrics(self, model, x_train, y_train, x_val, y_val, x_test, y_test):
        if not os.path.exists(self.__get_output_path(model)):
            os.makedirs(self.__get_output_path(model))

        train_pred = model.predict(x_train, data_type='train')
        val_pred = model.predict(x_val, data_type='val')

        self.__save_pr_curve(model, train_pred, y_train, val_pred, y_val)
        self.__save_probs(model, train_pred, val_pred)
        self.__class_reports(model, train_pred, y_train, val_pred, y_val)

        # Save the results
        # self.__save_results(run_title, {
        #     'date': datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
        # })

    def __class_reports(self, model, train_pred, y_train, val_pred, y_val):
        train_pred = np.round(train_pred).flatten()
        val_pred = np.round(val_pred).flatten()

        pred = {
            'train': classification_report(y_train, train_pred, output_dict=True),
            'val': classification_report(y_val, val_pred, output_dict=True)
        }

        for t, report in pred.items():
            for m in ['precision', 'recall', 'f1-score']:
                for c in ['0', '1', 'macro avg', 'weighted avg']:
                    if c in report:
                        mlflow.log_metric(t + '_' + m + '_c' + c, report[c][m])
                    else:
                        mlflow.log_metric(t + '_' + m + '_c' + c, np.nan)

        self.__save_reports(model,
                            classification_report(y_train, train_pred),
                            classification_report(y_val, val_pred))

    # def __save_results(self, run_title, obj):
    #     with open(self.__get_output_path(run_title, file='train.json'), 'w') as w:
    #         json.dump(obj, w)

    def __save_probs(self, model, train_pred, val_pred):
        train_pred = train_pred.flatten()
        val_pred = val_pred.flatten()

        def generate_hist(data_type, y_pred):
            plt.hist(y_pred, color='steelblue')
            plt.title(data_type + ' Prediction Probabilities')
            plt.savefig(self.__get_output_path(model, file=data_type + '_probs_hist.png'))
            plt.clf()
            mlflow.log_artifact(self.__get_output_path(model, file=data_type + '_probs_hist.png'))

        generate_hist('train', train_pred)
        generate_hist('val', val_pred)

    def __save_pr_curve(self, model, train_pred, y_train, val_pred, y_val):
        train_pred = train_pred.flatten()
        val_pred = val_pred.flatten()

        def generate_curve(data_type, y_true, y_pred):
            from sklearn.metrics import precision_recall_curve, auc, average_precision_score, roc_auc_score
            from inspect import signature

            precision, recall, _ = precision_recall_curve(y_true, y_pred)
            area = auc(recall, precision)
            average_precision = average_precision_score(y_true, y_pred)
            roc_auc = roc_auc_score(y_true, y_pred)

            if Tracker.IS_LOGGING:
                mlflow.log_metric(data_type + '_auc', roc_auc)
                mlflow.log_metric(data_type + '_auc_pr', average_precision)

            # In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
            step_kwargs = ({'step': 'post'}
                           if 'step' in signature(plt.fill_between).parameters
                           else {})
            plt.step(recall, precision, color='b', alpha=0.2,
                     where='post')
            plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)

            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.ylim([0.0, 1.05])
            plt.xlim([0.0, 1.0])
            plt.title('Precision-Recall Curve: AP={0:0.2f}; AUC={0:0.2f}'.format(average_precision, auc))
            plt.savefig(self.__get_output_path(model, file=data_type + '_pr_curve.png'))
            plt.clf()
            mlflow.log_artifact(self.__get_output_path(model, file=data_type + '_pr_curve.png'))

        generate_curve('train', y_train, train_pred)
        generate_curve('val', y_val, val_pred)

    def __save_reports(self, model, train_report, val_report):
        with open(self.__get_output_path(model, file='class_reports.txt'), 'w') as w:
            w.write('Train\n')
            w.write(train_report)
            w.write('\n\n')
            w.write('Val\n')
            w.write(val_report)

        mlflow.log_artifact(self.__get_output_path(model, file='class_reports.txt'))
