import argparse
import os
from datetime import datetime

from asreview.entry_points import BaseEntryPoint

from asreviewcontrib.postprocess.keywords import extract_keywords


class KeywordsEntryPoint(BaseEntryPoint):
    description = "Extracting keywords from the title and abstract of the record"
    extension_name = "asreview-postprocess"

    @property
    def version(self):
        from asreviewcontrib.postprocess.__init__ import __version__
        return __version__

    def execute(self, argv):
        parser = argparse.ArgumentParser(prog='asreview keywords')

        parser.add_argument('asreview_files',
                            metavar='asreview_files',
                            type=str,
                            nargs='+',
                            help='A (list of) ASReview files')
        
        parser.add_argument(
            "-m",
            "--method",
            dest="method",
            default="tf-idf",
            help='Method for extracting keywords (default = tf-idf)'
        )

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
        
        if len(args.asreview_files) > 1:
            raise ValueError("Extracting keywords from multiple project files"
                             " via the CLI is not supported yet.")
            
        asreview_filename = args.asreview_files[0]
            
        if args.outputfile_name:
            outputfile_name = args.outputfile_name
            if not outputfile_name.endswith('.csv'):
                if '.' in outputfile_name:
                    raise ValueError("File extensions other than .csv are not supported yet")
                else:
                    outputfile_name += '.csv'
        else:
            outputfile_name = os.path.basename(asreview_filename)
            outputfile_name = f"{os.path.splitext(outputfile_name)[0]}-with-keywords-{datetime.now().strftime('%Y%m%dT%H%M')}.csv"
                
        extract_keywords(
            asreview_filename=asreview_filename,
            outputfile_name=outputfile_name,
            method=args.method
        )
