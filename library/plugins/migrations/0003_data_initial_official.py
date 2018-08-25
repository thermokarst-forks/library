from django.db import migrations


class Migration(migrations.Migration):
    def migrate(apps, schema_editor):
        Plugin = apps.get_model('plugins', 'Plugin')
        PluginAuthorship = apps.get_model('plugins', 'PluginAuthorship')
        User = apps.get_model('users', 'User')

        plugins = [
            {'description': 'This QIIME 2 plugin provides support for generating and manipulating sequence alignments.',
              'name': 'alignment',
              'short_summary': 'Plugin for generating and manipulating alignments.'},
            {'description': 'This QIIME 2 plugin provides functionality for working with and visualizing Metadata.',
              'name': 'metadata',
              'short_summary': 'Plugin for working with Metadata.'},
            {'description': 'This QIIME 2 plugin supports demultiplexing of single-end and paired-end sequence reads and visualization of sequence quality information.',
             'name': 'demux',
             'short_summary': 'Plugin for demultiplexing & viewing sequence quality.'},
            {'description': 'This QIIME 2 plugin wraps DADA2 and supports sequence quality control for single-end and paired-end reads using the DADA2 R library.',
             'name': 'dada2',
             'short_summary': 'Plugin for sequence quality control with DADA2.'},
            {'description': 'This QIIME 2 plugin supports methods for supervised classification and regression of sample metadata, and other supervised machine learning methods.',
             'name': 'sample-classifier',
             'short_summary': 'Plugin for machine learning prediction of sample metadata.'},
            {'description': 'This QIIME 2 plugin supports methods for compositional data analysis.',
             'name': 'composition',
             'short_summary': 'Plugin for compositional data analysis.'
            },
            {'description': 'This QIIME 2 plugin supports generating and manipulating phylogenetic trees.',
             'name': 'phylogeny',
             'short_summary': 'Plugin for generating and manipulating phylogenies.'},
            {'description': 'This QIIME 2 plugin uses cutadapt to work with adapters (e.g. barcodes, primers) in sequence data.',
             'name': 'cutadapt',
             'short_summary': 'Plugin for removing adapter sequences, primers, and other unwanted sequence from sequence data.'},
            {'description': 'This QIIME 2 plugin supports metrics for calculating and exploring community alpha and beta diversity through statistics and visualizations in the context of sample metadata.',
             'name': 'diversity',
             'short_summary': 'Plugin for exploring community diversity.'},
            {'description': 'This QIIME 2 plugin supports taxonomic classification of features using a variety of methods, including Naive Bayes, vsearch, and BLAST+.',
             'name': 'feature-classifier',
             'short_summary': 'Plugin for taxonomic classification.'},
            {'description': 'This plugin wraps the vsearch application, and provides methods for clustering and dereplicating features and sequences.',
             'name': 'vsearch',
             'short_summary': 'Plugin for clustering and dereplicating with vsearch.'},
            {'description': 'This is a QIIME 2 plugin supporting operations on sample by feature tables, such as filtering, merging, and transforming tables.',
             'name': 'feature-table',
             'short_summary': 'Plugin for working with sample by feature tables.'},
            {'description': 'This QIIME 2 plugin wraps the Deblur software for performing sequence quality control.',
             'name': 'deblur',
             'short_summary': 'Plugin for sequence quality control with Deblur.'},
            {'description': 'This QIIME 2 plugin supports filtering and trimming of sequence reads based on PHRED scores and ambiguous nucleotide characters.',
             'name': 'quality-filter',
             'short_summary': 'Plugin for PHRED-based filtering and trimming.'},
            {'description': 'This QIIME 2 plugin wraps Emperor and supports interactive visualization of ordination plots.',
             'name': 'emperor',
             'short_summary': 'Plugin for ordination plotting with Emperor.'},
            {'description': 'This QIIME 2 plugin supports methods for assessing and controlling the quality of feature and sequence data.',
             'name': 'quality-control',
             'short_summary': 'Plugin for quality control of feature and sequence data.'},
            {'description': 'This QIIME 2 plugin supports methods for analysis of time series analysis, involving either paired sample comparisons or longitudinal study designs.',
             'name': 'longitudinal',
             'short_summary': 'Plugin for paired sample and time series analyses.'},
            {'description': 'This QIIME 2 plugin provides functionality for working with and visualizing taxonomic annotations of features.',
             'name': 'taxa',
             'short_summary': 'Plugin for working with feature taxonomy annotations.'},
            {'description': 'This QIIME 2 plugin defines semantic types and transformers supporting microbiome analysis.',
             'name': 'types',
             'short_summary': 'Plugin defining types for microbiome analysis.'},
            {'description': 'This is a QIIME 2 plugin supporting statistical models on feature tables and metadata using balances.',
             'name': 'gneiss',
             'short_summary': 'Plugin for building compositional models.'}
        ]

        q2d2 = User.objects.get(username='q2d2')

        for plugin in plugins:
            plugin = Plugin.objects.create(
                name=plugin['name'],
                short_summary=plugin['short_summary'],
                description=plugin['description'],
                install_guide='Check out https://docs.qiime2.org/2018.6/install/ for installation instructions.',
                published=True,
            )
            PluginAuthorship.objects.create(
                plugin=plugin,
                author=q2d2,
                list_position=0,
            )

    def rollback(apps, schema_editor):
        Plugin = apps.get_model('plugins', 'Plugin')
        PluginAuthorship = apps.get_model('plugins', 'PluginAuthorship')

        PluginAuthorship.objects.all().delete()
        Plugin.objects.all().delete()

    dependencies = [
        ('plugins', '0002_plugin_authors'),
        ('users', '0003_data_initial_official'),
    ]

    operations = [
        migrations.RunPython(migrate, rollback),
    ]
