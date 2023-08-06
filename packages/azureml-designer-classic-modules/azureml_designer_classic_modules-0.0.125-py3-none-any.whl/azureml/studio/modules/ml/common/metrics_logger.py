import pandas as pd
from collections import namedtuple
from azureml.studio.modules.ml.common.report_data import ReportData
from azureml.core.run import Run
from azureml.studio.core.logger import module_logger

MetricsLogItem = namedtuple("MetricsLogItem", ["name", "data"])


class BaseMetricsLogger:
    # the suffix of metrics name is from binary classification metrics visualization tab naming
    LEFT_PORT_SUFFIX = " (left port)"
    RIGHT_PORT_SUFFIX = " (right port)"

    @classmethod
    def log_metrics(cls, data: pd.DataFrame, data_to_compare: pd.DataFrame = None):
        run = Run.get_context()
        metrics_log_scalars = []

        if data_to_compare is not None:
            # convert data frame to the argument metrics map where key is metric name and value is metric value
            metrics_log_scalars += cls._log_scalar_metrics(run, data.iloc[0, :].to_dict(), cls.LEFT_PORT_SUFFIX)
            metrics_log_scalars += cls._log_scalar_metrics(run, data_to_compare.iloc[0, :].to_dict(),
                                                           cls.RIGHT_PORT_SUFFIX)
        else:
            metrics_log_scalars += cls._log_scalar_metrics(run, data.iloc[0, :].to_dict())

        # flush metrics
        run.flush()

        return metrics_log_scalars

    @classmethod
    def _log_scalar_metrics(cls, run, metrics_map, name_suffix=""):
        metrics_log_scalars = []
        if name_suffix:
            metrics_map = {name + name_suffix: value for name, value in metrics_map.items()}
        for name, value in metrics_map.items():
            if not pd.isna(value):
                module_logger.info(f'Log scalar metric "{name}".')
                run.log(name, value)
                metrics_log_scalars.append(MetricsLogItem(name, value))
            else:
                module_logger.warning(f'Scalar metric "{name}" is null, not log to metrics tab.')

        return metrics_log_scalars


class ClusterMetricsLogger(BaseMetricsLogger):
    CLUSTERING_EVALUATION_TABLE_NAME = "Clustering evaluation"

    @classmethod
    def log_metrics(cls, data: pd.DataFrame, data_to_compare: pd.DataFrame = None):
        run = Run.get_context()
        metrics_log_tables = []

        if data_to_compare is not None:
            metrics_log_tables.append(cls._log_data_frame_as_table(
                run=run,
                data_frame=data,
                name=cls.CLUSTERING_EVALUATION_TABLE_NAME + cls.LEFT_PORT_SUFFIX))
            metrics_log_tables.append(cls._log_data_frame_as_table(
                run=run,
                data_frame=data_to_compare,
                name=cls.CLUSTERING_EVALUATION_TABLE_NAME + cls.RIGHT_PORT_SUFFIX))
        else:
            metrics_log_tables.append(cls._log_data_frame_as_table(
                run=run,
                data_frame=data,
                name=cls.CLUSTERING_EVALUATION_TABLE_NAME))

        run.flush()

        return metrics_log_tables

    @staticmethod
    def _log_data_frame_as_table(run, data_frame, name):
        for _, row in data_frame.iterrows():
            run.log_row(name, **row.to_dict())

        return MetricsLogItem(name=name, data=data_frame.to_dict("list"))


