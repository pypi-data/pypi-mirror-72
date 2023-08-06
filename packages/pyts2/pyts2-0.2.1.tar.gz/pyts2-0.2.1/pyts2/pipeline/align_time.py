# Copyright (c) 2018 Gareth Dunstone <gareth.dunstone@anu.edu.au>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .base import PipelineStep
from datetime_truncate import truncate


class TruncateTimeStep(PipelineStep):

    def __init__(self, truncate_to='5_minute'):
        self.truncate_to = truncate_to

    def process_file(self, file):
        file.instant.datetime = truncate(file.instant.datetime, self.truncate_to)
        return file
