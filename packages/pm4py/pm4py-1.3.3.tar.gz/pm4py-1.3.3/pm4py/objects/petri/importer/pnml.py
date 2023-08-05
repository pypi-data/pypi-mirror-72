import functools
import warnings

from pm4py.objects.petri.importer import versions


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


@deprecated
def import_petri_from_string(petri_string):
    """
    Import a Petri net from a string

    Parameters
    ----------
    petri_string
        Petri net expressed as PNML string
    parameters
        Other parameters of the algorithm
    """
    return versions.pnml.import_petri_from_string(petri_string)


@deprecated
def import_net(input_file_path):
    """
    Import a Petri net from a PNML file

    Parameters
    ----------
    input_file_path
        Input file path
    parameters
        Other parameters of the algorithm
    """
    return versions.pnml.import_net(input_file_path)
