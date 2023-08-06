import numpy as np
from pegasus import io, tools, demuxEM


def run_demuxEM_pipeline(input_adt_file, input_rna_file, output_name, **kwargs):
    # load input data
    adt = io.read_input(input_adt_file, genome="_ADT_")
    print("ADT file is loaded.")
    data = io.read_input(input_rna_file, genome=kwargs["genome"], concat_matrices=True)
    print("RNA file is loaded.")

    # Filter the RNA matrix
    data.obs["n_genes"] = data.X.getnnz(axis=1)
    data.obs["n_counts"] = data.X.sum(axis=1).A1
    obs_index = np.logical_and.reduce(
        (
            data.obs["n_genes"] >= kwargs["min_num_genes"],
            data.obs["n_counts"] >= kwargs["min_num_umis"],
        )
    )
    data._inplace_subset_obs(obs_index)
    data.var["robust"] = True

    # run demuxEM
    demuxEM.estimate_background_probs(adt, random_state=kwargs["random_state"])
    print("Background probability distribution is estimated.")
    demuxEM.demultiplex(
        data,
        adt,
        min_signal=kwargs["min_signal"],
        alpha=kwargs["alpha"],
        n_threads=kwargs["n_jobs"],
    )
    print("Demultiplexing is done.")

    # annotate raw matrix with demuxEM results
    genome_indexed_raw_data = io.read_input(
        input_rna_file, return_type="MemData", concat_matrices=False
    )
    for keyword in genome_indexed_raw_data.listKeys():
        array2d = genome_indexed_raw_data.getData(keyword)
        barcodes = array2d.barcode_metadata.index
        idx = barcodes.isin(data.obs_names)
        selected = barcodes[idx]

        demux_type = np.empty(barcodes.size, dtype="object")
        demux_type[:] = ""
        demux_type[idx] = data.obs.loc[selected, "demux_type"]
        array2d.barcode_metadata["demux_type"] = demux_type

        assignment = np.empty(barcodes.size, dtype="object")
        assignment[:] = ""
        assignment[idx] = data.obs.loc[selected, "assignment"]
        array2d.barcode_metadata["assignment"] = assignment

        if "assignment.dedup" in data.obs:
            assignment_dedup = np.empty(barcodes.size, dtype="object")
            assignment_dedup[:] = ""
            assignment_dedup[idx] = data.obs.loc[selected, "assignment.dedup"]
            array2d.barcode_metadata["assignment.dedup"] = assignment_dedup

    print("Demultiplexing results are added to raw expression matrices.")

    # generate plots
    if kwargs["gen_plots"]:
        demuxEM.plot_adt_hist(
            adt, "hto_type", output_name + ".ambient_hashtag.hist.pdf", alpha=1.0
        )
        demuxEM.plot_bar(
            adt.uns["background_probs"],
            adt.var_names,
            "Sample ID",
            "Background probability",
            output_name + ".background_probabilities.bar.pdf",
        )
        demuxEM.plot_adt_hist(
            adt, "rna_type", output_name + ".real_content.hist.pdf", alpha=0.5
        )
        demuxEM.plot_rna_hist(data, output_name + ".rna_demux.hist.pdf")
        print("Diagnostic plots are generated.")

    if len(kwargs["gen_gender_plot"]) > 0:
        tools.log_norm(data, 1e5)
        for gene_name in kwargs["gen_gender_plot"]:
            demuxEM.plot_violin(
                data,
                {"gene": gene_name},
                "{output_name}.{gene_name}.violin.pdf".format(
                    output_name=output_name, gene_name=gene_name
                ),
                title="{gene_name}: a gender-specific gene".format(gene_name=gene_name),
            )
        print("Gender-specific gene expression violin plots are generated.")

    # output results
    io.write_output(adt, output_name + "_ADTs.h5ad")
    print(
        "Hashtag count information is written to {output_name}_ADTs.h5ad .".format(
            output_name=output_name
        )
    )
    io.write_output(data, output_name + "_demux.h5ad")
    print(
        "Demutiplexed RNA expression information is written to {output_name}_demux.h5ad .".format(
            output_name=output_name
        )
    )
    io.write_output(genome_indexed_raw_data, output_name + "_demux")
    print(
        "Raw pegasus-format hdf5 file with demultiplexing results is written to {output_name}_demux.h5sc .".format(
            output_name=output_name
        )
    )

    # output summary statistics
    print("\nSummary statistics:")
    print("total\t{}".format(data.shape[0]))
    for name, value in data.obs["demux_type"].value_counts().iteritems():
        print("{}\t{}".format(name, value))
