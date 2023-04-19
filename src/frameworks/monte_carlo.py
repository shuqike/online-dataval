import numpy as np
import torch
from src.frameworks.valuator import Valuator
import src.utils as utils
from tqdm import tqdm


class TruncatedMC(Valuator):
    def __init__(self,
                 model_family,
                 train_dataset,
                 num_data,
                 test_dataset,
                 sources=None,
                 seed=None,
                 perf_metric='accuracy',
                 **kwargs) -> None:
        """
        Args:
            X: Data covariates
            y: Data labels
            X_test: Test+Held-out covariates
            y_test: Test+Held-out labels
            sources: An array or dictionary assiging each point to its group.
                If None, evey points gets its individual value
            samples_weights: Weight of train samples in the loss function
                (for models where weighted training method is enabled.)
            model_family: The model family used for learning algorithm
            metric: Evaluation metric
            seed: Random seed. When running parallel monte-carlo samples,
                we initialize each with a different seed to prevent getting 
                same permutations
            directory: Directory to save results and figures
            **kwargs: Arguments of the model
        """
        # Sanity check for datasets
        assert 'feature' in train_dataset,\
            'Cannot find "feature" in the training dataset dictionary'
        assert 'feature' in test_dataset,\
            'Cannot find "feature" in the testing dataset dictionary'
        if len(test_dataset) > 2:
            assert perf_metric != 'f1', 'Invalid metric for multiclass!'
            assert perf_metric != 'auc', 'Invalid metric for multiclass!'

        # Prepare datasets
        if seed is not None:
            np.random.seed(seed)
            torch.manual_seed(seed)
        self.sources = sources
        self.train_dataset = train_dataset
        self.num_data = len(self.train_dataset['feature'])
        self.test_dataset = test_dataset

        # Prepare model
        self.model_family = model_family
        self.model = utils.return_model(self.model_family, **kwargs)
        self.perf_metric = perf_metric

        # Get the score of the initial model
        self.random_score = self._init_score()

    def _init_score(self):
        """Get the score of the initial model.
        """
        if self.perf_metric == 'accuracy':
            hist = np.bincount(self.test_dataset['label']).astype(float) / len(self.test_dataset['label'])
            return np.max(hist)
        else:
            raise NotImplementedError

    def _calc_loo(self):
        """Calculate leave-one-out values for the given metric.
        """
        if sources is None:
            # Each datum has its own source
            sources = {i:np.array([i]) for i in range(len(self.X))}
        elif not isinstance(sources, dict):
            # Set down the given sources as a dict
            sources = {i:np.where(sources==i)[0] for i in set(sources)}
        self.model.fit(self.train_dataset, self.test_dataset)
        baseline_val = self.model.perf_metric(self.test_dataset)
        self.vals_loo = np.zeros(self.num_data)
        for i in tqdm(self.sources.keys()):
            X_batch = np.delete(self.train_dataset['feature'], self.sources[i], axis=0)
            y_batch = np.delete(self.train_dataset['label'], self.sources[i], axis=0)
            self.model.reset()
            self.model.fit(
                train_dataset={
                    'feature': X_batch,
                    'label': y_batch
                }
            )
            removed_val = self.model.perf_metric(self.test_dataset)
            self.vals_loo[sources[i]] = (baseline_val - removed_val)
            self.vals_loo[sources[i]] /= len(sources[i])

    def run(self, save_every, err, tol=1e-2, do_gshap=True, do_loo=False):
        """
        Calculates datum values
        Args:
            save_every: save marginal contrivbutions every n iterations
            err: stopping criteria
            tol: truncation tolerance. If None, it's computed
            gshap: whether to use G-Shapley to compute marginal contributions
            loo: whether to use Leave-One-Out to compute marginal contributions
        """
        if do_loo:
            try:
                len(self._loo_vals)
            except:
                print('Calculate leave-one-out')
                self._calc_loo()
            do_tmc = True
            while do_tmc or do_gshap:
                if do_gshap:
                    pass
                if do_tmc:
                    pass
