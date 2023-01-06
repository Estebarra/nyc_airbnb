#!/usr/bin/env python
"""
Performs basic cleaning on the data and store the results in Weights & Biases
"""
import os
import argparse
import logging
import pandas as pd

import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    """
    Main function, implementation of basic cleaning operations
    """

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()
    df = pd.read_csv(artifact_path)

    # Drop outliers
    min_price = 10
    max_price = 350
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    filename = args.output_artifact
    df.to_csv(filename, index=False)

    artifact = wandb.Artifact(
        filename,
        type=args.output_type,
        description=args.output_description,
    )

    artifact.add_file(filename)
    run.log_artifact(artifact)

    os.remove(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Input file",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="output file",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="output type",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="File processed by eliminating outliers",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum limit to consider if a datum is an outlier or not",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum limit to consider if a datum is an outlier or not",
        required=True
    )

    args = parser.parse_args()

    go(args)
