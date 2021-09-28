""" Parses performance data from nvidia-smi """

import csv
import re

from Products.ZenRRD.CommandParser import CommandParser
from Products.ZenUtils.Utils import prepId

from ZenPacks.daviswr.Nvidia.lib.util import get_unit_value


class smi(CommandParser):
    """ Parses performance data from nvidia-smi """

    def processResults(self, cmd, result):
        """ Returns metrics from command output """
        components = dict()
        gpu_comp_ids = dict()
        csv_data, proc_data = cmd.result.output.split('+-', 1)

        # CSV-formatted output
        gpu_list = list(csv.DictReader(
            csv_data.splitlines(),
            skipinitialspace=True,
            ))

        for gpu in gpu_list:
            serial = gpu.get('serial', '')
            comp_id = prepId('GPU_{0}'.format(serial))
            components[comp_id] = dict()

            for key, value in gpu.iteritems():
                key = key.strip().replace('.', '_').split(' ')[0]
                value = value.strip()
                # MiB, W, %, etc
                if value[-1] in 'BW%':
                    measure, unit = value.split(' ')
                    # For ease of casting general values later
                    value = str(get_unit_value(measure, unit))
                # [Not Supported], [N/A]
                elif value.startswith('['):
                    continue

                if value.isdigit():
                    components[comp_id][key] = int(value)
                else:
                    try:
                        components[comp_id][key] = float(value)
                    except ValueError:
                        continue

            components[comp_id]['proc_memory'] = 0
            components[comp_id]['proc_count'] = 0

            gpu_comp_ids[components[comp_id].get('index')] = comp_id

        # Processes table
        # Example:
        # |    0   N/A  N/A     45359      C   /usr/bin/zmc                      273MiB |  # noqa
        proc_re = r'\|\s+(?P<id>\d+)\s+.*?(?P<mem>\d+)(?P<unit>\w?i?B)\s+\|[\r\n]'  # noqa
        for match in re.findall(proc_re, proc_data):
            gpu_id, mem, unit = match
            if gpu_id in gpu_comp_ids:
                component = components[gpu_comp_ids[gpu_id]]
                component['proc_memory'] += get_unit_value(mem, unit)
                component['proc_count'] += 1

        for point in cmd.points:
            if point.component in components:
                values = components[point.component]
                if point.id in values:
                    result.values.append((point, values[point.id]))
