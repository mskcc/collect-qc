# Collect QC

Collect QC (CQ) is pipeline agnostic tool to merge QC metrics. Collect QC searches a given directory for bioinformatics metrics data and processes multiple QC metrics for each sample.

## Installation Guide

**Docker**
Build the Docker image from the container directory of the repository (CONTAINER_NAME is the name you assign to the container):

1. `cd collect-qc/container`
2. `docker build -t CONTAINER_NAME .`

**Python Virtual Environment**

1. Install [virtualenv](https://virtualenv.pypa.io/)
   `python3 -m pip install --user virtualenv`
2. Create a virtual environment (ENV_NAME is the name you assign to the virtual environment)
   `python3 -m venv ENV_NAME`
3. Install the required Python packages for Collect QC
   `cd collect-qc`
   `pip install -r requirements.txt`
4. Activate the virtual environment
   `source ENV_NAME/bin/activate`
5. Exiting the virtual environment
   `deactivate`

## How to run Collect QC

Ensure you have the bioinformatics metrics data and the config.yaml ([example_config.yaml](https://github.com/mskcc/collect-qc/blob/main/example_config.yaml)) file in your directory.

**Docker**
Run the Docker image with: `` docker run -it -v `pwd`:/usr/bin/collectqc/ {CONTAINER NAME} ``

**Python Virtual Environment**

1. Activate your virtual environment.
2. `cd collect-qc`
3. `python3 scripts/main.py`

## Modules

Each module will be implemented based on the inputs in the config.yaml ([example_config.yaml](https://github.com/mskcc/collect-qc/blob/main/example_config.yaml)) using the following format:

```
    module:
        function:
            function_name:
                ...
```

### Picard Insert Size

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

- **Mean Target Coverage**: Determines if the mean target coverage from each sample falls under the warning or error thresholds.

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

### Concordance

- **Match Sample Matrix**: Determines if there are sample mix-ups between patients.

  ```
  concordance:
      function:
      match_sample_matrix:
          match_error_lt: 49
          match_warn_lt: 90
          unmatch_warn_gt: 43.41
          unmatch_error_gt: 60
  ```

### Picard GC Bias

- **Coverage Deviation**: Determines the extent to which the coverage of the sample deviates based on the user's threshold.

  ```
  gcbias:
      function:
      coverage_deviation:
          columns: [gc, normalized_coverage]
          threshold: 0.6
  ```

## Contibuting Guide

When adding new modules to Collect QC, ensure that a unit test is provided for each module using the [pytest framework](https://pytest.org/).
