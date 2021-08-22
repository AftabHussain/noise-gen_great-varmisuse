import json
import glob
from pathlib import Path
import sys

INPUT_DIRS = ['noise75_1']

step_no = -1

def generate_logs(input_dir):
    global step_no

    f_summary = open(input_dir + "/log_summary.txt", "a")

    with open(input_dir + "/summary") as file_in:

      lines = []

      for line in file_in:
        parts = line.strip().split(" ")

        if parts[0]=="Step:":
          step_no = parts[1]

        if parts[0]=="Training" and parts[1]!="with":
          partition = "Training"
          
          #loc_loss        = parts[7][:-1].strip()
          #rep_loss        = parts[8][:-1].strip()
          no_bug_pred_acc  = parts[10][:-1].strip()
          bug_loc_acc      = parts[11][:-1].strip()
          target_loc_acc   = parts[12][:-1].strip()
          joint_acc        = parts[13].strip()

          #print(step_no, partition, loc_loss, rep_loss, no_bug_pred_acc, bug_loc_acc, target_loc_acc, joint_acc, sep = ",", file = f_summary)
          print(step_no, partition, no_bug_pred_acc, bug_loc_acc, target_loc_acc, joint_acc, sep = ",", file = f_summary)
          #print(line.strip())

        elif parts[0]=="Evaluation":
          partition = "Evaluation"
          
          #loc_loss        = parts[7][:-1].strip()
          #rep_loss        = parts[8][:-1].strip()
          no_bug_pred_acc  = parts[10][:-1].strip()
          bug_loc_acc      = parts[11][:-1].strip()
          target_loc_acc   = parts[12][:-1].strip()
          joint_acc        = parts[13].strip()

          #print(step_no, partition, loc_loss, rep_loss, no_bug_pred_acc, bug_loc_acc, target_loc_acc, joint_acc, sep = ",", file = f_summary)
          print(step_no, partition, no_bug_pred_acc, bug_loc_acc, target_loc_acc, joint_acc, sep = ",", file = f_summary)
          #print(line.strip())

    print(f_summary.name)
    f_summary.close()

if __name__ == "__main__":
  for input_dir in INPUT_DIRS:
    generate_logs(input_dir)
