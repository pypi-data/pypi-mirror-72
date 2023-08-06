import os
import argparse

import matplotlib.pyplot as plt
import numpy as np

from vivarium.core.experiment import Experiment
from vivarium.core.composition import (
    simulate_compartment_in_experiment,
    plot_compartment_topology,
    plot_simulation_output,
    COMPARTMENT_OUT_DIR,
)
from vivarium.data.nucleotides import nucleotides
from vivarium.data.amino_acids import amino_acids
from vivarium.data.chromosomes.flagella_chromosome import FlagellaChromosome
from vivarium.states.chromosome import Chromosome, rna_bases, sequence_monomers
from vivarium.processes.transcription import UNBOUND_RNAP_KEY
from vivarium.processes.translation import UNBOUND_RIBOSOME_KEY
from vivarium.compartments.gene_expression import (
    GeneExpression,
    plot_gene_expression_output,
    gene_network_plot,
)
from vivarium.parameters.parameters import (
    parameter_scan,
    get_parameters_logspace,
    plot_scan_results,
)


NAME = 'flagella_gene_expression'


def get_flagella_expression_config(config):
    flagella_data = FlagellaChromosome(config)
    chromosome_config = flagella_data.chromosome_config
    sequences = flagella_data.chromosome.product_sequences()

    return {

        'transcription': {

            'sequence': chromosome_config['sequence'],
            'templates': chromosome_config['promoters'],
            'genes': chromosome_config['genes'],
            'transcription_factors': flagella_data.transcription_factors,
            'promoter_affinities': flagella_data.promoter_affinities,
            'polymerase_occlusion': 30,
            'elongation_rate': 50},

        'translation': {

            'sequences': flagella_data.protein_sequences,
            'templates': flagella_data.transcript_templates,
            'concentration_keys': ['CRP', 'flhDC', 'fliA'],
            'transcript_affinities': flagella_data.transcript_affinities,
            'elongation_rate': 22,
            'polymerase_occlusion': 50},

        'degradation': {

            'sequences': sequences,
            'catalysis_rates': {
                'endoRNAse': 0.01},
            'degradation_rates': {
                'transcripts': {
                    'endoRNAse': {
                        transcript: 1e-23
                        for transcript in chromosome_config['genes'].keys()}}}},

        'complexation': {
            'monomer_ids': flagella_data.complexation_monomer_ids,
            'complex_ids': flagella_data.complexation_complex_ids,
            'stoichiometry': flagella_data.complexation_stoichiometry,
            'rates': flagella_data.complexation_rates},
    }


def get_flagella_initial_state(ports={}):
    flagella_data = FlagellaChromosome()
    chromosome_config = flagella_data.chromosome_config

    molecules = {}
    for nucleotide in nucleotides.values():
        molecules[nucleotide] = 5000000
    for amino_acid in amino_acids.values():
        molecules[amino_acid] = 1000000

    return {
        ports.get(
            'molecules',
            'molecules'): molecules,
        ports.get(
            'transcripts',
            'transcripts'): {
                gene: 0
                for gene in chromosome_config['genes'].keys()
        },
        ports.get(
            'proteins',
            'proteins'): {
                'CpxR': 10,
                'CRP': 10,
                'Fnr': 10,
                'endoRNAse': 1,
                'flagella': 8,
                UNBOUND_RIBOSOME_KEY: 200,  # e. coli has ~ 20000 ribosomes
                UNBOUND_RNAP_KEY: 200
            }
    }


def get_flagella_compartment(config):
    flagella_expression_config = get_flagella_expression_config(config)
    return GeneExpression(flagella_expression_config)


def plot_timeseries_heatmaps(timeseries, config, out_dir='out'):
    ''' make a timeseries heatmap for each port specified in config['plot_ports'] '''

    name = config.get('name', 'timeseries')
    plot_ports = config.get('plot_ports', {})
    ports = config.get('ports', {})
    time = timeseries['time']

    def relative_to_max(series):
        relative = max(max(series), 1)
        return [
            value / relative
            for value in series]

    # make timeseries heatmaps
    ts_heatmap = {}
    for port_id, order in plot_ports.items():
        port = timeseries[ports[port_id]]
        var_keys = list(order)

        var_series = [
            relative_to_max(port[key])
            for key in var_keys]

        var_keys.reverse()  # reverse to get proper labeling with imshow

        ts_heatmap[port_id] = {
            'keys': var_keys,
            'timeseries': var_series}

    # make figure for each port in plot_ports
    for port_id, heatmap in ts_heatmap.items():
        n_cols = 1
        n_vars = len(heatmap['keys'])

        fig = plt.figure(figsize=(4 * n_cols, 0.6 * n_vars))

        var_keys = heatmap['keys']
        var_series = heatmap['timeseries']
        n_vars = len(var_keys)
        ax = fig.add_subplot(111)

        im = ax.imshow(var_series,
            extent=[time[0], time[-1], 0, n_vars],
            interpolation='nearest',
            aspect='auto',
            cmap='cividis'
            )
        ax.locator_params(axis='y', nbins=n_vars)

        # set y ticks locations and labels
        y_tick_locs = np.asarray([loc+0.5 for loc in range(n_vars)])
        ax.set_yticks(y_tick_locs)
        ax.set_yticklabels(var_keys)
        ax.set_xlabel('time (s)')

        # colorbar
        cbar = fig.colorbar(im)
        cbar.set_label('relative flourescence', rotation=270, labelpad=20)

        # save figure
        figname = name + '_' + port_id
        fig_path = os.path.join(out_dir, figname)
        plt.savefig(fig_path, bbox_inches='tight')


