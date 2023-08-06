# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 22:49:17 2020

@author: yrc2
"""
from .iterative_solvers import wegstein, aitken
from .profiler import Profiler
from numba import njit

__all__ = ('Problem',)

fixedpoint_solvers = [wegstein, aitken]

class Problem:
    __slots__ = ('f', 'cases', '_f_fixedpoint_jit')
    
    def __init__(self, f, cases):
        self.f = f
        self.cases = cases
        self._f_fixedpoint_jit = None
    
    @property
    def name(self):
        return self.f.__name__.capitalize().replace('_', ' ')
        
    def test(self, x, tol, args=()): 
        assert abs(self.f(x, *args)) <= tol, "result not within tolerance"
        
    def f_fixedpoint(self, x, *args):
        return self.f(x, *args) + x
    
    @property
    def f_fixedpoint_jit(self):
        f_fixedpoint_jit = self._f_fixedpoint_jit
        if f_fixedpoint_jit: return f_fixedpoint_jit
        f = self.f
        @njit
        def f_fixedpoint_jit(x):
            return f(x) + x
        self._f_fixedpoint_jit = f_fixedpoint_jit
        return f_fixedpoint_jit

    
    def profile_solver(self, solver, ytol, kwargs={}):
        f = self.f_fixedpoint if solver in fixedpoint_solvers else self.f
        p = Profiler(f)
        for case in self.cases:
            try: 
                x = solver(p, 0., **kwargs)
                self.test(x, ytol, kwargs.get('args', ()))
            except: 
                p.archive_case(case, failed=True)
            else:
                p.archive_case(case)
        return p
    
    def __repr__(self):
        return f"{type(self).__name__}(f={self.f}, cases={self.cases})"
    
    def _ipython_display_(self):
        print(f"{type(self).__name__}: {self.name}\n"
              f" cases: {self.cases}")