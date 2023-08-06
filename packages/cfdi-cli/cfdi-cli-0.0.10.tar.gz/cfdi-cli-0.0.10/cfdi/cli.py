import optparse
import sys
import traceback
from . import get_version
from .CfdiParser import CfdiParser


def main():
    op = optparse.OptionParser(
        usage='usage: %prog Export [options]',
        version='%prog {}'.format(get_version())
    )

    op.add_option("-i", "--infile",
                  dest="infile",
                  help="CFDI's XML file path (default: %default)",
                  default='examples/cfdi33.xml')

    (o, args) = op.parse_args()

    if len(args) > 0:
        print("More Args ({})".format(len(args)))

    try:
        # noinspection SpellCheckingInspection
        cfdi = CfdiParser()
        cfdi.load_xml(o.infile)
        print(cfdi)
    except Exception as e:
        print(e)
        traceback.print_exc(None, sys.stderr)
        sys.exit(2)
