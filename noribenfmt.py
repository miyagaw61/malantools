from enert import *
import traceback
import sys
import re

argv = sys.argv
argc = len(argv)

def usage():
    usage_text = """Usage:
$ touch noribenfmt_start
$ touch noribenfmt_finish
$ rm -rf noribenfmt_start
$ ./malware
$ rm -rf noribenfmt_finish
$ python noribenfmt.py log.csv out.csv\
"""
    print(usage_text)
    exit()

if argc < 3:
    usage()
elif argv[1] in ["-h", "--help"]:
    usage()

r_start_text = "SetRenameInformationFile.*hogehogehoge.*Recycle"
r_finish_text = "SetRenameInformationFile.*fugafugafuga.*Recycle"
r_linenr = re.compile("^[0-9]+")
r_first_block_text = "^[^,]+,"
r_second_block_text = "^([^,]+,)([^,]+,)"
log_file = argv[1]
out_file = argv[2]
f_log = File(log_file)
f_out = File(out_file)
data = f_log.read()
if f_out.exist():
    f_out.rm()
try:
    start_line, _ = Shell("cat %s | grep -n %s" % (log_file, r_start_text)).readlines()
    start_line = start_line[0]
except:
    traceback.print_exc()
    exit()
try:
    finish_line, _ = Shell("cat %s | grep -n %s" % (log_file, r_finish_text)).readlines()
    finish_line = finish_line[0]
except:
    traceback.print_exc()
    exit()

try:
    start_linenr = r_linenr.findall(start_line)[0]
except:
    traceback.print_exc()
    exit()

try:
    finish_linenr = r_linenr.findall(finish_line)[0]
except:
    traceback.print_exc()
    exit()

start_linenr = int(start_linenr)
finish_linenr = int(finish_linenr)
tail_arg = finish_linenr - start_linenr + 1
cmd = f"head -n {finish_linenr} {log_file} | tail -n {tail_arg} > {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^[^,]+,@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^([^,]+,)([^,]+,)([^,]+,)@\\1\\3@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^(.*)([^,]+),([^,]+,)([^,]+$)@\\1\\2@g' -i {out_file}"
Shell(cmd).call()

cmd = f"sed -E 's@(reateFile.*OpenResult: Created)@G\\1@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@(reateFile.*Desired Access: Delete)@G\\1@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@.*CreateFile.*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@CGreateFile@CreateFile@g' -i {out_file}"
Shell(cmd).call()

cmd = f"sed -E 's@.*CloseFile.*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@.*LockFile.*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@.*UnlockFileSingle.*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^\"csrss.exe\".*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^\"MsMpEng.exe\".*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^\"svchost.exe\".*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^\"OneDrive.exe\".*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^\"Conhost.exe\".*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^\"VBoxTray.exe\".*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^\"TiWorker.exe\".*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@^\"ctfmon.exe\".*@@g' -i {out_file}"
Shell(cmd).call()
cmd = f"sed -E 's@.*RegSetInfoKey.*KeySetInformationClass:\\sKeySetHandleTagsInformation,\\sLength:\\s0.*@@g' -i {out_file}"
Shell(cmd).call()

cmd = f"grep -v -e '^\s*$' {out_file} > noribenfmt.tmp && mv noribenfmt.tmp {out_file}"
Shell(cmd).call()
