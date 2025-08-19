import sys
sys.path.append('/glade/u/home/chayan/myutils/')
import errormetrics as em

def compute_metrics(predictions, observations, metric_list=None):
    """
    Compute error metrics using the errormetrics module.
    metric_list: list of metric names to compute (default: all)
    """
    metrics = em.ErrorMetrics(predictions=predictions, observations=observations)
    if metric_list is None:
        return metrics.all_metrics(2)
    else:
        return metrics.get_metrics(metric_list) 