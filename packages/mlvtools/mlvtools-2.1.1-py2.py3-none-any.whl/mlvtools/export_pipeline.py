#!/usr/bin/env python3
import argparse
import glob
import logging
from collections import namedtuple
from os.path import abspath, join, exists
from os.path import realpath, dirname
from typing import List

from mlvtools.cmd import CommandHelper, ArgumentBuilder
from mlvtools.exception import MlVToolException
from mlvtools.helper import write_template
from mlvtools.mlv_dvc.dvc_parser import get_dvc_dependencies

ARG_IDENTIFIER = '-'

CURRENT_DIR = realpath(dirname(__file__))

PIPELINE_EXPORT_TEMPLATE_NAME = 'pipeline-export.tpl'
ConfigurableCmds = namedtuple('ConfigurableCmds', ('cmds', 'variables'))


def get_dvc_files(dvc_target_file: str) -> List[str]:
    """
        Return the list of potential DVC meta file pipeline step.
        DVC meta files are all located in the same directory for a given pipeline.
        DVC file extension: .dvc
    """
    if not exists(dvc_target_file):
        raise MlVToolException(f'Targeted pipeline metadata step {dvc_target_file} does not exist')
    return glob.glob(join(dirname(dvc_target_file), '*.dvc'))


def export_pipeline(dvc_meta_file: str, output: str, work_dir: str):
    """
     Generate an executable script to run a whole pipeline
    """
    logging.info(f'Export pipeline from step {dvc_meta_file} to {output}')
    logging.debug(f'Work directory {work_dir}')

    ordered_dvc_metas = get_dvc_dependencies(dvc_meta_file, get_dvc_files(dvc_meta_file))

    template_data = {'work_dir': work_dir, 'cmds': [dvc_meta.cmd for dvc_meta in ordered_dvc_metas]}
    logging.debug(f'Template data: {template_data}')

    templates_path = join(CURRENT_DIR, 'templates', PIPELINE_EXPORT_TEMPLATE_NAME)
    write_template(output, templates_path, info=template_data)
    logging.log(logging.WARNING + 1, f'Pipeline successfully exported in {abspath(output)}')


class MlExportPipeline(CommandHelper):
    def run(self, *args, **kwargs):
        args = ArgumentBuilder(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                               description='Export a DVC pipeline to sequential execution.') \
            .add_force_argument() \
            .add_work_dir_argument() \
            .add_argument('--dvc', type=str, required=True, help='DVC targeted pipeline metadata step') \
            .add_argument('-o', '--output', type=str, help='The Python pipeline script output path',
                          required=True) \
            .parse(args)

        self.set_log_level(args)
        work_dir = args.working_directory

        if not args.force and exists(args.output):
            raise MlVToolException(f'Output file {args.output} already exists, use --force option to overwrite it')

        export_pipeline(args.dvc, args.output, work_dir)
