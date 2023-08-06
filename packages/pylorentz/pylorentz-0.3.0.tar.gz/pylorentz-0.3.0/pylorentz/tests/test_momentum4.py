"""
Unittests for the class Momentum4
"""

import unittest
import numpy as np
import cmath
from pylorentz import Momentum4


class Momentum4TestCase(unittest.TestCase):
    """
    Test the implementation of Momentum4.
    """
    def assertListAlmostEqual(self, list_a, list_b, *args, **kwds):
        list_a = list(list_a)
        list_b = list(list_b)
        if len(list_a) != len(list_b):
            self.assertEqual(list_a, list_b)

        for a, b in zip(list_a, list_b):
            self.assertAlmostEqual(a, b, *args, **kwds)


    def test_init(self):
        """
        Check that a instantiation with all four components returns the
        correct vector.
        """
        momentum = Momentum4(100, 2.5, 1.23, 1.777)
        self.assertAlmostEqual(momentum.e, 100)
        self.assertAlmostEqual(momentum.p_x, 2.5)
        self.assertAlmostEqual(momentum.p_y, 1.23)
        self.assertAlmostEqual(momentum.p_z, 1.777)

    def test_init_vectorized(self):
        """
        Check that a instantiation with all four components returns the
        correct numpy vector.
        """
        x1 = np.array([100, 200, 300, 400])
        x2 = np.array([1.5, 2.5, 3.5, 4.5])
        x3 = np.array([1.23]*4)
        x4 = np.array([1.777]*4)
        momentum = Momentum4(x1, x2, x3, x4)

        self.assertListAlmostEqual(momentum.e, [100, 200, 300, 400])
        self.assertListAlmostEqual(momentum.p_x, [1.5, 2.5, 3.5, 4.5])
        self.assertListAlmostEqual(momentum.p_y, [1.23]*4)
        self.assertListAlmostEqual(momentum.p_z, [1.777]*4)

    def test_e_eta_phi_pt_vectorized(self):
        """
        Check that instantiation with e_eta_phi_pt() returns the correct
        object.
        """
        x1 = np.array([100, 200, 300, 400])
        x2 = np.array([1.5, 2.5, 3.5, 4.5])
        x3 = np.array([1.23]*4)
        x4 = np.array([1.777]*4)
        momentum = Momentum4.e_eta_phi_pt(x1, x2, x3, x4)

        self.assertListAlmostEqual(momentum.e, [100, 200, 300, 400])
        self.assertListAlmostEqual(momentum.eta, [1.5, 2.5, 3.5, 4.5])
        self.assertListAlmostEqual(momentum.phi, [1.23]*4)
        self.assertListAlmostEqual(momentum.p_t, [1.777]*4)

        self.assertListAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_e_eta_phi_pt(self):
        """
        Check that instantiation with e_eta_phi_pt() returns the correct
        object.
        """
        momentum = Momentum4.e_eta_phi_pt(100, 2.5, 1.23, 1.777)
        self.assertAlmostEqual(momentum.e, 100)
        self.assertAlmostEqual(momentum.eta, 2.5)
        self.assertAlmostEqual(momentum.phi, 1.23)
        self.assertAlmostEqual(momentum.p_t, 1.777)

        self.assertAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_m_eta_phi_pt(self):
        """
        Check that instantiation with m_eta_phi_pt() returns the correct
        object.
        """
        momentum = Momentum4.m_eta_phi_pt(0.105, 2.5, 1.23, 1.777)
        self.assertAlmostEqual(momentum.m, 0.105)
        self.assertAlmostEqual(momentum.eta, 2.5)
        self.assertAlmostEqual(momentum.phi, 1.23)
        self.assertAlmostEqual(momentum.p_t, 1.777)
        self.assertAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_m_eta_phi_pt_vectorized(self):
        """
        Check that instantiation with m_eta_phi_pt() returns the correct
        object.
        """
        x1 = np.array([0.105, 1.105, 2.105, 3.105])
        x2 = np.array([1.5, 2.5, 3.5, 4.5])
        x3 = np.array([1.23]*4)
        x4 = np.array([1.777]*4)
        momentum = Momentum4.m_eta_phi_pt(x1, x2, x3, x4)

        self.assertListAlmostEqual(momentum.m, np.arange(4) + 0.105)
        self.assertListAlmostEqual(momentum.eta, np.arange(4) + 1.5)
        self.assertListAlmostEqual(momentum.phi, [1.23]*4)
        self.assertListAlmostEqual(momentum.p_t, [1.777]*4)
        self.assertListAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_m_eta_phi_p(self):
        """
        Check that instantiation with m_eta_phi_p() returns the correct
        object.
        """
        momentum = Momentum4.m_eta_phi_p(0.105, 2.5, 1.23, 1.777)
        self.assertAlmostEqual(momentum.m, 0.105)
        self.assertAlmostEqual(momentum.eta, 2.5)
        self.assertAlmostEqual(momentum.phi, 1.23)
        self.assertAlmostEqual(momentum.p, 1.777)
        self.assertAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_m_eta_phi_p_vectorized(self):
        """
        Check that instantiation with m_eta_phi_p() returns the correct
        object.
        """
        x1 = np.array([0.105, 1.105, 2.105, 3.105])
        x2 = np.array([1.5, 2.5, 3.5, 4.5])
        x3 = np.array([1.23]*4)
        x4 = np.array([1.777]*4)
        momentum = Momentum4.m_eta_phi_p(x1, x2, x3, x4)

        self.assertListAlmostEqual(momentum.m, np.arange(4) + 0.105)
        self.assertListAlmostEqual(momentum.eta, np.arange(4) + 1.5)
        self.assertListAlmostEqual(momentum.phi, [1.23]*4)
        self.assertListAlmostEqual(momentum.p, [1.777]*4)
        self.assertListAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_e_eta_phi_p(self):
        """
        Check that instantiation with e_eta_phi_p() returns the correct
        object.
        """
        momentum = Momentum4.e_eta_phi_p(2, 2.5, 1.23, 1.777)
        self.assertAlmostEqual(momentum.e, 2)
        self.assertAlmostEqual(momentum.eta, 2.5)
        self.assertAlmostEqual(momentum.phi, 1.23)
        self.assertAlmostEqual(momentum.p, 1.777)
        self.assertAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_e_eta_phi_p_vectorized(self):
        """
        Check that instantiation with m_eta_phi_p() returns the correct
        object.
        """
        x1 = np.array([0.105, 1.105, 2.105, 3.105])
        x2 = np.array([1.5, 2.5, 3.5, 4.5])
        x3 = np.array([1.23]*4)
        x4 = np.array([1.777]*4)
        momentum = Momentum4.m_eta_phi_p(x1, x2, x3, x4)

        self.assertListAlmostEqual(momentum.m, np.arange(4) + 0.105)
        self.assertListAlmostEqual(momentum.eta, np.arange(4) + 1.5)
        self.assertListAlmostEqual(momentum.phi, [1.23]*4)
        self.assertListAlmostEqual(momentum.p, [1.777]*4)
        self.assertListAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_e_m_eta_phi(self):
        """
        Check that instantiation with e_m_eta_phi() returns the correct
        object.
        """
        momentum = Momentum4.e_m_eta_phi(2, 1.777, 2.5, 1.23)
        self.assertAlmostEqual(momentum.e, 2)
        self.assertAlmostEqual(momentum.eta, 2.5)
        self.assertAlmostEqual(momentum.phi, 1.23)
        self.assertAlmostEqual(momentum.m, 1.777)
        self.assertAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_e_m_eta_phi_vectorized(self):
        """
        Check that instantiation with e_m_eta_phi() returns the correct
        object.
        """
        x1 = np.array([1.5, 2.5, 3.5, 4.5])
        x2 = np.array([0.105, 1.105, 2.105, 3.105])
        x3 = np.array([1.23]*4)
        x4 = np.array([1.777]*4)
        momentum = Momentum4.e_m_eta_phi(x1, x2, x3, x4)

        self.assertListAlmostEqual(momentum.e, np.arange(4) + 1.5)
        self.assertListAlmostEqual(momentum.m, np.arange(4) + 0.105)
        self.assertListAlmostEqual(momentum.eta, [1.23]*4)
        self.assertListAlmostEqual(momentum.phi, [1.777]*4)
        self.assertListAlmostEqual(momentum.e**2, momentum.p**2 + momentum.m**2)

    def test_type_m(self):
        """
        Check that the mass is real valued.
        """
        momentum = Momentum4.e_m_eta_phi(2, 1.777, 2.5, 1.23)
        self.assertIsInstance(momentum.m, float)

    def test_type_m_vectorized(self):
        """
        Check that the mass is real valued.
        """
        x1 = np.array([0.105, 1.105, 2.105, 3.105])
        x2 = np.array([1.5, 2.5, 3.5, 4.5])
        x3 = np.array([1.23]*4)
        x4 = np.array([1.777]*4)
        momentum = Momentum4.e_m_eta_phi(2, 1.777, 2.5, 1.23)
        self.assertEqual(momentum.m.dtype, 'float')
