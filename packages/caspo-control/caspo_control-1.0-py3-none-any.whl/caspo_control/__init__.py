"""
This Python module provides a simple wrapper for the *control* method of the
tool `caspo <https://bioasp.github.io/caspo/>`_, which implements the
computation of intervention strategies in logical signaling networks with
Answer-Set Programming (https://doi.org/10.1017/S1471068413000422).

The control predictions can be processed using the `algorecell_types
<https://github.com/algorecell/algorecell_types>`_ library, which eases the
display and comparison with other control methods.

Installation instructions at https://github.com/algorecell/caspo-control.

Examples can be found at:
    - https://nbviewer.jupyter.org/github/algorecell/caspo-control/tree/master/examples/

Quick usage:

>>> import caspo_control

Model loading:

>>> cc = caspo_control.load("model.bnet") # in BoolNet format
# alternatively, load with biolqm in any format
>>> lm = biolqm.load("model.zginml") # or any format support by bioLQM
>>> cc = caspo_control.load(lm)

Reprogramming predictions:

>>> rs = cc.reprogramming_to_attractor({"A": 1, "B": 0})
>>> rs

See ``help(rs)`` for other display methods

"""

from .iface import caspo_control

from colomoto.types import PartialState
from algorecell_types import *

from colomoto.minibn import BooleanNetwork

class CaspoControl(object):
    """
    Wrapper for the `caspo control` method.
    """
    def __init__(self, bn, fixed={}):
        """
        :param bn: Boolean network in any format supported by
            ``colomoto.minibn.BooleanNetwork``, which includes filename in BoolNet
            format, and ``biolqm`` or ``ginsim`` objects.
        :keyword dict[str,int] fixed: fix the given nodes to their associated given values
        """
        self.bn = BooleanNetwork.auto_cast(bn)
        self.fixed = fixed

    def reprogramming_to_attractor(self, *goal_spec,
            exclude_goal=False, maxsize=0, **goal_kwspec):
        """
        Compute reprogramming strategies ensuring that all the attractors of the
        perturbed network match with the given specification with the
        (general) asynchronous mode.
        The perturbations are permanent, and can change the attractors of the
        input model.

        :keyword bool exclude_goal: Whenever ``True``, skip solutions
            controlling the nodes specified for the reprogramming goal (default: ``False``)
        :keyword int maxsize: maximum number of simultaneous perturbations
            (default: ``0``, unlimited)
        :rtype: `algorecell_types.ReprogrammingStrategies <https://algorecell-types.readthedocs.io/#algorecell_types.ReprogrammingStrategies>`_

        Examples:

        >>> rs = cc.reprogramming_to_attractor(A=1, B=0)
        >>> rs = cc.reprogramming_to_attractor({"A": 1, "B": 0})
        """
        goal = PartialState(*goal_spec, **goal_kwspec)
        interventions = caspo_control(self.bn, goal, self.fixed,
                allow_goal_intervention=not exclude_goal,
                maxsize=maxsize)
        strategies = ReprogrammingStrategies()
        for control in interventions:
            p = PermanentPerturbation(control)
            st = FromCondition("input", p) if self.fixed else FromAny(p)
            strategies.add(st)
        if self.fixed:
            strategies.register_alias("input", self.fixed)
        return strategies

def load(bn, fixed={}):
    """
    Returns :py:class:`.CaspoControl` `(bn, fixed)` object
    """
    return CaspoControl(bn, fixed)

