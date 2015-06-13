import ipdb
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# TO DO: Have plot return an object that can with other, new methods, be used
# to generate new plots -- e.g. with different bins -- without recomputing
# everything from raw data again.


def plot(vals, bins, fmt='{:5.1f}', N=None, with_counts=True, yscale='lin', height=20):
    vals = np.array(vals).astype(float)
    left_tail = vals[(vals < bins[0])]
    right_tail = vals[(vals > bins[-1])]
    vals = vals[(vals >= bins[0]) & (vals <= bins[-1])]
    bin_vals, left_edges, _ = plt.hist(vals, bins=bins)
    if yscale == 'log':
        bin_vals[bin_vals > 0] = np.log2(bin_vals[bin_vals > 0]) + 1
    s = '\n'
    bin_val_max = max(bin_vals)
    max_bar_height = height
    sep = ' - '
    if len(left_tail) > 0:
        s += '<' + str(bins[0]) + ': (' + str(len(left_tail)) + ')\n'
    for i in range(len(left_edges)-1):
        right_edge = fmt.format(left_edges[i+1]) if i < len(left_edges) - 1 else '*'
        prefix = fmt.format(left_edges[i]) + sep + right_edge + ': '
        prefix_length = len(prefix)
        s += prefix
        bar_height = int(max_bar_height * bin_vals[i] / bin_val_max)
        s += '#' * bar_height + ' ' * (max_bar_height - bar_height)
        if with_counts:
            s += ' ' * 2 + '(' + str(bin_vals[i]) + ')'
        s += '\n'
    if len(right_tail) > 0:
        s += '>' + str(bins[-1]) + ': (' + str(len(right_tail)) + ')\n'
    return s

def main(args):
    with open(args.infile, 'rb') as fp:
        vals = []
        for line in fp:
            try:
                vals.append(float(line.strip()))
            except ValueError:
                pass
    bins = args.bins
    v_min = args.min if args.min is not None else min(vals)
    v_max = args.max if args.max is not None else max(vals)
    shown_vals = [v for v in vals if v >= v_min and v <= v_max]
    if bins is None:
        n = args.num_bins
        bins = np.linspace(v_min, v_max, n+1)
    fmt = args.fmt
    if fmt is None:
        if v_max - v_min < len(bins):
            w = max(map(lambda x: len(str(x)), shown_vals)) - 1
            t, p = 'f', 1
        else:
            w = max(map(lambda x: len(str(int(x))), shown_vals)) - 1
            t, p = 'f', 0
        w += p + 1
        fmt = '{:' + str(w) + '.' + str(p) + t + '}'
    kwargs = {
            'fmt': fmt,
            'height': args.height,
            'with_counts': args.with_counts,
            'yscale': args.yscale,
            }
    print plot(vals, bins, **kwargs)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', default='/dev/stdin')
    parser.add_argument('--bins', '-b', nargs='+')
    parser.add_argument('--fmt', '-f', default=None)
    parser.add_argument('--height', type=int, default=50)
    parser.add_argument('--min', '-a', type=float)
    parser.add_argument('--max', '-z', type=float)
    parser.add_argument('--num-bins', '-n', type=int, default=10)
    parser.add_argument('--yscale', '-y', choices=['lin', 'log'], default='lin')
    parser.add_argument('--with-counts', action='store_false')
    args = parser.parse_args()
    main(args)

