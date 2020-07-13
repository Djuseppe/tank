import logging
import argparse
import math
import scipy.integrate as integrate


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('in module %(name)s, in func %(funcName)s, '
                              '%(levelname)-8s: [%(filename)s:%(lineno)d] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
if not len(logger.handlers):
    logger.addHandler(stream_handler)
    logger.propagate = False


def get_segment(r, chord_len):
    alpha = 2 * math.asin(chord_len / 2 / r)
    s = 0.5 * (alpha - math.sin(alpha)) * r ** 2
    return s


def get_circle_intersection(z_h, r_2):
    return math.sqrt(r_2 ** 2 - z_h ** 2)


def get_radius(h, r, offset):
    _r = r - (h + offset)
    return math.sqrt(r ** 2 - _r ** 2)


def get_chord(h, r):
    return get_circle_intersection(r - h, r) * 2


def sphere_func(h: float, r_1: float, r_2: float, offset=740*1e-3):
    chord = get_chord(h, r_2)
    _r = get_radius(h, r_1, offset)
    return get_segment(_r, chord)


def cylinder_func(h, r):
    chord = get_chord(h, r)
    return get_segment(r, chord)


def parse_args():
    parser = argparse.ArgumentParser(description='Calculates tank volume of a tank as integral of a function.')
    parser.add_argument('--height', type=float, required=False,
                        default=1,
                        help='Height of water in the tank [m].')
    return parser.parse_args()


def main(h):
    # r1, r2 = 1, 1.4283 / 2
    r1, r2 = 2540 * 1e-3, 1800 * 1e-3
    sphere = integrate.quad(sphere_func, 0, h, args=(r1, r2))
    print(f'Sphere part volume is {sphere[0]:>19.2f} m\u00b3')

    cylinder_r = 1800 * 1e-3
    cylinder_length = 19_000 * 1e-3
    # print(f'cyl chord = {get_chord(h, cylinder_r):.2f}')
    cylinder_segment = get_segment(cylinder_r, get_chord(h, cylinder_r))
    if h <= cylinder_r:
        cylinder = cylinder_segment
    else:
        cylinder = math.pi * cylinder_r ** 2 - cylinder_segment
    cylinder *= cylinder_length
    print(f'Cylinder part volume is {cylinder:>18.2f} m\u00b3')
    print('-' * 50)
    print(f'Total volume occupied by water is {(sphere[0] * 2 + cylinder):>8.2f} m\u00b3')


if __name__ == '__main__':
    args = parse_args()
    main(args.height)
