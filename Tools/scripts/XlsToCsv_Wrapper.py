import sys, os, subprocess

base_dir = os.path.dirname(os.path.realpath(__file__))
vbs_script = base_dir + "\XlsToCsv.vbs"

def main(dir_path):
  os.chdir(dir_path)
  curr_dir = os.getcwd()
  files = os.listdir(".")
  for file in files:
    filename = file.split(".")
    subprocess.call(["Cscript.exe", vbs_script, curr_dir+"\\"+file, curr_dir+"\\"+filename[0]+".csv"])
  

if __name__ == "__main__":
  main(sys.argv[1])