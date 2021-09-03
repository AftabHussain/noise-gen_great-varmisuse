import json
import glob
from pathlib import Path
import sys

INPUT_DIRS = ['']

step_no = -1

def generate_logs(input_dir):
    global step_no

    f_summary = open(input_dir + "/log_summary.txt", "a")

    with open(input_dir + "/summary") as file_in:

      lines = []
      no_bug_pred_acc_PREV = bug_loc_acc_PREV = tgt_loc_acc_PREV = jnt_acc_PREV = seqs_PREV = -1

      for line in file_in:
        parts = line.strip().split(" ")

        if parts[0]=="Step:":
          step_no = parts[1]

        if parts[0]=="Training" and parts[1]!="with":

          partition = "Training"
          
          ## -- CUMULATIVE VALUES -- ##

          no_bug_pred_acc  = float(parts[10][:-2].strip())                  # [:-2] to cut % and comma
          bug_loc_acc      = float(parts[11][:-2].strip())
          tgt_loc_acc      = float(parts[12][:-2].strip())
          jnt_acc          = float(parts[13][:-1].strip())
          seqs             = float(parts[3][:-1].strip().replace(",",""))   # [:-1] to only cut % (there's no comma afterwards) 

          ## -- NON-CUMULATIVE VALUES -- ## (The following processing is unnecessary for Evaluation)

          if int(step_no) == 1:
            no_bug_pred_acc_NC   = no_bug_pred_acc_PREV = no_bug_pred_acc   # PREV Corresponds to cum. values of previous step
            bug_loc_acc_NC       = bug_loc_acc_PREV     = bug_loc_acc       
            tgt_loc_acc_NC       = tgt_loc_acc_PREV     = tgt_loc_acc
            jnt_acc_NC           = jnt_acc_PREV         = jnt_acc
            seqs_NC              = seqs_PREV            = seqs

          else:

            # Formula explanation:
            # step2 non cum. acc = (step2_seqs x step2_accuracy - step1_seqs x step1_accuracy) / (step2_seqs - step1_seqs)

            no_bug_pred_acc_NC   = (seqs * no_bug_pred_acc - seqs_PREV * no_bug_pred_acc_PREV) / (seqs - seqs_PREV)
            bug_loc_acc_NC       = (seqs * bug_loc_acc - seqs_PREV * bug_loc_acc_PREV)         / (seqs - seqs_PREV)
            tgt_loc_acc_NC       = (seqs * tgt_loc_acc - seqs_PREV * tgt_loc_acc_PREV)         / (seqs - seqs_PREV)
            jnt_acc_NC           = (seqs * jnt_acc - seqs_PREV * jnt_acc_PREV)                 / (seqs - seqs_PREV)

            # Save the cumulative values of current step for next step
            no_bug_pred_acc_PREV   = no_bug_pred_acc
            bug_loc_acc_PREV       = bug_loc_acc
            tgt_loc_acc_PREV       = tgt_loc_acc
            jnt_acc_PREV           = jnt_acc
            seqs_PREV              = seqs

          print(step_no, partition, round(no_bug_pred_acc_NC,2), round(bug_loc_acc_NC,2), round(tgt_loc_acc_NC,2), round(jnt_acc_NC,2), sep = ",", file = f_summary)

        elif parts[0]=="Evaluation":

          partition = "Evaluation"
          
          no_bug_pred_acc  = parts[10][:-2].strip()
          bug_loc_acc      = parts[11][:-2].strip()
          tgt_loc_acc      = parts[12][:-2].strip()
          jnt_acc          = parts[13][:-1].strip()

          print(step_no, partition, no_bug_pred_acc, bug_loc_acc, tgt_loc_acc, jnt_acc, sep = ",", file = f_summary)
    print(f_summary.name)
    f_summary.close()

if __name__ == "__main__":
  for input_dir in INPUT_DIRS:
    generate_logs(input_dir)
