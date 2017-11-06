# -*- coding: utf-8 -*-

from __future__ import division, print_function

import numpy as np
from .red_blue import RedBlueMove

__all__ = ["DESnookerMove"]


class DESnookerMove(RedBlueMove):
    """A snooker proposal using differential evolution.

    Based on `Ter Braak & Vrugt (2008)
    <http://link.springer.com/article/10.1007/s11222-008-9104-9>`_.

    Credit goes to GitHub user `mdanthony17 <https://github.com/mdanthony17>`_
    for proposing this as an addition to the original emcee package.

    Args:
        gammas (Optional[float]): The mean stretch factor for the proposal
            vector. By default, it is :math:`1.7` as recommended by the
            reference.

    """
    def __init__(self, gammas=1.7, **kwargs):
        self.gammas = gammas
        kwargs["nsplits"] = 4
        super(DESnookerMove, self).__init__(**kwargs)

    def get_proposal(self, s, c, random):
        Ns = len(s)
        Nc = list(map(len, c))
        ndim = s.shape[1]
        q = np.empty((Ns, ndim), dtype=np.float64)
        metropolis = np.empty(Ns, dtype=np.float64)
        for i in range(Ns):
            z = c[0][random.randint(Nc[0])]
            z1 = c[1][random.randint(Nc[1])]
            z2 = c[2][random.randint(Nc[2])]
            delta = s[i] - z
            norm = np.linalg.norm(delta)
            u = delta / np.sqrt(norm)
            q[i] = s[i] + u * self.gammas * (np.dot(u, z1) - np.dot(u, z2))
            metropolis[i] = np.log(np.linalg.norm(q[i]-z)) - np.log(norm)
        return q, 0.5 * (ndim - 1.0) * metropolis
