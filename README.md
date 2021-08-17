# Scripts for processing the GREAT Dataset

This repo consists of scripts that perform operations on the [great dataset](https://github.com/google-research-datasets/great).

To add noise to buggy samples, run `add_noise.py` as follows:
```
python3 trial_noise.py <dir_name_of_sample> <noise_level_percentage> <trial_no> <estimate_of_total_no._of_buggy_samples>
```
