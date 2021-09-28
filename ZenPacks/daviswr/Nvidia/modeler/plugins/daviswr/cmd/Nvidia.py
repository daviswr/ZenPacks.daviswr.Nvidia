""" Models Nvidia GPUs via SSH """

import csv

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

from ZenPacks.daviswr.Nvidia.lib.util import get_unit_value


class Nvidia(CommandPlugin):
    """ Models Nvidia GPUs via SSH """

    relname = 'nvidiaGPUs'
    modname = 'ZenPacks.daviswr.Nvidia.NvidiaGPU'

    fields = [
        'serial',
        'name',
        'vbios_version',
        'memory.total',
        'compute_mode',
        'power.management',
        'power.limit',
        'driver_version',
        'index',
        ]

    commands = [
        '$ZENOTHING;',
        'nvidia-smi',
        '--format=csv',
        '--query-gpu={0}'.format(','.join(fields)),
        ]

    command = ' '.join(commands)

    def process(self, device, results, log):
        """ Generates RelationshipMaps from Command output """

        log.info(
            'Modeler %s processing data for device %s',
            self.name(),
            device.id
            )
        rm = self.relMap()
        gpu_list = list(csv.DictReader(
            results.splitlines(),
            skipinitialspace=True,
            ))

        for gpu in gpu_list:
            dev_map = dict()
            serial = gpu.get('serial', '')

            for key, value in gpu.iteritems():
                key = key.replace('.', '_').split(' ')[0]
                if 'name' == key:
                    key = 'gpu_name'
                # MiB, W, %, etc
                if value[-1] in 'BW%':
                    measure, unit = value.split(' ')
                    # For ease of casting general values later
                    value = str(get_unit_value(measure, unit))
                # [Not Supported], [N/A]
                elif value.startswith('['):
                    value = ''

                if value.isdigit():
                    dev_map[key] = int(value)
                else:
                    try:
                        dev_map[key] = float(value)
                    except ValueError:
                        dev_map[key] = value

            if serial and 'index' in dev_map:
                dev_map['id'] = self.prepId('GPU_{0}'.format(serial))
                dev_map['serial'] = serial
                dev_map['title'] = 'GPU {0}: {1}'.format(
                    dev_map['index'],
                    dev_map.get('gpu_name', '')
                    )
                rm.append(ObjectMap(
                    modname=self.modname,
                    data=dev_map
                    ))

        log.debug('%s RelMap:\n%s', self.name(), str(rm))
        return rm
