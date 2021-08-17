import json
import random
import glob
import sys
import os

# Reference
# https://stackoverflow.com/questions/23306653/python-accessing-nested-json-data

noise_count = 0
threshold = 0

# Adds noise to a specific file
def add_noise(jline, file_op):
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
  json.dump(jline, file_op)
  file_op.write("\n")

# The function for deciding whether or not to add noise to a sample in a file
def proc_file(filename, dir_name, noise_level, trial_no, out_dir):
    global noise_count
    with open(filename,"r") as file_in:
        lines = []
        filename_parts = filename.split("/")
        file_op = open(out_dir + "/" + filename_parts[len(filename_parts)-1], "a")
        for line in file_in:
            jline = json.loads(line)
            if str(jline["has_bug"])=="True":
              if (random.randint(1,100) < 50) and noise_count < threshold:
                #print(noise_count, threshold, "adding noise") 
                add_noise(jline, file_op)
                noise_count+=1 
            else:
                #print(noise_count, threshold, "skipped") 
                json.dump(jline, file_op)
                file_op.write("\n")
        file_op.close()

if __name__ == "__main__":

  if len(sys.argv)<5:
    sys.exit("You did not enter all args. Exited")

  ip_dir_name = sys.argv[1]
  noise_level = sys.argv[2]
  trial_no = sys.argv[3]
  total_samples = sys.argv[4]

  # Fraction of buggy samples to which noise is to be added
  threshold = 500 * int(noise_level) / 100

  out_dir = ip_dir_name + "_noisy" + str(noise_level) + "_" + str(trial_no)
  os.system("mkdir " + out_dir)

  for filename in glob.glob('./' + ip_dir_name + '/*'):
    print(filename)
    proc_file(filename, ip_dir_name, noise_level, trial_no, out_dir)


