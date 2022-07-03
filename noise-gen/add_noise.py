import json
import random
import glob
import sys
import os
from noise_util import *

# Reference
# https://stackoverflow.com/questions/23306653/python-accessing-nested-json-data

noise_on_buggy = 0
noise_on_buggy_thresh = 0
noise_on_correct = 0
noise_on_correct_thresh = 0

# The function for deciding whether or not to add noise to a sample in a file
def proc_file(filename, dir_name, noise_level, trial_no, out_dir):
    global noise_on_buggy, noise_on_buggy_thresh, noise_on_correct, noise_on_correct_thresh
    with open(filename,"r") as file_in:
        lines = []
        filename_parts = filename.split("/")
        file_op = open(out_dir + "/" + filename_parts[len(filename_parts)-1], "a")
        for line in file_in:
            jline = json.loads(line)
            if jline["has_bug"]== True:
              if (random.randint(1,100) < int(noise_level) + 1) and noise_on_buggy < noise_on_buggy_thresh:
                try:
                  jline = add_x_noise_to_buggy(jline)    # noisify buggy (x noise)
                  #jline = buggy_to_correct(jline)      # noisify buggy (y noise)
                  noise_on_buggy += 1 
                except Exception as e:
                  print("Exception, ignoring sample")
                  continue
            elif jline["has_bug"] == False:
              if (random.randint(1,100) < int(noise_level) + 1) and noise_on_correct < noise_on_correct_thresh:
                jline = add_x_noise_to_correct(jline)  # noisify correct (x noise)
                #jline = correct_to_buggy(jline)      # noisify correct (y noise)
                noise_on_correct += 1 
            json.dump(jline, file_op)
            file_op.write("\n")
        file_op.close()

        # Stopping criterion
        if noise_on_buggy >= noise_on_buggy_thresh and noise_on_correct >= noise_on_correct_thresh:
           print("Noise Thresholds reached!")
           return True
        else:
           return False

if __name__ == "__main__":

  if len(sys.argv)<5:
    sys.exit("You did not enter all args. Exited")

  ip_dir_name = sys.argv[1]                 
  noise_level = sys.argv[2]                # Noise Level (e.g. 25, 50, etc.)
  trial_no = sys.argv[3]                   # Instance Number
  total_samples = sys.argv[4]              # Total Number of Samples               

  # Fraction of buggy samples to which noise is to be added
  noise_on_buggy_thresh = int(total_samples) * int(noise_level) / 100

  # Fraction of correct samples to which noise is to be added
  noise_on_correct_thresh = int(total_samples) * int(noise_level) / 100

  out_dir = ip_dir_name + "_noisy" + str(noise_level) + "_" + str(trial_no)
  os.system("mkdir " + out_dir)
 
  noise_thresh_reached = False

  for filename in glob.glob('./' + ip_dir_name + '/*'):
    print(filename)
    if noise_thresh_reached == False:
      noise_thresh_reached = proc_file(filename, ip_dir_name, noise_level, trial_no, out_dir)
    else: # Stopping criterion reached
      os.system("cp -frv " + filename + " " + out_dir)          # if files are still left, copy them over
      
  print("No. of buggy samples to which noise was added: ", noise_on_buggy)
  print("No. of correct samples to which noise was added: ", noise_on_correct)

  with open (out_dir + "_log", "w") as f:
    f.write("\nNo. of buggy samples to which noise was added: " + str(noise_on_buggy))
    f.write("\nNo. of correct samples to which noise was added: " + str(noise_on_correct))
    f.close()




