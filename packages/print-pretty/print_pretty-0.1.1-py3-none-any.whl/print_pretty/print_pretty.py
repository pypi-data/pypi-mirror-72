
from input_util import I
from print_dict import print_dict


def print_pretty(arg):

    if I(arg).is_dict:
        print_dict(arg)

    else:
        raise NotImplementedError

    return True

