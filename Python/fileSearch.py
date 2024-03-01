import os
import glob

# files = os.listdir("C:/Users/joelg/Downloads/templogs")
# files = [*{*files}]



file = open("C:/Users/joelg/Downloads/templogs/temp_scans_IMSVA2.txt", "r")
messages = []
for line in file:
    #print(line.split())
    messageID = line.split()[-1]
    if messageID.endswith(".DF") or messageID.endswith(".RF"):
        messageID = messageID[11:-3]
    else:
        messageID = messageID[6:]
    print(messageID)
    messages.append(messageID)
messages = [*{*messages}]
messages = messages[110:130]
print(messages)
results = []


def search_folder(folder):
    os.chdir(folder)
    logfiles = glob.glob("log.imss*")
    for message in messages:
        #print(message)
        for logfile in logfiles:
            with open(logfile, "r", errors="surrogateescape") as f:
                for line in f:
                    if message in line:
                        results.append([line, f.name])


# search_folder("C:/Users/joelg/Downloads/CDT-20211105-162538/IMSVA/LogFile/Event3")
search_folder("C:/Users/joelg/Downloads/CDT-20211105-163028/IMSVA/LogFile/Event3")

with open("C:/Users/joelg/Downloads/templogs/search_results.txt", "w", errors="surrogateescape") as f:
    f.write("".join(str(results)))