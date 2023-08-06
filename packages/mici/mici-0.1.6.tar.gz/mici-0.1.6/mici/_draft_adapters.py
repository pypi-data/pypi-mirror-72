class BatchCovarianceMetricAdapter(Adapter):

    def __init__(self, reg_iter_offset=5, reg_coefficient=1e-3):
        """
        Args:
            reg_iter_offset (int): Iteration offset used for calculating
                iteration dependent weighting between regularisation target and
                current covariance estimate. Higher values cause stronger
                regularisation during initial iterations.
            reg_scale (float): Positive scalar defining value variance estimates
                are regularized towards.
        """
        self.reg_iter_offset = reg_iter_offset
        self.reg_coefficient = reg_coefficient

    def initialize(self, chain_state, transition):
        return {
            'iter': 0,
            'pos_samples': []
        }

    def update(self, chain_state, adapt_state, trans_stats, transition):
        adapt_state['iter'] += 1
        adapt_state['pos_samples'].append(chain_state.pos)

    def finalize(self, adapt_state, transition):
        if isinstance(adapt_state, dict):
            n_iter = adapt_state['iter']
            covar_factor = np.stack(adapt_state['pos_samples'], 1)
        else:
            # Use pooled covariance estimator
            # https://en.wikipedia.org/wiki/Pooled_covariance_matrix
            n_iter, pos_samples = 0, []
            for i, a in enumerate(adapt_state):
                n_iter += a['iter']
                pos_samples += a['pos_samples']
            covar_factor = np.stack(pos_samples, 1)
        mean = covar_factor.mean(1)
        covar_factor -= mean[:, None]
        covar_factor /= (n_iter - 1)**0.5
        covar_factor *= (n_iter / (self.reg_iter_offset + n_iter))**0.5
        identity_scale = self.reg_coefficient * (
            self.reg_iter_offset / (self.reg_iter_offset + n_iter))
        dim_pos = covar_factor.shape[0]
        transition.system.metric = PositiveDefiniteLowRankUpdateMatrix(
            covar_factor,
            PositiveScaledIdentityMatrix(identity_scale, dim_pos)).inv
