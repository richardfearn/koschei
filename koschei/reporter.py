#!/usr/bin/python
# Copyright (C) 2014  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Author: Michael Simacek <msimacek@redhat.com>

import os

from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from koschei import models, submitter

jinja_env = Environment(loader=FileSystemLoader('./report-templates'))

def date_filter(date):
    return date.strftime("%x %X")

jinja_env.filters['date'] = date_filter

def installed_pkgs_from_log(root_log):
    with open(root_log) as log:
        pkgs = []
        lines = log.read().split('\n')
        i = 0
        while i < len(lines):
            if lines[i].endswith('Installed packages:'):
                # skip debug out
                i += 2
                break
            i += 1
        if i >= len(lines):
            return
        while i < len(lines):
            if 'Child return code was:' in lines[i]:
                break
            pkgs.append(lines[i].split()[-1])
            i += 1
        return pkgs

def log_diff(session, build1, build2):
    logdir1 = os.path.join(submitter.log_output_dir, str(build1.id))
    logdir2 = os.path.join(submitter.log_output_dir, str(build2.id))
    logdiffs = {}
    for arch in os.listdir(logdir1):
        pkgs1 = set(installed_pkgs_from_log(os.path.join(logdir1, arch, 'root.log')))
        pkgs2 = set(installed_pkgs_from_log(os.path.join(logdir2, arch, 'root.log')))
        if arch == 'noarch':
            pkgs1 = {'.'.join(pkg.split('.')[:-1]) for pkg in pkgs1}
            pkgs2 = {'.'.join(pkg.split('.')[:-1]) for pkg in pkgs2}
        diff = ['+ {}'.format(pkg) for pkg in pkgs1.difference(pkgs2)]
        diff += ['- {}'.format(pkg) for pkg in pkgs2.difference(pkgs1)]
        logdiffs[arch] = sorted(diff, key=lambda x: x[1:])
    return logdiffs

def generate_report(template, since, until):
    session = models.Session()
    template = jinja_env.get_template(template)
    packages = session.query(models.Package).filter_by(watched=True)\
               .order_by(models.Package.id).all()
    return template.render(packages=packages, since=since, until=until, models=models,
                           log_diff=lambda b1, b2: log_diff(session, b1, b2))

if __name__ == '__main__':
    since = datetime.min
    until = datetime.now()
    print generate_report('base-report.html', since, until)