#!python3
# Author Joel Ginsberg
# Modified from https://geekflare.com/python-delete-files/

import os
import shutil
import time

# main function
def main():
    # initializing the count
    deleted_folders_count = 0
    deleted_files_count = 0

    # specify the path
    path = r"C:\Users\joelg\Documents\Cases"

    # specify the days
    days = 30

    # converting days to seconds
    # time.time() returns current time in seconds
    seconds = time.time() - (days * 24 * 60 * 60)

    # checking whether the file is present in path or not
    if os.path.exists(path):

        # iterating over each and every folder and file in the path
        for root_folder, folders, files in os.walk(path):

            #for subdir, dirs, files in os.walk(path):

            for file in files:
                # set file path
                fp = os.path.join(root_folder, file)
                # weird filepath workaround
                # https://stackoverflow.com/questions/33604543/python-filenotfounderror-winerror-3-for-getsizefilepath
                fp = u"\\\\?\\" + fp
                # print(fp)

                if os.path.getsize(fp) > 10 * 1048000: # if greater than 10 MB
                    print(fp)
                    print(os.path.getsize(fp))
                    # file path
                    file_path = os.path.join(root_folder, file)

                    # If file is older than number of days specified above
                    if seconds <= get_file_or_folder_age(fp):
                        # invoking the remove_file function
                        print(fp)
                        remove_file(file_path)
                        deleted_files_count += 1  # incrementing count

                        # Check if current folder is empty after deleting the file
                        if len(os.listdir(root_folder)) == 0:
                            print(root_folder)
                            print(len(os.listdir(root_folder)))
                            remove_folder(root_folder)
                            deleted_folders_count += 1  # incrementing count

                        # trying to check one level above, decided it wasn't necessary
                        #print(os.listdir(os.path.dirname(root_folder)))
                            #print("No")
    else:
        # file/folder is not found
        print(f'"{path}" is not found')


    print(f"Total folders deleted: {deleted_folders_count}")
    print(f"Total files deleted: {deleted_files_count}")


def remove_folder(path):
    # removing the folder
    if not shutil.rmtree(path):

        # success message
        print(f"{path} is removed successfully")

    else:

        # failure message
        print(f"Unable to delete the {path}")


def remove_file(path):
    # removing the file
    if not os.remove(path):

        # success message
        print(f"{path} is removed successfully")

    else:

        # failure message
        print(f"Unable to delete the {path}")


def get_file_or_folder_age(path):
    # getting ctime of the file/folder
    # time will be in seconds
    ctime = os.stat(path).st_ctime

    # returning the time
    return ctime


if __name__ == '__main__':
    main()