import argparse

from asreview.entry_points import BaseEntryPoint

from asreviewcontrib.postprocess import *


class ExportEntryPoint(BaseEntryPoint):
    description = "Postprocessing functions for ASReview"
    extension_name = "asreview-postprocess"

    @property
    def version(self):
        from asreviewcontrib.postprocess.__init__ import __version__
        return __version__

    def execute(self, argv):
        parser = argparse.ArgumentParser(prog='asreview postprocess')

        parser.add_argument('asreview_files',
                            metavar='asreview_files',
                            type=str,
                            nargs='+',
                            help='A (list of) ASReview files')

        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"asreview-notes-export: {self.version}",
        )

        parser.add_argument(
            "-o",
            "--output",
            dest="outputfile_name",
            help='Output file name or path. Currently only .csv files are supported.')

        args = parser.parse_args(argv)
