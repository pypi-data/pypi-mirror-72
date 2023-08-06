# -*- coding: utf-8 -*-
#
#    Copyright 2020 Ibai Roman
#
#    This file is part of EvoCov.
#
#    EvoCov is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    EvoCov is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with EvoCov. If not, see <http://www.gnu.org/licenses/>.

import time

import numpy as np

from .kernel_fitting_method import KernelFittingMethod

from ..gen_prog_tools import selection


class Random(KernelFittingMethod):
    """

    """

    def __init__(self, obj_fun, max_fun_call=500, dims=1,
                 nested_fit_method=None):

        super(Random, self).__init__(
            obj_fun,
            max_fun_call=max_fun_call,
            dims=dims,
            nested_fit_method=nested_fit_method
        )

        selection.add_selection(
            toolbox=self.toolbox,
            selection_method='best'
        )

    def fit(self, model, folds, budget=None, verbose=False):
        """

        :param model:
        :type model:
        :param folds:
        :type folds:
        :param budget:
        :type budget:
        :param verbose:
        :type verbose:
        :return:
        :rtype:
        """
        if budget is None or self.max_fun_call < budget:
            max_fun_call = self.max_fun_call
        else:
            max_fun_call = budget

        start = time.time()

        best_state = {
            'name': self.__class__.__name__,
            'fun_calls': 0,
            'restarts': 0,
            'time': 0,
            'value': np.inf,
            'creation': 0,
            'evals': 0,
            'id': 0,
            'origin': 0,
            'hp_count': 0,
            'prim_count': 0
        }
        best_state.update(self.save_state(model))
        initial_state = self.save_state(model)

        npop = max_fun_call
        if self.nested_fit_method is not None:
            npop = int(max_fun_call / self.nested_fit_method.max_fun_call)

        population = self.toolbox.random_population(n=npop)
        id_i = 0
        for ind in population:
            ind.log.id = id_i
            id_i += 1

        self.evaluate_population(
            model,
            best_state,
            initial_state,
            max_fun_call,
            folds,
            population,
            verbose=verbose
        )

        best = self.toolbox.select(population, 1)[0]

        end = time.time()

        best_state['value'] = best.fitness.getValues()
        best_state['restarts'] = len(population)
        best_state['state'] = best
        best_state['nested'] = best.nested
        best_state['time'] = end - start
        best_state['creation'] = best.log.creation
        best_state['evals'] = best.log.evals
        best_state['id'] = best.log.id
        best_state['origin'] = best.log.origin
        best_state['hp_count'] = best.log.hp_count
        best_state['prim_count'] = best.log.prim_count

        self.load_state(model, best_state)

        return best_state
