#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`orion.core.cli.db.rm` -- Module running the rm command
============================================================

.. module:: setup
   :platform: Unix
   :synopsis: Delete experiments and trials from the database
"""
import argparse
import logging
import os
import sys

import yaml

import orion.core
import orion.core.io.experiment_builder as experiment_builder
from orion.core.utils.pptree import print_tree

log = logging.getLogger(__name__)


EXP_RM_MESSAGE = """
All experiments above and their corresponding trials will be deleted.
To select a specific version use --version <VERSION>. Note that all
children of a given version will be deleted. Oríon cannot delete a
parent experiment without deleting the children.
To delete trials only, use --status <STATUS>.

Make sure to stop any worker currently executing one of these experiment.

To proceed, type again the name of the experiment: """


TRIALS_RM_MESSAGE = """
Matching trials of all experiments above will be deleted.
To select a specific version use --version <VERSION>. Note that all
children of a given version will be deleted. Oríon cannot delete a
parent experiment without deleting the children.

Make sure to stop any worker currently executing one of these experiment.

To proceed, type again the name of the experiment: """



def add_subparser(parser):
    """Return the parser that needs to be used for this command"""
    # TODO: Document parser
    # Remove experiment, all its childrens and all corresponding trials.
    # Supports regex
    # If --status is used, only delete the trials matching the given status and experiments is kept
    rm_parser = parser.add_parser(
        'rm', 
        help='rm help')

    rm_parser.set_defaults(func=main)

    # rm_parser.add_argument(
    #     'type',
    #     help='`exp` to delete experiments and trials, `trial` to delete trials only')

    rm_parser.add_argument(
        'name',
        help='Name of the experiment to delete. Also supports regex.')

    rm_parser.add_argument('-c', '--config', type=argparse.FileType('r'),
                           metavar='path-to-config', help="user provided "
                           "orion configuration file")

    rm_parser.add_argument(
        '-v', '--version', type=int, default=1,
        help="specific version of experiment to fetch; "
             "(default: root experiment matching.)")

    rm_parser.add_argument(
        '-s', '--status',
        help='Name of the experiment to delete. Also supports regex.')


    return rm_parser


def confirm_name(message, name):
    """Ask the user to confirm the name.

    Parameters
    ----------
    message: str
        The message to be printed.
    name: str
        The string that the user must enter.

    Returns
    -------
    bool 
        True if confirmed, False otherwise.

    """
    answer = input(message)

    return answer.strip() == name


def process_trial_rm(root, status):
    for node in root:
        if status == '*':
            query = {}
        else:
            query = {'status': status}

        # TODO: Delete in batch for exp.id
        # print(node.item.fetch_trials(with_evc_tree=False))

        # NOTE: Storage does not support deletion...

        # TODO: Give count of deleted experiments


def process_exp_rm(root):
    for node in root:
        print(node)


def delete_experiments(root, args):
    confirmed = confirm_name(EXP_RM_MESSAGE, args['name'])

    if not confirmed:
        print('Confirmation failed, aborting operation.')
        sys.exit(1)

    process_trial_rm(root, '*')
    process_exp_rm(root)


def delete_trials(root, args):
    confirmed = confirm_name(TRIALS_RM_MESSAGE, args['name'])

    if not confirmed:
        print('Confirmation failed, aborting operation.')
        sys.exit(1)

    process_trial_rm(root, args['status'])


# pylint: disable = unused-argument
def main(args):
    """Remove the experiment(s) or trial(s)."""
    config = experiment_builder.get_cmd_config(args)
    experiment_builder.setup_storage(config.get('storage'))

    # Find root experiment
    root = experiment_builder.build_view(name=args['name'],
                                         version=args.get('version', 1)).node

    # List all experiments with children
    print_tree(root, nameattr='tree_name')

    if args['status']:
        delete_trials(root, args)
    else:
        delete_experiments(root, args)

    # First delete all trials

    # If --status, only delete trials.














# orion db rm exp algo
# orion db rm trial algo --status
# 
# 
# 
# 
# 
# 
# orion db rm algo
# orion db rm algo --status *


# orion db set algo trial.id='' status=''