class BinaryClassificationMetricsLogger(BaseMetricsLogger):
    ROC_CURVE_NAME = "ROC curve"
    P_R_CURVE_NAME = "Precision-recall curve"
    LIFT_CURVE_NAME = "Lift curve"
    SCORED_BINS_NAME = "Scored bins"
    CONFUSION_MATRIX_NAME = "Confusion matrix"

    @classmethod
    def log_metrics(cls, report_data: ReportData, report_data_to_compare: ReportData = None):
        # if no valid bins (where there is no valid instances when evaluate), do not log any metrics
        if not report_data.chart.data_points:
            return []

        run = Run.get_context()
        metric_loggers = [cls._log_charts, cls._log_threshold_scalar_metrics, cls._log_confusion_matrix,
                          cls._log_score_bins]
        metric_log_items = []
        if report_data_to_compare is not None:
            for logger in metric_loggers:
                metric_log_items += logger(run, report_data, cls.LEFT_PORT_SUFFIX)
            for logger in metric_loggers:
                metric_log_items += logger(run, report_data_to_compare, cls.RIGHT_PORT_SUFFIX)
        else:
            for logger in metric_loggers:
                metric_log_items += logger(run, report_data)

        # flush metrics
        run.flush()

        return metric_log_items

    @staticmethod
    def _extract_chart_statistics(data_points):
        tpr = [x.tpr for x in data_points]
        fpr = [x.fpr for x in data_points]
        precision = [x.precision for x in data_points]
        recall = [x.recall for x in data_points]
        true_positive = [x.true_positive for x in data_points]
        y_rate = [x.y_rate for x in data_points]

        return tpr, fpr, precision, recall, true_positive, y_rate

    @classmethod
    def _log_charts(cls, run, report_data: ReportData, name_suffix=""):
        # compress bins to the max chart points
        tpr, fpr, precision, recall, true_positive, y_rate = cls._extract_chart_statistics(
            report_data.chart.data_points)

        metric_tables = [MetricsLogItem(f"{cls.ROC_CURVE_NAME}{name_suffix}",
                                        {"False positive rate": fpr, "True positive rate": tpr}),
                         MetricsLogItem(f"{cls.P_R_CURVE_NAME}{name_suffix}",
                                        {"Recall": recall, "Precision": precision}),
                         MetricsLogItem(f"{cls.LIFT_CURVE_NAME}{name_suffix}",
                                        {"Positive rate": y_rate, "Number of true positive": true_positive})]

        for table in metric_tables:
            cls._log_table_by_rows(run, table)

        return metric_tables

    @staticmethod
    def _log_table_by_rows(run, table):
        module_logger.info(f'Log metrics table "{table.name}" by row.')
        data_df = pd.DataFrame(table.data)
        for _, row in data_df.iterrows():
            run.log_row(table.name, **row.to_dict())

    @staticmethod
    def _extract_score_bin_statistics(coarse_data, displayed_decimal=3):
        score_bin = [f'({round(x.bin_start, displayed_decimal)},{round(x.bin_end, displayed_decimal)}]' for x in
                     coarse_data]
        positive_example = [x.num_positive for x in coarse_data]
        negative_example = [x.num_negative for x in coarse_data]
        count = [x.count for x in coarse_data]
        fraction_above_threshold = [round(sum(count[i:]) / sum(count), displayed_decimal) for i in range(len(count))]
        accuracy = [round(x.accuracy, displayed_decimal) for x in coarse_data]
        f1 = [round(x.f1, displayed_decimal) for x in coarse_data]
        precision = [round(x.precision, displayed_decimal) for x in coarse_data]
        recall = [round(x.recall, displayed_decimal) for x in coarse_data]
        negative_precision = [round(x.neg_precision, displayed_decimal) for x in coarse_data]
        negative_recall = [round(x.neg_recall, displayed_decimal) for x in coarse_data]
        auc = [round(x.auc, displayed_decimal) for x in coarse_data]
        cumulative_auc = [round(sum(auc[i:]), displayed_decimal) for i in range(len(auc))]

        bins = {"Score bin": score_bin,
                "Positive example": positive_example,
                "Negative example": negative_example,
                "Fraction above threshold": fraction_above_threshold,
                "Accuracy": accuracy,
                "F1 Score": f1,
                "Precision": precision,
                "Recall": recall,
                "Negative precision": negative_precision,
                "Negative recall": negative_recall,
                "Cumulative AUC": cumulative_auc}
        return bins

    @classmethod
    def _log_score_bins(cls, run, report_data: ReportData, name_suffix=""):
        bins = cls._extract_score_bin_statistics(report_data.chart.coarse_data)
        bins_table = MetricsLogItem(f"{cls.SCORED_BINS_NAME}{name_suffix}", bins)
        cls._log_table_by_rows(run, bins_table)

        return bins_table,

    @classmethod
    def _log_threshold_scalar_metrics(cls, run, report_data: ReportData, name_suffix=""):
        coarse_data = report_data.chart.coarse_data
        threshold_bin = coarse_data[len(coarse_data) // 2]
        accuracy = threshold_bin.accuracy
        precision = threshold_bin.precision
        recall = threshold_bin.recall
        f1 = threshold_bin.f1
        auc = report_data.chart.auc

        metrics_map = {"Accuracy": accuracy,
                       "Precision": precision,
                       "Recall": recall,
                       "F1 Score": f1,
                       "AUC": auc}
        return cls._log_scalar_metrics(run, metrics_map, name_suffix)

    @classmethod
    def _log_confusion_matrix(cls, run, report_data: ReportData, name_suffix=""):
        predicted_label_column_name = "Predicted label"
        predicted_label_prefix = "Predicted"
        actual_label_prefix = "Actual"

        positive_label = report_data.chart.positive_label
        negative_label = report_data.chart.negative_label
        predicted_label_column = [f"{predicted_label_prefix}_{positive_label}",
                                  f"{predicted_label_prefix}_{negative_label}"]

        coarse_data = report_data.chart.coarse_data
        threshold_bin = coarse_data[len(coarse_data) // 2]
        actual_positive_label_column_name = f"{actual_label_prefix}_{positive_label}"
        actual_positive_label_column = [threshold_bin.true_positive, threshold_bin.false_negative]
        actual_negative_label_column_name = f"{actual_label_prefix}_{negative_label}"
        actual_negative_label_column = [threshold_bin.false_positive, threshold_bin.true_negative]

        confusion_matrix_table = MetricsLogItem(f"{cls.CONFUSION_MATRIX_NAME}{name_suffix}",
                                                {predicted_label_column_name: predicted_label_column,
                                                 actual_positive_label_column_name: actual_positive_label_column,
                                                 actual_negative_label_column_name: actual_negative_label_column})
        module_logger.info(f'Log metrics table "{confusion_matrix_table.name}".')
        run.log_table(confusion_matrix_table.name, confusion_matrix_table.data)

        return confusion_matrix_table,
