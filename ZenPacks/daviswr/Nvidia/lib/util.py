""" Shared methods for modeler & parser """

multipliers = {
    'B': 1,
    'KiB': 1024,
    'MiB': 1024**2,
    'GiB': 1024**3,
    'TiB': 1024**4,
    'PiB': 1024**5,
    'KB': 1000,
    'MB': 1000**2,
    'GB': 1000**3,
    'TB': 1000**4,
    'PB': 1000**5,
    'W': 1,
    '%': 1,
    }


def get_unit_value(value, unit):
    """ Returns value multiplied by given unit """
    return int(float(value) * multipliers.get(unit, 1))
