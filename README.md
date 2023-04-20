# Collect QC

Collect QC (CQ) is pipeline agnostic tool to merge QC metrics. Collect QC searches a given directory for bioinformatics metrics data and processes multiple QC metrics for each sample.

## Installation Guide

Clone the repository:

```
git clone https://github.com/mskcc/collect-qc.git
```

- **Docker**

  Build the Docker image from the container directory of the repository (CONTAINER_NAME is the name you assign to the container):

  1. Navigate to the directory of the repository with the Dockerfile:
     ```
     cd collect-qc/container
     ```
  2. Build the Docker image:
     ```
     docker build -t CONTAINER_NAME .
     ```

- **Python Virtual Environment**

  1. Install [virtualenv](https://virtualenv.pypa.io/):

     ```
     python3 -m pip install --user virtualenv
     ```

  2. Create a virtual environment (ENV_NAME is the name you assign to the virtual environment):

     ```
     python3 -m venv ENV_NAME
     ```

  3. Install the required Python packages for Collect QC
     - Navigate to the repository directory:
     ```
     cd collect-qc
     ```
     - Install the required Python packages:
     ```
     pip install -r requirements.txt
     ```
  4. Activate the virtual environment:

     ```
     source ENV_NAME/bin/activate
     ```

  5. Exit the virtual environment:

     ```
     deactivate
     ```

## How to run Collect QC

Ensure you have the bioinformatics metrics data and the config.yaml ([example_config.yaml](example_config.yaml)) file in your directory.

- **Docker**

  Run the Docker image with:

  ```
  docker run -it -v `pwd`:/usr/bin/collectqc/ {CONTAINER NAME}
  ```

- **Python Virtual Environment**

  1. Activate your virtual environment.
  2. Navigate to the repository directory:

     ```
     cd collect-qc
     ```

  3. Run the main Python script:
     ```
     python3 scripts/main.py
     ```

## Modules

Each module will be implemented based on the inputs in the config.yaml ([example_config.yaml](example_config.yaml)) using the following format:

```
  module:
    function:
      function_name:
        ...
```

### Picard Insert Size

Extracts data from files ending with .ismetrics

- **Peak Analysis**: Identifies the maximum peak in each insert size distribution and reports whether the sample passed or failed based on the number of peaks.

  ```
  insert_size:
    function:
      peak_analysis:
        columns: [1, 2]
  ```

  Results:

  - PASS: The number of peaks is equal to 1.
  - FAIL: The number of peaks is not equal to 1.

  Plot Output:

  - Insert size distribution of each sample with the maximum peak listed for each sample in the plot legend.

### Picard HsMetrics

Extracts data from files ending with .hsmetrics

- **Thresholding**: Determines if the mean target coverage from each sample falls under the warning or error thresholds.

  ```
  hsmetrics:
    function:
      threshold:
        column: mean_target_coverage
        warn: 700
        error: 500
  ```

  Results:

  - PASS: the sample's value does not fall under the WARNING or ERROR threshold.
  - WARNING: the sample's value falls under the WARNING threshold and above the ERROR threshold.
  - ERROR: the sample's value falls under the ERROR threshold.

  Plot Output:

  - Bar graph of the mean target coverages of each sample and the warning and error threshold lines.

### Concordance

Extracts data from files ending with concordance.txt

- **Match Sample Matrix**: Determines if there are sample mix-ups between patients. The "match" threshold corresponds to tumor samples with the same patient as the normal sample, and the "unmatch" threshold corresponds to tumor samples with a different patient from the normal sample.

  ```
  concordance:
    function:
      match_sample_matrix:
        match_error_lt: 49
        match_warn_lt: 90
        unmatch_warn_gt: 43.41
        unmatch_error_gt: 60
  ```

  Results:

  - PASS: When there is a match between the normal sample and the tumor sample, and the value is greater than match_warn_lt, or when there is a mismatch between the normal sample and the tumor sample and the value is less than unmatch_warn_gt.
  - WARNING: When the value falls within the match (match_error_lt and match_warn_lt) or unmatch (unmatch_warn_gt and unmatch_error_gt) thresholds.
  - ERROR: When there is a match between the normal sample and the tumor sample and the value is less than match_error_lt, or when there is a mismatch between the normal sample and the tumor sample and the value is greater than or equal to unmatch_error_gt.

  Plot Output:

  - Heatmap plot of the concordance matrix with the normal sample and the tumor samples.

### Picard GC Bias

Extracts data from files ending with .hstmetrics

- **Coverage Deviation**: Determines the extent to which the coverage of the sample deviates based on the user's threshold.

  ```
  gcbias:
    function:
      coverage_deviation:
        columns: [gc, normalized_coverage]
        threshold: 0.6
  ```

  Results:

  - PASS: The area under the curve of the normalized coverage vs. GC-content plot for the sample is less than the threshold.
  - FAIL: The area under the curve of the normalized coverage vs. GC-content plot for the sample is greater than the threshold.

  Plot Output:

  - The Normalized Coverage vs. GC-content plot will be created with the GC-content binned in 5% intervals.

## Integration with MultiQC

[MultiQC](https://multiqc.info/) has been integrated with Collect QC using the [MultiQC python package](https://pypi.org/project/multiqc/). After running Collect QC, the MultiQC HTML report will be created (multiqc_report.html).

## Output of Collect QC

After running Collect QC, the following will appear in your working directory:

- "CollectQC_Plots" folder containing plots (.png files) corresponding to each module output.
- CollectQC_Summary.txt report consisting of the result status (PASSED, WARNING, or FAILED), tables listing the samples that have a WARNING or FAILED status, and the reason why each sample was assigned that status. The contents of the config.yaml file are located at the end of the report for reference.
- MultiQC HTML report (multiqc_report.html) consisting of data analytics provided by MultiQC.

## Contibuting Guide

When adding new modules to Collect QC, ensure that a unit test is provided for each module using the [pytest framework](https://pytest.org/), and update the README with a description of the module.
