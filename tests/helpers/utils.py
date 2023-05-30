import itertools


def _fixture_id(ctx):
    """Helper to get a user friendly test name from the parametrized context."""
    return "-".join(f"{key}:{value}" for key, value in ctx.items())


def is_contained(option, unsupported_options):
    """Checks whether the given options is contained in unsupported_options.

    Args:
        option (set of tuples): option to check.
        unsupported_options (list of set of tuples):

    Returns:
        bool: True, if the given option is included in the unsupported_options.
    """
    for us in unsupported_options:
        return option.intersection(us) == us


def generate_supported_combinations(options, unsupported_combinations):
    """Generate all supported combinations for the given options and unsupported
    combinations.

    Args:
        options (OrderedDict): cookiecutter's choice prompts, and their values.
        unsupported_combinations (list of dict): unsupported combinations of
         the chosen prompts.

    Returns:
        list of dict: all the supported combinations.
    """

    result = []
    unsupported = [set(combi.items()) for combi in unsupported_combinations]
    for values in itertools.product(*options.values()):
        if is_contained(set(zip(options.keys(), values)), unsupported):
            continue
        result.append(dict(zip(options.keys(), values)))
    return result
