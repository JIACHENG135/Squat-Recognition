cmd = 'OpenposeDemo.exe --video VIDEO_NAME  --write_video output/OUTPUT_FILE --write_json output/FILE_NAME  '

# 
import os 
filepath = os.getcwd()
print(filepath)
files = os.listdir(filepath + "//example")

with open('run.txt','w') as opening:

    for ind,file in enumerate(files):
        fixed_file = file.replace("_","")
        try:
            if 30<int(file.strip(".avi"))<37:
        # try:
        #     os.mkdir(filepath + "/output/"+str(ind))
        # except:
        #     continue
        # os.rename(filepath + "\\example\\" + file ,filepath + "\\example\\" + str(ind)+".avi")
                opening.write(cmd.replace("VIDEO_NAME", "example/" +file).replace("FILE_NAME",file.strip(".avi")).replace("OUTPUT_FILE",file))
                opening.write("\n")
                opening.write("\n")
        except:
            continue
    opening.close()
