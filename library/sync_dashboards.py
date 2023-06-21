#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2021-2023, Bodo Schulz <bodo@boone-schulz.de>
# Apache-2.0 (see LICENSE or https://opensource.org/license/apache-2-0)
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import, division, print_function
import os
import logging
import collections
import re
import dirsync

from ansible.module_utils.basic import AnsibleModule


class TailLogHandler(logging.Handler):

    def __init__(self, log_queue):
        logging.Handler.__init__(self)
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.append(self.format(record))


class TailLogger(object):

    def __init__(self, maxlen):
        self._log_queue = collections.deque(maxlen=maxlen)
        self._log_handler = TailLogHandler(self._log_queue)

    def contents(self):
        return '\n'.join(self._log_queue)

    @property
    def log_handler(self):
        return self._log_handler


class Sync(object):
    """
    """

    def __init__(self, module):
        """
        """
        self.module = module

        self.source_directory = module.params.get("source_directory")
        self.destination_directory = module.params.get("destination_directory")

    def run(self):
        """
        """
        result = dict(
            changed=False,
            failed=True,
            msg="initial"
        )

        tail = TailLogger(2)

        logger = logging.getLogger('dirsync')
        formatter = logging.Formatter('%(message)s')

        log_handler = tail.log_handler
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        logger.setLevel(logging.DEBUG)

        include_pattern = ('^.*\\.json$',)

        if os.path.isdir(self.source_directory):

            args = {
                'create': 'False',
                'verbose': 'False',
                'purge': 'True',
                'include': include_pattern,
                'logger': logger,
            }

            dirsync.sync(self.source_directory, self.destination_directory, 'sync', **args)

            result['failed'] = False
            result['msg'] = "The directories were successfully synchronised."

        log_contents = tail.contents()

        # self.module.log(msg=f"len: {len(log_contents)}")
        # self.module.log(msg=f"log: {log_contents}")

        if len(log_contents) > 0:
            pattern = re.compile(r"(?P<directories_parsed>\d+).*directories parsed, (?P<files_copied>\d+) files copied")

            re_result = re.search(pattern, log_contents)

            files_copied = re_result.group('files_copied')

            if files_copied:
                if int(files_copied) == 0:
                    result['changed'] = False
                    result['msg'] = "The directories are synchronous."
                elif int(files_copied) > 0:
                    result['changed'] = True
                    result['msg'] = "The directories were successfully synchronised."

        return result

# ===========================================
# Module execution.


def main():
    """
    """
    args = dict(
        source_directory = dict(
            required=True,
            type='str'
        ),
        destination_directory=dict(
            required=True,
            type='str'
        ),
    )

    module = AnsibleModule(
        argument_spec=args,
        supports_check_mode=True,
    )

    p = Sync(module)
    result = p.run()

    module.log(msg=f"= result: {result}")
    module.exit_json(**result)


if __name__ == '__main__':
    main()
