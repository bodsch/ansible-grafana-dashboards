#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2021-2023, Bodo Schulz <bodo@boone-schulz.de>
# Apache-2.0 (see LICENSE or https://opensource.org/license/apache-2-0)
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import, division, print_function
import os
import dirsync

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.bodsch.core.plugins.module_utils.directory import create_directory, current_state
# from ansible_collections.bodsch.core.plugins.module_utils.lists import compare_two_lists


class Sync(object):
    """
    """

    def __init__(self, module):
        """
        """
        self.module = module

        self.source_directory = module.params.get("source_directory")
        self.destination_directory = module.params.get("destination_directory")
        self.owner = module.params.get("owner")
        self.group = module.params.get("group")
        self.mode = module.params.get("mode")

    def run(self):
        """
        """
        result = dict(
            changed=False,
            failed=True,
            msg="initial"
        )

        include_pattern = ('^.*\.json$',)

        if os.path.isdir(self.source_directory):
            args = {'create': 'False', 'verbose': 'False', 'purge': 'True', 'include': include_pattern}
            dirsync.sync(self.source_directory, self.destination_directory, 'sync', **args)

            self.module.log(msg=f"= state: {self.module.stdout}")

        # dirsync.sync(self.source_directory, self.destination_directory, 'diff', logger=self.logger)

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
        owner=dict(
            required=False
        ),
        group=dict(
            required=False
        ),
        mode=dict(
            required=False,
            type="str"
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
