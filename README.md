# Scripts for processing the GREAT Dataset

This repo consists of scripts that perform operations on the [great dataset](https://github.com/google-research-datasets/great).

To add noise to buggy samples, run `add_noise.py` as follows:
```
python3 add_noise.py <dir_name_of_sample> <noise_level_percentage> <trial_no> <estimate_of_total_no._of_buggy_samples>
```

We used the following bash command to run the script on multiple datasets:
```
for i in {1..5}; do time python3 add_noise.py train 25 ${i} 1798742 && zip -r train_noisy25_${i}.zip train_noisy25_${i} && rm -frv train_noisy25_${i}; done
```
