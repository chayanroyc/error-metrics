import optuna
from optuna.samplers import TPESampler, CmaEsSampler, BaseSampler
from optuna.pruners import BasePruner
import typing

class DuplicateIterationPruner(BasePruner):
    def prune(self, study: "optuna.study.Study", trial: "optuna.trial.FrozenTrial") -> bool:
        completed_trials = study.get_trials(states=[optuna.trial.TrialState.COMPLETE])
        for completed_trial in completed_trials:
            if completed_trial.params == trial.params:
                return True
        return False

class SwitchingSampler(optuna.samplers.BaseSampler):
    def __init__(self, switch_trial=30, seed=None):
        self._tpe = TPESampler(seed=seed, multivariate=True, group=True)
        self._cmaes = CmaEsSampler(seed=seed, consider_pruned_trials=False)
        self._switch_trial = switch_trial
    def infer_relative_search_space(self, study, trial):
        if trial.number <= self._switch_trial:
            return self._tpe.infer_relative_search_space(study, trial)
        return self._cmaes.infer_relative_search_space(study, trial)
    def sample_relative(self, study, trial, search_space):
        if trial.number <= self._switch_trial:
            return self._tpe.sample_relative(study, trial, search_space)
        return self._cmaes.sample_relative(study, trial, search_space)
    def sample_independent(self, study, trial, param_name, param_distribution):
        if trial.number <= self._switch_trial:
            return self._tpe.sample_independent(study, trial, param_name, param_distribution)
        return self._cmaes.sample_independent(study, trial, param_name, param_distribution)

class MultiplePruners(optuna.pruners.BasePruner):
    def __init__(self, pruners: typing.Iterable[optuna.pruners.BasePruner], pruning_condition: str = "any"):
        self._pruners = tuple(pruners)
        self._pruning_condition_check_fn = any if pruning_condition == "any" else all
    def prune(self, study: optuna.study.Study, trial: optuna.trial.FrozenTrial) -> bool:
        return self._pruning_condition_check_fn(pruner.prune(study, trial) for pruner in self._pruners)

class EarlyStoppingPruner(optuna.pruners.BasePruner):
    def __init__(self, min_trials=10, patience=5, min_delta=0.001):
        self.min_trials = min_trials
        self.patience = patience
        self.min_delta = min_delta
        self.best_value = float('inf')
        self.no_improvement_count = 0
    def prune(self, study: "optuna.study.Study", trial: "optuna.trial.FrozenTrial") -> bool:
        if trial.number < self.min_trials:
            return False
        current_value = trial.value
        if current_value is None:
            return False
        if current_value < self.best_value - self.min_delta:
            self.best_value = current_value
            self.no_improvement_count = 0
        else:
            self.no_improvement_count += 1
        return self.no_improvement_count >= self.patience 