def make_compartment_topology(out_dir='out'):
    # load the compartment
    flagella_compartment = get_flagella_compartment({})

    settings = {'show_ports': True}
    plot_compartment_topology(
        flagella_compartment,
        settings,
        out_dir)


def make_flagella_network(out_dir='out'):
    # load the compartment
    flagella_compartment = get_flagella_compartment({})

    # make expression network plot
    flagella_expression_processes = flagella_compartment.generate_processes({})
    operons = flagella_expression_processes['transcription'].genes
    promoters = flagella_expression_processes['transcription'].templates
    complexes = flagella_expression_processes['complexation'].stoichiometry
    data = {
        'operons': operons,
        'templates': promoters,
        'complexes': complexes}
    gene_network_plot(data, out_dir)


def run_flagella_expression(out_dir='out'):
    # load the compartment
    flagella_compartment = get_flagella_compartment({})

    # get flagella data
    flagella_data = FlagellaChromosome()

    # run simulation
    initial_state = get_flagella_initial_state()
    settings = {
        'timestep': 1,
        # a cell cycle of 2520 sec is expected to express 8 flagella.
        # 2 flagella expected in ~630 seconds.
        'total_time': 760,
        'verbose': True,
        'initial_state': initial_state}
    timeseries = simulate_compartment_in_experiment(flagella_compartment, settings)

    plot_config = {
        'name': 'flagella_expression',
        'ports': {
            'transcripts': 'transcripts',
            'proteins': 'proteins',
            'molecules': 'molecules'}}

    plot_gene_expression_output(
        timeseries,
        plot_config,
        out_dir)

    # just-in-time figure
    plot_config2 = plot_config.copy()
    plot_config2.update({
        'name': 'flagella',
        'plot_ports': {
            'transcripts': list(flagella_data.chromosome_config['genes'].keys()),
            'proteins': flagella_data.complexation_monomer_ids + flagella_data.complexation_complex_ids,
            'molecules': list(nucleotides.values()) + list(amino_acids.values())}})

    plot_timeseries_heatmaps(
        timeseries,
        plot_config2,
        out_dir)

    # make a basic sim output
    plot_settings = {
        'max_rows': 30,
        'remove_zeros': False,
        'skip_ports': ['chromosome', 'ribosomes']}
    plot_simulation_output(
        timeseries,
        plot_settings,
        out_dir)


def scan_flagella_expression_parameters():
    compartment = get_flagella_compartment({})
    flagella_data = FlagellaChromosome()

    # conditions
    conditions = {}

    # parameters
    scan_params = {}
    # # add promoter affinities
    # for promoter in flagella_data.chromosome_config['promoters'].keys():
    #     scan_params[('promoter_affinities', promoter)] = get_parameters_logspace(1e-3, 1e0, 4)

    # scan minimum transcript affinity -- other affinities are a scaled factor of this value
    scan_params[('min_tr_affinity', flagella_data.min_tr_affinity)] = get_parameters_logspace(1e-2, 1e2, 6)

    # # add transcription factor thresholds
    # for threshold in flagella_data.factor_thresholds.keys():
    #     scan_params[('thresholds', threshold)] = get_parameters_logspace(1e-7, 1e-4, 4)

    # metrics
    metrics = [
        ('proteins', monomer)
        for monomer in flagella_data.complexation_monomer_ids] + [
        ('proteins', complex)
        for complex in flagella_data.complexation_complex_ids]

    print('number of parameters: {}'.format(len(scan_params)))  # TODO -- get this down to 10

    # run the scan
    scan_config = {
        'compartment': compartment,
        'scan_parameters': scan_params,
        'conditions': conditions,
        'metrics': metrics,
        'settings': {'total_time': 480}}
    results = parameter_scan(scan_config)

    return results


if __name__ == '__main__':
    out_dir = os.path.join(COMPARTMENT_OUT_DIR, NAME)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # run scan with python vivarium/compartments/flagella_expression.py --scan
    parser = argparse.ArgumentParser(description='flagella expression')
    parser.add_argument('--scan', '-s', action='store_true', default=False,)
    parser.add_argument('--network', '-n', action='store_true', default=False,)
    parser.add_argument('--topology', '-t', action='store_true', default=False,)
    args = parser.parse_args()

    if args.scan:
        results = scan_flagella_expression_parameters()
        plot_scan_results(results, out_dir)
    elif args.network:
        make_flagella_network(out_dir)
    elif args.topology:
        make_compartment_topology(out_dir)
    else:
        run_flagella_expression(out_dir)

