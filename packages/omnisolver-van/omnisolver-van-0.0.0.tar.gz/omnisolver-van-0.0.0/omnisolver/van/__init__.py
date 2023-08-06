"""Package with Variational Autoregressive Network sampler"""
from typing import Tuple

from omnisolver.plugin import sampler_spec_impl


@sampler_spec_impl
def get_specification_resource() -> Tuple[str, str]:
    """Get package name and resource path."""
    return "omnisolver.van", "van.yml"
