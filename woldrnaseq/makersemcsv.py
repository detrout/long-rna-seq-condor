#!/usr/bin/python3
import argparse
import logging

from woldrnaseq import models
from woldrnaseq import madqc

logger = logging.getLogger('RSEM CSV')

def main(cmdline=None):
    parser = make_parser()
    args = parser.parse_args(cmdline)

    logging.basicConfig(level=logging.INFO)

    sep = models.get_seperator(args.sep)
    experiments = models.load_experiments([args.experiments], sep=sep)
    libraries = models.load_library_tables([args.libraries], sep=sep)

    output_sep = models.get_seperator(args.output_format)
    output_extension = {
        'TAB': '.tsv',
        ',': '.csv',
    }[args.output_format]

    for name in experiments:
        filename = name + '_' + args.quantification + output_extension
        replicates = experiments[name]
        logger.info("%s %s: %s",
                    name, args.quantification, ','.join(replicates))
        quantifications = madqc.load_replicates(
            replicates, libraries, args.quantification)
        quantifications.to_csv(filename, sep=output_sep)

def make_parser():
    parser = argparse.ArgumentParser(
        description="Write combined CSV for a specific quantification.")
    parser.add_argument('-q', '--quantification',
                        choices=['FPKM', 'TPM', 'expected_count',
                                 'effective_length', 'length'],
                        default='FPKM',
                        help='which quantification value to use')
    parser.add_argument('-l', '--libraries', help='library information table')
    parser.add_argument('-e', '--experiments', help='experiment information table')
    parser.add_argument('-s', '--sep', choices=['TAB', ','], default='TAB')
    parser.add_argument('--output-format', choices=['TAB', ','], default=',')
    return parser

if __name__ == '__main__':
    main()