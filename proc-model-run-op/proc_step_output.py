import json
import glob
from pathlib import Path
import sys

# Reference(s):
# https://www.kite.com/python/answers/how-to-print-a-list-without-brackets-in-python#:~:text=Use%20*%20to%20print%20a%20list,set%20sep%20to%20%22%2C%20%22%20.

# This program generates a csv output from step_X_output.txt files that are generated (per step) while running the GREAT model.

INPUT_DIRS = ['GREAT-Aftab']
TRAIN_SET = "train" 
TOTAL_STEPS = 50
bug_map = {}
source_tokens_len_map = {}
repair_cands_len_map = {}

def load_dataset(dataset):
  global bug_map
  for filename in Path("./" + dataset + "/").glob("*"): 
    filename = filename.name
    if filename[0] == ".":
      continue
    print(filename)
    with open(dataset + "/" + filename, "r") as file_in:
          lines = []
          filename_parts = filename.split("/")
          for line in file_in:
              jline = json.loads(line)
              key = jline["line_no"]
              bug_map[key] = jline["has_bug"]
              source_tokens_len_map[key] = (len(jline["source_tokens"]))
              repair_cands_len=0
              for candidate in jline["repair_candidates"]: 
                if isinstance(candidate, int):
                   repair_cands_len += 1
              repair_cands_len_map[key] = repair_cands_len 

   
def generate_logs(input_dir):

  global bug_map, source_token_len_map 

  # Files (in csv) for storing info on the samples (We only need to process
  # step files of one epoch to get the ids of the samples that were picked from
  # the train and dev sets.)
  f_dev_data = open(input_dir + "/log_dev_data"+".txt", "a")
  print("#samp_id, #has_bug, #num_of_src_tokens, #num_of_rep_candidates", file = f_dev_data)
  f_train_data = open(input_dir + "/log_train_data"+".txt", "a")
  print("#samp_id, #has_bug, #num_of_src_tokens, #num_of_rep_candidates", file = f_train_data)

  for step in range(1,TOTAL_STEPS+1):
                
    # Files (in csv) for storing per epoch stats for each sample. 
    f_train = open(input_dir + "/log_train_ep"+str(step)+".txt", "a")
    print("#samp_id, #samp_loc_prob, #samp_loc_loss, #samp_tgt_prob, #samp_tgt_loss", file = f_train)
    f_dev = open(input_dir + "/log_dev_ep"+str(step)+".txt", "a")
    print("#samp_id, #samp_loc_prob, #samp_loc_loss, #samp_tgt_prob, #samp_tgt_loss", file = f_dev)

    with open(input_dir + "/step_" + str(step) + "_output.txt") as file_in:

      lines = []
      batch_ids = []
      batch_loc_prob = []
      batch_loc_loss = []
      batch_tgt_prob = []
      batch_tgt_loss = []

      read_batch_ids = False
      read_batch_data = False
      read_batch_loc_prob = False
      read_batch_loc_loss = False
      read_batch_tgt_prob = False
      read_batch_tgt_loss = False

      for line in file_in:

        parts = line.strip().split(" ")

        # --- PROCESSING BATCH IDS --- #

        if parts[0]=="BATCH_START":
          read_batch_ids = True
          read_batch_data = False
          continue

        if read_batch_ids == True:
          batch_ids.append(line.strip())

        if parts[0]=="BATCH_END":
          read_batch_ids = False
          read_batch_data = True
          continue

        # --- PROCESSING BATCH DATA --- #

        if read_batch_data == True:

          # Processing Batch Loc Prob # 

          if parts[0]=="LOC_PROB_SAMP_START":
            read_batch_loc_prob = True
            continue

          if read_batch_loc_prob == True:
            batch_loc_prob = parts 
            read_batch_loc_prob = False

          # Processing Batch Loc Loss # 

          if parts[0]=="LOC_LOSS_SAMP_START":
            read_batch_loc_loss = True
            continue

          if read_batch_loc_loss == True:
            batch_loc_loss = parts 
            read_batch_loc_loss = False

          # Processing Batch Tgt Prob # 

          if parts[0]=="TGT_PROB_SAMP_START":
            read_batch_tgt_prob = True
            continue

          if read_batch_tgt_prob == True:
            batch_tgt_prob = parts 
            read_batch_tgt_prob = False

          # Processing Batch Tgt Loss # 

          if parts[0]=="TGT_LOSS_SAMP_START":
            read_batch_tgt_loss = True
            continue

          if read_batch_tgt_loss == True:
            batch_tgt_loss = parts 
            read_batch_tgt_loss = False
             
          if parts[0]=="TGT_LOSS_SAMP_END":
            # At this point, batch data reading is complete.
            # print data in the format: 
            for sample in list(zip(batch_ids, batch_loc_prob, batch_loc_loss, batch_tgt_prob, batch_tgt_loss)):
              has_bug_val = bug_map[sample[0]]
              source_tokens_len = source_tokens_len_map[sample[0]]
              repair_cands_len = repair_cands_len_map[sample[0]]
              data_set = sample[0].split("_")[0].split("-")[0]
              if (data_set == "train"):
                print(*sample, sep = ", ", file = f_train)
                if step ==1: 
                  print(sample[0], has_bug_val, source_tokens_len, repair_cands_len, sep = ", ", file = f_train_data)
              elif (data_set == "dev"):
                print(*sample, sep = ", ", file = f_dev)
                if step ==1: 
                  print(sample[0], has_bug_val, source_tokens_len, repair_cands_len, sep = ", ", file = f_dev_data)

     
            batch_ids.clear()
            batch_loc_prob.clear()
            batch_loc_loss.clear()
            batch_tgt_prob.clear()
            batch_tgt_loss.clear()

    print(f_train.name)
    print(f_dev.name)
    f_train.close()
    f_dev.close()
  f_train_data.close()
  f_dev_data.close()

if __name__ == "__main__":

  load_dataset("dev")
  load_dataset(TRAIN_SET)
  
  for input_dir in INPUT_DIRS:
    generate_logs(input_dir)
