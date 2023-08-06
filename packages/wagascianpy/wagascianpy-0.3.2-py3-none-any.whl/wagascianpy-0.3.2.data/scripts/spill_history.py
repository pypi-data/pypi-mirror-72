#!python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import os
import sys

import wagascianpy.plotting.detector
import wagascianpy.plotting.marker
import wagascianpy.plotting.parse_args
import wagascianpy.plotting.plotter
import wagascianpy.utils.utils
from wagascianpy.plotting.configuration import Configuration


def spill_history(plotter):
    plotter.template_plotter()


if __name__ == "__main__":

    # Parse shell arguments
    args = wagascianpy.plotting.parse_args.parse_args(sys.argv[1:])

    # Edit the initial configuration
    wagascianpy.plotting.configuration.fill_configuration(args)

    if not os.path.exists(Configuration.plotter_configuration.output_path()):
        wagascianpy.utils.utils.mkdir_p(Configuration.plotter_configuration.output_path())

    markers = wagascianpy.plotting.marker.MarkerTuple(
        run=Configuration.plotter_configuration.run_markers(),
        maintenance=Configuration.plotter_configuration.maintenance_markers(),
        trouble=Configuration.plotter_configuration.trouble_markers())

    output_file_format = os.path.join(Configuration.plotter_configuration.output_path(),
                                      "%s_{name}.pdf" % Configuration.plotter_configuration.output_string())

    topology_str = Configuration.plotter_configuration.topology()
    topology = wagascianpy.plotting.parse_args.parse_plotting_topology(topology_str)

    if Configuration.plotter_configuration.delivered_pot():
        spill_history(
            wagascianpy.plotting.plotter.BsdPotPlotter(
                output_file_path=output_file_format.format(name='bsd_pot_history'),
                bsd_database=Configuration.bsd_database_configuration.bsd_database(),
                bsd_repository=Configuration.bsd_database_configuration.bsd_download_location(),
                wagasci_database=Configuration.wagasci_database_configuration.wagasci_database(),
                t2krun=Configuration.global_configuration.t2krun(),
                start=Configuration.run_select_configuration.start(),
                stop=Configuration.run_select_configuration.stop(),
                enabled_markers=markers,
                save_tfile=Configuration.run_select_configuration.save_tfile()))

    if Configuration.plotter_configuration.accumulated_pot():
        spill_history(wagascianpy.plotting.plotter.WagasciPotPlotter(
            output_file_path=output_file_format.format(name='wagasci_pot_history'),
            bsd_database=Configuration.bsd_database_configuration.bsd_database(),
            bsd_repository=Configuration.bsd_database_configuration.bsd_download_location(),
            wagasci_database=Configuration.wagasci_database_configuration.wagasci_database(),
            wagasci_repository=Configuration.wagasci_database_configuration.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select_configuration.start(),
            stop=Configuration.run_select_configuration.stop(),
            enabled_markers=markers,
            save_tfile=Configuration.run_select_configuration.save_tfile()))

    if Configuration.plotter_configuration.bsd_spill():
        spill_history(wagascianpy.plotting.plotter.BsdSpillPlotter(
            output_file_path=output_file_format.format(name='bsd_spill_history'),
            bsd_database=Configuration.bsd_database_configuration.bsd_database(),
            bsd_repository=Configuration.bsd_database_configuration.bsd_download_location(),
            wagasci_database=Configuration.wagasci_database_configuration.wagasci_database(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select_configuration.start(),
            stop=Configuration.run_select_configuration.stop(),
            enabled_markers=markers,
            save_tfile=Configuration.run_select_configuration.save_tfile()))

    if Configuration.plotter_configuration.wagasci_spill_history():
        spill_history(wagascianpy.plotting.plotter.WagasciSpillHistoryPlotter(
            output_file_path=output_file_format.format(name='wagasci_spill_history'),
            bsd_database=Configuration.bsd_database_configuration.bsd_database(),
            bsd_repository=Configuration.bsd_database_configuration.bsd_download_location(),
            wagasci_database=Configuration.wagasci_database_configuration.wagasci_database(),
            wagasci_repository=Configuration.wagasci_database_configuration.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select_configuration.start(),
            stop=Configuration.run_select_configuration.stop(),
            enabled_markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select_configuration.save_tfile()))

    if Configuration.plotter_configuration.wagasci_fixed_spill():
        spill_history(wagascianpy.plotting.plotter.WagasciFixedSpillPlotter(
            output_file_path=output_file_format.format(name='wagasci_fixed_spill_history'),
            bsd_database=Configuration.bsd_database_configuration.bsd_database(),
            bsd_repository=Configuration.bsd_database_configuration.bsd_download_location(),
            wagasci_database=Configuration.wagasci_database_configuration.wagasci_database(),
            wagasci_repository=Configuration.wagasci_database_configuration.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select_configuration.start(),
            stop=Configuration.run_select_configuration.stop(),
            enabled_markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select_configuration.save_tfile()))

    if Configuration.plotter_configuration.wagasci_spill_number():
        spill_history(wagascianpy.plotting.plotter.WagasciSpillNumberPlotter(
            output_file_path=output_file_format.format(name='wagasci_spill_number'),
            bsd_database=Configuration.bsd_database_configuration.bsd_database(),
            bsd_repository=Configuration.bsd_database_configuration.bsd_download_location(),
            wagasci_database=Configuration.wagasci_database_configuration.wagasci_database(),
            wagasci_repository=Configuration.wagasci_database_configuration.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select_configuration.start(),
            stop=Configuration.run_select_configuration.stop(),
            enabled_markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select_configuration.save_tfile()))

    if Configuration.plotter_configuration.temperature():
        spill_history(wagascianpy.plotting.plotter.TemperaturePlotter(
            output_file_path=output_file_format.format(name='wagasci_temperature_history'),
            bsd_database=Configuration.bsd_database_configuration.bsd_database(),
            bsd_repository=Configuration.bsd_database_configuration.bsd_download_location(),
            wagasci_database=Configuration.wagasci_database_configuration.wagasci_database(),
            wagasci_repository=Configuration.wagasci_database_configuration.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select_configuration.start(),
            stop=Configuration.run_select_configuration.stop(),
            enabled_markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select_configuration.save_tfile()))

    if Configuration.plotter_configuration.humidity():
        spill_history(wagascianpy.plotting.plotter.HumidityPlotter(
            output_file_path=output_file_format.format(name='wagasci_humidity_history'),
            bsd_database=Configuration.bsd_database_configuration.bsd_database(),
            bsd_repository=Configuration.bsd_database_configuration.bsd_download_location(),
            wagasci_database=Configuration.wagasci_database_configuration.wagasci_database(),
            wagasci_repository=Configuration.wagasci_database_configuration.wagasci_decoded_location(),
            t2krun=Configuration.global_configuration.t2krun(),
            start=Configuration.run_select_configuration.start(),
            stop=Configuration.run_select_configuration.stop(),
            enabled_markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select_configuration.save_tfile()))

    if Configuration.plotter_configuration.gain_history():
        spill_history(wagascianpy.plotting.plotter.GainHistoryPlotter(
            output_file_path=output_file_format.format(name='wagasci_gain_history'),
            data_quality_location=Configuration.global_configuration.data_quality_location(),
            data_quality_filename=Configuration.global_configuration.data_quality_filename(),
            enabled_markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select_configuration.save_tfile()))

    if Configuration.plotter_configuration.dark_noise_history():
        spill_history(wagascianpy.plotting.plotter.DarkNoiseHistoryPlotter(
            output_file_path=output_file_format.format(name='wagasci_dark_noise_history'),
            data_quality_location=Configuration.global_configuration.data_quality_location(),
            data_quality_filename=Configuration.global_configuration.data_quality_filename(),
            enabled_markers=markers,
            topology=topology,
            save_tfile=Configuration.run_select_configuration.save_tfile()))