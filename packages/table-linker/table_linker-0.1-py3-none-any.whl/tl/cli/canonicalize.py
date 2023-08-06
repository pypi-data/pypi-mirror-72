import sys
import argparse
import traceback
import tl.exceptions


def parser():
    return {
        'help': 'translate an input CSV or TSV file to canonical form'
    }


def add_arguments(parser):
    """
    Parse Arguments
    Args:
        parser: (argparse.ArgumentParser)

    """
    parser.add_argument('-c', '--columns', action='store', type=str, dest='columns', required=True,
                        help='the columns in the input file to be linked to KG entities. Multiple columns'
                             ' are specified as a comma separated string.')
    parser.add_argument('-o', '--output-column', action='store', type=str, dest='output_column', default='label')
    parser.add_argument('--tsv', action='store', type=str, dest='csv')
    parser.add_argument('--csv', action='store', type=str, dest='tsv')

    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)


def run(**kwargs):
    from tl.preprocess import preprocess
    import pandas as pd

    file_type = 'tsv' if kwargs['tsv'] else 'csv'
    try:
        df = pd.read_csv(kwargs['input_file'], dtype=object)

        odf = preprocess.canonicalize(kwargs['columns'], output_column=kwargs['output_column'], df=df,
                                      file_type=file_type)
        odf.to_csv(sys.stdout, index=False)
    except:
        message = 'Command: canonicalize\n'
        message += 'Error Message:  {}\n'.format(traceback.format_exc())
        raise tl.exceptions.TLException(message)
