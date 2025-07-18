import numpy as np

from pymoo.constraints.adaptive import AdaptiveConstraintHandling


class AdaptiveEpsilonConstraintHandling(AdaptiveConstraintHandling):

    def __init__(self, algorithm, perc_eps_until=0.5):
        super().__init__(algorithm)
        self.perc_eps_until = perc_eps_until
        self.max_cv = None

    def _adapt_constraint_handling(self, config, **kwargs):
        t = self.termination.perc
        alpha = np.maximum(0.0, 1 - 1 / self.perc_eps_until * t)
        eps = alpha * self.max_cv

        config["cv_eps"] = eps

    def _initialize_advance(self, infills=None, **kwargs):

        # get the average constraint violation in the current generation
        if infills is not None and infills.has("cv"):
            cv = infills.get("cv")
            self.max_cv = np.mean(cv)
        elif self.pop is not None and self.pop.has("cv"):
            # Use current population if available
            cv = self.pop.get("cv")
            self.max_cv = np.mean(cv)
        else:
            # Default value during initialization
            self.max_cv = 1.0

        return super()._initialize_advance(infills, **kwargs)
