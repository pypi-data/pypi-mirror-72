import argparse
import re

from typing import Union


def pos_int(value: str) -> int:
    """ Positive int value not including 0"""
    error_msg = f"{value} is an invalid positive int value"
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(error_msg)
    else:
        if int_value <= 0:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            return int_value


def neg_int(value: str) -> int:
    """ Negative int value not including 0 """
    error_msg = f"{value} is an invalid negative int value"
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(error_msg)
    else:
        if int_value >= 0:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            return int_value


def zero_int(value: str) -> int:
    """ Zero int value. """
    # will allow a string with multiple zeroes to work and return
    # in single int 0.  Not sure if this should be.
    error_msg = f"{value} is an invalid zero int value"
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(error_msg)
    else:
        if int_value != 0:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            return int_value


def pos_float(value: str) -> float:
    """ Positive float value not including 0 """
    error_msg = f"{value} is an invalid positive float"
    if value.isdigit():
        raise argparse.ArgumentTypeError(error_msg)
    else:
        try:
            float_value = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if float_value <= 0.0:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return float_value


def neg_float(value: str) -> float:
    """ Negative float value not including 0 """
    error_msg = f"{value} is an invalid negative float"
    if value.isdigit() or value.find(".") == -1:
        raise argparse.ArgumentTypeError(error_msg)
    else:
        try:
            float_value = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if float_value >= 0.0:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return float_value


def zero_float(value: str) -> float:
    """ Zero float value """
    error_msg = f"{value} is an invalid zero float"
    if value.isdigit() or value.find(".") == -1:
        raise argparse.ArgumentTypeError(error_msg)
    else:
        try:
            float_value = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if float_value != 0.0:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return float_value


def int_float(value: str) -> Union[int, float]:
    """ Any int or float number"""
    error_msg = f"{value} is invalid int or float"
    try:
        int_value = int(value)
        return int_value
    except ValueError:
        try:
            float_value = float(value)
            return float_value
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)


def bool_none(value: str) -> Union[bool, None]:
    """ String True, False or None and return types bool or None."""
    error_msg = f"{value} is an invalid bool or none"
    if value == "True":
        return True
    elif value == "False":
        return False
    elif value == "None":
        return None
    else:
        raise argparse.ArgumentTypeError(error_msg)


def ip4(value: str) -> str:
    """
    ip address 0.0.0.0 to 255.255.255.255. raises error if
    port is given too.
    """
    error_msg = f"{value} is an invalid ip4 address"
    ip4_re = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)"
                        "{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    if ip4_re.match(value):
        return value
    else:
        raise argparse.ArgumentTypeError(error_msg)


if __name__ == "__main__":
    pass
