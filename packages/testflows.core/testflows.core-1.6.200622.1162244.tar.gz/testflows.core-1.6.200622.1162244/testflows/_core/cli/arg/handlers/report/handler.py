# Copyright 2019 Katteli Inc.
# TestFlows Test Framework (http://testflows.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from testflows._core.cli.arg.common import epilog
from testflows._core.cli.arg.common import HelpFormatter
from testflows._core.cli.arg.handlers.handler import Handler as HandlerBase
from testflows._core.cli.arg.handlers.report.srs_coverage import Handler as srs_coverage_handler
from testflows._core.cli.arg.handlers.report.passing import Handler as passing_handler
from testflows._core.cli.arg.handlers.report.totals import Handler as totals_handler
from testflows._core.cli.arg.handlers.report.fails import Handler as fails_handler
from testflows._core.cli.arg.handlers.report.version import Handler as version_handler
from testflows._core.cli.arg.handlers.report.official import Handler as official_handler
from testflows._core.cli.arg.handlers.report.compare.handler import Handler as compare_handler
from testflows._core.cli.arg.handlers.report.requirements import Handler as requirements_handler
from testflows._core.cli.arg.handlers.report.map.handler import Handler as map_handler

class Handler(HandlerBase):
    @classmethod
    def add_command(cls, commands):
        parser = commands.add_parser("report", help="generate report", epilog=epilog(),
            description="Generate report.",
            formatter_class=HelpFormatter)

        report_commands = parser.add_subparsers(title="commands", metavar="command",
            description=None, help=None)
        report_commands.required = True
        official_handler.add_command(report_commands)
        compare_handler.add_command(report_commands)
        totals_handler.add_command(report_commands)
        passing_handler.add_command(report_commands)
        fails_handler.add_command(report_commands)
        version_handler.add_command(report_commands)
        requirements_handler.add_command(report_commands)
        srs_coverage_handler.add_command(report_commands)
        map_handler.add_command(report_commands)
