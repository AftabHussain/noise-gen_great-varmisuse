import json
import random
import time


# Adds noise to a specific buggy sample
# NOTE: Currently not being used
def add_noise(jline):
  error_location = []
  '''
  print("--------------------------------------------------------")
  print("Original Data")
  print("Repair candidates: ", jline["repair_candidates"])
  print("Repair targets: ", jline["repair_targets"])
  print("Error Loc: ", jline["error_location"])
  '''
  error_location.append(jline["error_location"])
  
  # print("Noisy Data")
  
  # Create Sets
  repair_candidates = set(jline["repair_candidates"])
  repair_targets = set(jline["repair_targets"])
  error_location = set(error_location)
  
  # Generate noisy data 
  repair_targets_noisy =  list(repair_candidates - repair_targets)
  error_location_noisy = -1
  error_location_noisy = random.choice(list(repair_candidates - error_location)) #- repair_targets_noisy
  
  '''
  print("Noisy Repair targets: ", repair_targets_noisy)
  print("Noisy Error Location:", error_location_noisy)
  print("--------------------------------------------------------")
  '''
  
  # Check for empty sets
  assert(error_location_noisy!=-1)
  assert(len(repair_targets_noisy)>0)
  #print(jline["provenances"])
  
  # Save the noisy data
  jline["error_location"] = error_location_noisy
  jline["repair_targets"] = repair_targets_noisy
  return jline

def buggy_to_correct(sample):
    sample["has_bug"] = False
    sample["bug_kind"] = 0
    sample["bug_kind_name"] = "NONE"
    sample["error_location"] = 0
    sample["repair_targets"] = []
    return sample


def correct_to_buggy(sample):
    sample["has_bug"] = True
    sample["bug_kind"] = 1
    sample["bug_kind_name"] = "VARIABLE_MISUSE"

    # for simplicity randomly shuffling the repair_candidates,
    #   and use last value as error_location
    #   and use first three values as repair_targets
    int_candidates = [x for x in sample["repair_candidates"] if isinstance(x, int)]
    random.seed(time.time())
    random.shuffle(int_candidates)
    sample["error_location"] = int_candidates[-1]
    sample["repair_targets"] = int_candidates[:3]
    return sample


# For Test
if __name__ == "__main__":
    filename = "train__VARIABLE_MISUSE__SStuB.txt-00000-of-00300.txt"
    temp_chk = True  # buggy = True, correct = False
    with open(filename) as txt_file:
        for str_line in txt_file:
            json_sample = json.loads(str_line)
            if json_sample["has_bug"] != temp_chk:
                continue
            print(json_sample)
            noisy_sample = None
            if json_sample["has_bug"]:
                noisy_sample = buggy_to_correct(json_sample.copy())
            else:
                noisy_sample = correct_to_buggy(json_sample.copy())
            print(noisy_sample)
            break
