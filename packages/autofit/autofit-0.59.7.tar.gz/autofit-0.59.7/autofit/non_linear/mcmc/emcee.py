import logging
import os
import emcee

from autofit import exc
from autofit.non_linear.mcmc.abstract_mcmc import AbstractMCMC
from autofit.non_linear.samples import MCMCSamples
logger = logging.getLogger(__name__)


class Emcee(AbstractMCMC):
    def __init__(
        self,
        paths=None,
        sigma=3,
        nwalkers=None,
        nsteps=None,
        initialize_method=None,
        initialize_ball_lower_limit=None,
        initialize_ball_upper_limit=None,
        auto_correlation_check_for_convergence=None,
        auto_correlation_check_size=None,
        auto_correlation_required_length=None,
        auto_correlation_change_threshold=None,
        iterations_per_update=None,
        number_of_cores=None,
    ):
        """ Class to setup and run an Emcee non-linear search.

        For a full description of Emcee, checkout its Github and readthedocs webpages:

        https://github.com/dfm/emcee

        https://emcee.readthedocs.io/en/stable/

        Extensions:

        - Provides the option to check the auto-correlation length of the samples during the run and terminating
          sampling early if these meet a specified threshold. See this page
          (https://emcee.readthedocs.io/en/stable/tutorials/autocorr/#autocorr) for a description.

        - Provides different options for walker initialization, with the default 'ball' method starting all walkers
          close to one another in parameter space, as recommended in the Emcee documentation
          (https://emcee.readthedocs.io/en/stable/user/faq/).

        If you use *Emcee* as part of a published work, please cite the package following the instructions under the
        *Attribution* section of the GitHub page.

        Parameters
        ----------
        paths : af.Paths
            A class that manages all paths, e.g. where the phase outputs are stored, the non-linear search samples,
            backups, etc.
        sigma : float
            The error-bound value that linked Gaussian prior withs are computed using. For example, if sigma=3.0,
            parameters will use Gaussian Priors with widths coresponding to errors estimated at 3 sigma confidence.
        nwalkers : int
            The number of walkers in the ensemble used to sample parameter space.
        nsteps : int
            The number of steps that must be taken by every walker. The non-linear search will thus run for nwalkers *
            nsteps iterations.
        initialize_method : str
            The method used to generate where walkers are initialized in parameter space, with options:
            ball (default):
                Walkers are initialized by randomly drawing unit values from a uniform distribution between the
                initialize_ball_lower_limit and initialize_ball_upper_limit values. It is recommended these limits are
                small, such that all walkers begin close to one another.
            prior:
                Walkers are initialized by randomly drawing unit values from a uniform distribution between 0 and 1,
                thus being distributed over the prior.
        initialize_ball_lower_limit : float
            The lower limit of the uniform distribution unit values are drawn from when initializing walkers using the
            ball method.
        initialize_ball_upper_limit : float
            The upper limit of the uniform distribution unit values are drawn from when initializing walkers using the
            ball method.
        auto_correlation_check_for_convergence : bool
            Whether the auto-correlation lengths of the Emcee samples are checked to determine the stopping criteria.
            If *True*, this option may terminate the Emcee run before the input number of steps, nsteps, has
            been performed. If *False* nstep samples will be taken.
        auto_correlation_check_size : int
            The length of the samples used to check the auto-correlation lengths (from the latest sample backwards).
            For convergence, the auto-correlations must not change over a certain range of samples. A longer check-size
            thus requires more samples meet the auto-correlation threshold, taking longer to terminate sampling.
            However, shorter chains risk stopping sampling early due to noise.
        auto_correlation_required_length : int
            The length an auto_correlation chain must be for it to be used to evaluate whether its change threshold is
            sufficiently small to terminate sampling early.
        auto_correlation_change_threshold : float
            The threshold value by which if the change in auto_correlations is below sampling will be terminated early.
        number_of_cores : int
            The number of cores Emcee sampling is performed using a Python multiprocessing Pool instance. If 1, a
            pool instance is not created and the job runs in serial.

        All remaining attributes are emcee parameters and described at the emcee API webpage:

        https://emcee.readthedocs.io/en/stable/
        """

        self.sigma = sigma

        self.nwalkers = self.config("search", "nwalkers", int) if nwalkers is None else nwalkers
        self.nsteps = self.config("search", "nsteps", int) if nsteps is None else nsteps

        self.auto_correlation_check_for_convergence = (
            self.config("auto_correlation", "check_for_convergence", bool)
            if auto_correlation_check_for_convergence is None
            else auto_correlation_check_for_convergence
        )
        self.auto_correlation_check_size = (
            self.config("auto_correlation", "check_size", int)
            if auto_correlation_check_size is None
            else auto_correlation_check_size
        )
        self.auto_correlation_required_length = (
            self.config("auto_correlation", "required_length", int)
            if auto_correlation_required_length is None
            else auto_correlation_required_length
        )
        self.auto_correlation_change_threshold = (
            self.config("auto_correlation", "change_threshold", float)
            if auto_correlation_change_threshold is None
            else auto_correlation_change_threshold
        )

        super().__init__(
            paths=paths,
            initialize_method=initialize_method,
            initialize_ball_lower_limit=initialize_ball_lower_limit,
            initialize_ball_upper_limit=initialize_ball_upper_limit,
            iterations_per_update=iterations_per_update,
        )

        self.number_of_cores = (
            self.config("parallel", "number_of_cores", int)
            if number_of_cores is None
            else number_of_cores
        )

        logger.debug("Creating Emcee NLO")


    class Fitness(AbstractMCMC.Fitness):
        def __call__(self, params):

            try:

                instance = self.model.instance_from_vector(vector=params)
                log_likelihood = self.fit_instance(instance)
                log_priors = self.model.log_priors_from_vector(vector=params)
                return log_likelihood + sum(log_priors)

            except exc.FitException:
                return self.resample_likelihood

    def _fit(self, model, analysis):
        """
        Fit a model using Emcee and the Analysis class which contains the data and returns the log likelihood from
        instances of the model, which the non-linear search seeks to maximize.

        Parameters
        ----------
        model : ModelMapper
            The model which generates instances for different points in parameter space.
        analysis : Analysis
            Contains the data and the log likelihood function which fits an instance of the model to the data, returning
            the log likelihood the non-linear search maximizes.

        Returns
        -------
        A result object comprising the Samples object that inclues the maximum log likelihood instance and full
        chains used by the fit.
        """
        pool, pool_ids = self.make_pool()

        fitness_function = self.fitness_function_from_model_and_analysis(
            model=model, analysis=analysis, pool_ids=pool_ids,
        )

        emcee_sampler = emcee.EnsembleSampler(
            nwalkers=self.nwalkers,
            ndim=model.prior_count,
            log_prob_fn=fitness_function.__call__,
            backend=emcee.backends.HDFBackend(filename=self.paths.samples_path + "/emcee.hdf"),
            pool=pool,

        )

        try:

            emcee_state = emcee_sampler.get_last_sample()

            samples = self.samples_from_model(model=model)

            total_iterations = emcee_sampler.iteration

            if samples.converged:
                iterations_remaining = 0
            else:
                iterations_remaining = self.nsteps - total_iterations

        except AttributeError:

            emcee_state = self.initial_points_from_model(number_of_points=emcee_sampler.nwalkers, model=model)

            total_iterations = 0
            iterations_remaining = self.nsteps


        logger.info("Running Emcee Sampling...")

        while iterations_remaining > 0:

            if self.iterations_per_update > iterations_remaining:
                iterations = iterations_remaining
            else:
                iterations = self.iterations_per_update

            for sample in emcee_sampler.sample(
                initial_state=emcee_state,
                iterations=iterations,
                progress=True,
                skip_initial_state_check=True,
                store=True,
            ):

                pass

            total_iterations += iterations
            iterations_remaining = self.nsteps - total_iterations

            samples = self.perform_update(model=model, analysis=analysis, during_analysis=True)

            if emcee_sampler.iteration % self.auto_correlation_check_size:
                if samples.converged and self.auto_correlation_check_for_convergence:
                    iterations_remaining = 0

        logger.info("Emcee complete")

    @property
    def tag(self):
        """Tag the output folder of the PySwarms non-linear search, according to the number of particles and
        parameters defining the search strategy."""

        name_tag = self.config('tag', 'name')
        nwalkers_tag = f"{self.config('tag', 'nwalkers')}_{self.nwalkers}"

        return f'{name_tag}__{nwalkers_tag}'

    def copy_with_name_extension(self, extension, remove_phase_tag=False):
        """Copy this instance of the emcee non-linear search with all associated attributes.

        This is used to set up the non-linear search on phase extensions."""
        copy = super().copy_with_name_extension(
            extension=extension, remove_phase_tag=remove_phase_tag
        )
        copy.sigma = self.sigma
        copy.nwalkers = self.nwalkers
        copy.nsteps = self.nsteps
        copy.auto_correlation_check_for_convergence = self.auto_correlation_check_for_convergence
        copy.auto_correlation_check_size = self.auto_correlation_check_size
        copy.auto_correlation_required_length = self.auto_correlation_required_length
        copy.auto_correlation_change_threshold = self.auto_correlation_change_threshold
        copy.initialize_method = self.initialize_method
        copy.initialize_ball_lower_limit = self.initialize_ball_lower_limit
        copy.initialize_ball_upper_limit = self.initialize_ball_upper_limit
        copy.iterations_per_update = self.iterations_per_update
        copy.number_of_cores = self.number_of_cores

        return copy

    def fitness_function_from_model_and_analysis(self, model, analysis, pool_ids=None):

        return Emcee.Fitness(
            paths=self.paths,
            model=model,
            analysis=analysis,
            samples_from_model=self.samples_from_model,
            pool_ids=pool_ids,
        )

    def samples_from_model(self, model):
        """Create a *Samples* object from this non-linear search's output files on the hard-disk and model.

        For Emcee, all quantities are extracted via the hdf5 backend of results.

        Parameters
        ----------
        model
            The model which generates instances for different points in parameter space. This maps the points from unit
            cube values to physical values via the priors.
        paths : af.Paths
            A class that manages all paths, e.g. where the phase outputs are stored, the non-linear search chains,
            backups, etc.
        """

        parameters = self.backend.get_chain(flat=True).tolist()
        log_priors = [
            sum(model.log_priors_from_vector(vector=vector)) for vector in parameters
        ]
        log_likelihoods = self.backend.get_log_prob(flat=True).tolist()
        weights = len(log_likelihoods) * [1.0]
        auto_correlation_time = self.backend.get_autocorr_time(tol=0)
        total_walkers = len(self.backend.get_chain()[0, :, 0])
        total_steps = len(self.backend.get_log_prob())

        return MCMCSamples(
            model=model,
            parameters=parameters,
            log_likelihoods=log_likelihoods,
            log_priors=log_priors,
            weights=weights,
            total_walkers=total_walkers,
            total_steps=total_steps,
            auto_correlation_times=auto_correlation_time,
            auto_correlation_check_size=self.auto_correlation_check_size,
            auto_correlation_required_length=self.auto_correlation_required_length,
            auto_correlation_change_threshold=self.auto_correlation_change_threshold,
            backend=self.backend,
        )

    @property
    def backend(self) -> emcee.backends.HDFBackend:
        """The *Emcee* hdf5 backend, which provides access to all samples, likelihoods, etc. of the non-linear search.

        The sampler is described in the "Results" section at https://dynesty.readthedocs.io/en/latest/quickstart.html"""
        if os.path.isfile(self.paths.samples_path + "/emcee.hdf"):
            return emcee.backends.HDFBackend(
                filename=self.paths.samples_path + "/emcee.hdf"
            )
        else:
            raise FileNotFoundError(
                "The file emcee.hdf does not exist at the path " + self.paths.samples_path
            )