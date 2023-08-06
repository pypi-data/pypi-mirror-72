from microcosm_logging.decorators import logger

from microcosm_sagemaker.decorators import metrics_observer, training_initializer
from wandb.apis import CommError


try:
    import wandb
except ImportError:
    pass


@training_initializer()
@metrics_observer()
@logger
class WeightsAndBiases:
    def __init__(self, graph):
        self.graph = graph
        self.testing = graph.metadata.testing
        self.project_name = graph.metadata.name.replace("_", "-")
        self.bundle_and_dependencies_config_extractor = self.graph.bundle_and_dependencies_config_extractor
        self.active_bundle = getattr(graph, graph.config.active_bundle)
        self.run_path = getattr(graph.config.wandb, "run_path", None)

    def init(self):
        # Only initialize wandb if it is not a testing
        if self.testing:
            return

        # Pushing into an existing wandb experiment
        if self.run_path:

            try:
                self.wandb_run = wandb.Api().run(path=self.run_path)
                self.logger.info(f"The existing Weights & Biases run was loaded: {self.run_path}")

            except CommError:
                # If the previous run cannot be found:
                #   - Start a new run instead
                #   - Add a note to the new run that this run is related to a previous run
                self.logger.warning(f"Could not find run: {self.run_path}")
                self.wandb_run = self._create_new_wandb_run(
                    notes=f"Related to previous run: {self.run_path}",
                )

        # Creating a new wandb experiment
        else:
            self.wandb_run = self._create_new_wandb_run()

    def _create_new_wandb_run(self, notes=None):
        wandb_run = wandb.init(
            project=self.project_name,
            config=self.bundle_and_dependencies_config_extractor(self.active_bundle),
            notes=notes,
        )

        # Injecting the wandb run path into the config
        self.graph.config.wandb.run_path = wandb_run.path

        self.logger.info(f"A new `weights & biases` run was created: {wandb_run.path}")

        return wandb_run

    def log_timeseries(self, **kwargs):
        step = kwargs.pop("step")
        self.wandb_run.log(row=kwargs, step=step)
        return None

    def log_static(self, **kwargs):
        self.wandb_run.summary.update(kwargs)
        return None
