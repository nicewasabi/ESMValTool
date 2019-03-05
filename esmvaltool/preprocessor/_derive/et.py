"""Derivation of variable `et`."""

import cf_units
from iris import Constraint

from ._derived_variable_base import DerivedVariableBase

# Constants
LATENT_HEAT_VAPORIZATION = 2.465E6


class DerivedVariable(DerivedVariableBase):
    """Derivation of variable `et`."""

    # Required variables
    _required_variables = {
        'vars': [{
            'short_name': 'hfls',
            'field': 'T2{frequency}s'
        }]
    }

    def calculate(self, cubes):
        """Compute evapotranspiration."""
        hfls_cube = cubes.extract_strict(
            Constraint(name='surface_upward_latent_heat_flux'))

        et_cube = hfls_cube * 24.0 * 3600.0 / LATENT_HEAT_VAPORIZATION
        et_cube.units = cf_units.Unit('mm day^-1')

        return et_cube