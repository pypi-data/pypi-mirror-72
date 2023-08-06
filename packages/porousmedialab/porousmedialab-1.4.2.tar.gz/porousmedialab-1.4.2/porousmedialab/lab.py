""" PorousMediaLab super class. Contains all the main methods.
"""

import sys
import time
import traceback

import numexpr as ne
import numpy as np

import porousmedialab.desolver as desolver
import porousmedialab.equilibriumsolver as equilibriumsolver
import porousmedialab.phcalc as phcalc
from porousmedialab.dotdict import DotDict
import porousmedialab.saver as saver


class Lab:
    """The batch experiments simulations"""

    def __init__(self, tend, dt, tstart=0):
        """ init function

        initialize the lab class

        Arguments:
            tend {float} -- end time of computation
            dt {float} -- timestep

        Keyword Arguments:
            tstart {float} -- start time of computation (default: {0})
        """

        self.tend = tend
        self.dt = dt
        self.time = np.linspace(tstart, tend, round(tend / dt) + 1)
        self.species = DotDict({})
        self.dynamic_functions = DotDict({})
        self.profiles = DotDict({})
        self.dcdt = DotDict({})
        self.rates = DotDict({})
        self.estimated_rates = DotDict({})
        self.constants = DotDict({})
        self.functions = DotDict({})
        self.henry_law_equations = []
        self.acid_base_components = []
        self.acid_base_system = phcalc.System()
        self.ode_method = 'scipy'

    def __getattr__(self, attr):
        """dot notation for species

        you can use lab.element and get
        species dictionary

        Arguments:
            attr {str} -- name of the species

        Returns:
            DotDict -- returns DotDict of species
        """

        return self.species[attr]

    def save_results_in_hdf5(self):
        """concentrations and rate profiles in the
        hdf5 files
        """
        self.reconstruct_rates()
        concentrations = {k: v['concentration'] for k, v in self.species.items()}

        results = {}
        results['time'] = self.time
        results['concentrations'] = concentrations
        results['estimated_rates'] = self.estimated_rates
        results['rates'] = self.rates
        results['parameters'] = {k: str(v) for k, v in self.constants.items()}

        saver.save_dict_to_hdf5(results, 'results.h5')

    def solve(self, verbose=True):
        """ solves coupled PDEs

        Keyword Arguments:
            verbose {bool} -- if true verbose output (default: {True})
            with estimation of computational time etc.
        """

        self.reset()
        with np.errstate(invalid='raise'):
            for i in np.arange(1, len(self.time)):
                try:
                    self.integrate_one_timestep(i)
                    if verbose:
                        self.estimate_time_of_computation(i)
                except FloatingPointError as inst:
                    print(
                        '\nABORT!!!: Numerical instability... Please, adjust dt and dx manually...'
                    )
                    traceback.print_exc()
                    sys.exit()

        # temporal hack for time dependent variables
        if 'TIME' in self.species:
            self.species.pop('TIME', None)

    def estimate_time_of_computation(self, i):
        """ function estimates time required for computation

        uses first hundread of steps to estimate approximate
        time for computation of all steps

        Arguments:
            i {int} -- index of time
        """

        if i == 1:
            self.start_computation_time = time.time()
            print("Simulation started:\n\t",
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if i == 100:
            total_t = len(self.time) * (
                time.time() - self.start_computation_time
            ) / 100 * self.dt / self.dt
            m, s = divmod(total_t, 60)
            h, m = divmod(m, 60)
            print(
                "\n\nEstimated time of the code execution:\n\t %dh:%02dm:%02ds"
                % (h, m, s))
            print("Will finish approx.:\n\t",
                  time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime(time.time() + total_t)))

    def henry_equilibrium_integrate(self, i):
        """integrates Henry equlibrium reactions

        Estimates the destribution of species using functions from
        equilibriumsolver, and, then, updated the profiles with new
        concentrations

        Arguments:
            i {int} -- index of time
        """

        for eq in self.henry_law_equations:
            self.species[eq['gas']]['concentration'][:, i], self.species[eq[
                'aq']][
                    'concentration'][:, i] = equilibriumsolver.solve_henry_law(
                        self.species[eq['aq']]['concentration'][:, i] +
                        self.species[eq['gas']]['concentration'][:, i],
                        eq['Hcc'])
            for elem in [eq['gas'], eq['aq']]:
                self.profiles[elem] = self.species[elem]['concentration'][:, i]
                if self.species[elem]['int_transport']:
                    self.update_matrices_due_to_bc(elem, i)

    def acid_base_solve_ph(self, i):
        """solves acid base reactions

        solves acid-base using function from phcalc. First, it sums the total
        concentration for particular species, then, estimates pH. if it idx=0,
        then it uses "greedy" algorithm, else, uses +-0.1 of previous pH and
        finds minimum around it.

        Arguments:
            i {[type]} -- [description]
        """

        # initial guess from previous time-step
        res = self.species['pH']['concentration'][0, i - 1]
        for idx_j in range(self.N):
            for c in self.acid_base_components:
                init_conc = 0
                for element in c['species']:
                    init_conc += self.species[element]['concentration'][idx_j,
                                                                        i]
                c['pH_object'].conc = init_conc
            if idx_j == 0:
                self.acid_base_system.pHsolve(guess=7, tol=1e-4)
                res = self.acid_base_system.pH
            else:
                phs = np.linspace(res - 0.1, res + 0.1, 201)
                idx = self.acid_base_system._diff_pos_neg(phs).argmin()
                res = phs[idx]
            self.species['pH']['concentration'][idx_j, i] = res
            self.profiles['pH'][idx_j] = res

    def add_partition_equilibrium(self, aq, gas, Hcc):
        """ For partition reactions between 2 species

        Args:
            aq (string): name of aquatic species
            gas (string): name of gaseous species
            Hcc (double): Henry Law Constant
        """
        self.henry_law_equations.append({'aq': aq, 'gas': gas, 'Hcc': Hcc})

    def henry_equilibrium(self, aq, gas, Hcc):
        """ For partition reactions between 2 species

        Args:
            aq (string): name of aquatic species
            gas (string): name of gaseous species
            Hcc (double): Henry Law Constant
        """
        self.add_partition_equilibrium(aq, gas, Hcc)

    def add_ion(self, name, charge):
        """add non-dissociative ion in acid-base system

        Arguments:
            name {str} -- name of the chemical element
            charge {float} -- charge of chemical element
        """

        ion = phcalc.Neutral(charge=charge, conc=np.nan)
        self.acid_base_components.append({
            'species': [name],
            'pH_object': ion
        })

    def add_acid(self, species, pKa, charge=0):
        """add acid in acid-base system

        Arguments:
            species {list} -- list of species, e.g. ['H3PO4', 'H2PO4', 'HPO4', 'PO4']
            pKa {list} -- list of floats with pKs, e.g. [2.148, 7.198, 12.375]

        Keyword Arguments:
            charge {float} -- highest charge in the acid  (default: {0})
        """

        acid = phcalc.Acid(pKa=pKa, charge=charge, conc=np.nan)
        self.acid_base_components.append({
            'species': species,
            'pH_object': acid
        })

    def acid_base_equilibrium_solve(self, i):
        """solves acid-base equilibrium equations

        Arguments:
            i {int} -- step in time
        """

        self.acid_base_solve_ph(i)
        self.acid_base_update_concentrations(i)

    def init_rates_arrays(self):
        """allocates zero matrices for rates
        """

        for rate in self.rates:
            self.estimated_rates[rate] = np.zeros((self.N, self.time.size))

    def create_dynamic_functions(self):
        """create strings of dynamic functions for scipy solver and later execute
        them using exec(), potentially not safe but haven't found better approach yet.
        """

        fun_str = desolver.create_ode_function(
            self.species, self.functions, self.constants, self.rates, self.dcdt)
        exec(fun_str)
        self.dynamic_functions['dydt_str'] = fun_str
        self.dynamic_functions['dydt'] = locals()['f']
        self.dynamic_functions['solver'] = desolver.create_solver(locals()['f'])

    def reset(self):
        """resets the solution for re-run
        """
        for element in self.species:
            self.profiles[element] = self.species[element]['concentration'][:,
                                                                            0]

    def pre_run_methods(self):
        """pre-run before solve
        initiates acid-base system and creates dynamic functions (strings of ODE)
        for reaction solver
        """
        self.add_time_variable()
        if len(self.acid_base_components) > 0:
            self.create_acid_base_system()
            self.acid_base_equilibrium_solve(0)
        if self.ode_method is 'scipy':
            self.create_dynamic_functions()
        self.init_rates_arrays()

    def change_concentration_profile(self, element, i, new_profile):
        """change concentration in profile vectors

        Arguments:
            element {str} -- name of the element
            i {int} -- step in time
            new_profile {np.array} -- vector of new concetrations
        """

        self.profiles[element] = new_profile
        self.update_matrices_due_to_bc(element, i)

    def reactions_integrate_scipy(self, i):
        """integrates ODE of reactions

        Arguments:
            i {int} -- step in time
        """

        # C_new, rates_per_elem, rates_per_rate = desolver.ode_integrate(self.profiles, self.dcdt, self.rates, self.constants, self.dt, solver='rk4')
        # C_new, rates_per_elem = desolver.ode_integrate(self.profiles, self.dcdt, self.rates, self.constants, self.dt, solver='rk4')
        # for idx_j in range(self.N):
        for idx_j in range(self.N):
            yinit = np.zeros(len(self.species))
            for idx, s in enumerate(self.species):
                yinit[idx] = self.profiles[s][idx_j]

            ynew = desolver.ode_integrate_scipy(
                self.dynamic_functions['solver'], yinit, self.dt)

            for idx, s in enumerate(self.species):
                self.species[s]['concentration'][idx_j, i] = ynew[idx]

        for element in self.species:
            self.profiles[element] = self.species[element]['concentration'][:,
                                                                            i]
            if self.species[element]['int_transport']:
                self.update_matrices_due_to_bc(element, i)

    def reconstruct_rates(self):
        """reconstructs rates after model run
        1. estimates rates;
        2. estimates changes of concentrations
        not sure if it works with dynamic functions of "scipy",
        only with rk4 and butcher 5?
        """
        if self.ode_method == 'scipy':
            rates_str = desolver.create_rate_function(
                self.species, self.functions, self.constants, self.rates,
                self.dcdt)
            exec(rates_str, globals())
            self.dynamic_functions['rates_str'] = rates_str
            # from IPython.core.debugger import set_trace
            # set_trace()
            self.dynamic_functions['rates'] = globals()['rates']
            yinit = np.zeros(len(self.species))

            for idx_t in range(len(self.time)):
                for idx_j in range(self.N):
                    for idx, s in enumerate(self.species):
                        yinit[idx] = self.species[s]['concentration'][idx_j,
                                                                      idx_t]

                    rates = self.dynamic_functions['rates'](yinit)

                    for idx, r in enumerate(self.rates):
                        self.estimated_rates[r][idx_j, idx_t] = rates[idx]
        else:
            for idx_t in range(len(self.time)):
                for name, rate in self.rates.items():
                    conc = {}
                    for spc in self.species:
                        conc[spc] = self.species[spc]['concentration'][:, idx_t]
                    r = ne.evaluate(rate, {**self.constants, **conc})
                    self.estimated_rates[name][:, idx_t] = r * (r > 0)

        for spc in self.species:
            self.species[spc]['rates'] = (
                self.species[spc]['concentration'][:, 1:] -
                self.species[spc]['concentration'][:, :-1]) / self.dt
