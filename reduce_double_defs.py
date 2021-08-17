import json
import os
import glob
import sys

# Reference
# https://stackoverflow.com/questions/23306653/python-accessing-nested-json-data

def has_double_def(jline):
  def_count = 0
  def_token = ""
  for token in jline["source_tokens"]:
    if token.startswith("def ") == True :
       def_token = token
       def_count += 1
       if def_count > 1:
         return True
  return False
 
def proc_file(filename, dir_name, out_dir):
  with open(filename,"r") as file_in:
    lines = []
    jlines = []
    filename_parts = filename.split("/")
    file_op = open(out_dir + "/" + filename_parts[len(filename_parts)-1], "a")
    for line in file_in:
        jline = json.loads(line)
        if has_double_def(jline) == True:
          continue
        else:
          jlines.append(jline)

    for jline in jlines:
        json.dump(jline, file_op)
        file_op.write("\n")
    file_op.close()
           
        #if str(jline["has_bug"])=="True":
            #print(jline["provenances"])
            #filepath = jline["provenances"][0]["datasetProvenance"]["filepath"]
            #print(def_token + " : " + filepath)

if __name__ == "__main__":

  if len(sys.argv)<2:
    sys.exit("You did not enter all args. Exited")

  ip_dir_name = sys.argv[1]

  out_dir = ip_dir_name + "_double_defs_removed"
  os.system("mkdir " + out_dir)

  for filename in glob.glob('./' + ip_dir_name + '/*'):
    print(filename)
    proc_file(filename, ip_dir_name, out_dir)
