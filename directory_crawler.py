from os import getcwd, listdir, path
from json import dumps
from pprint import pformat, pprint
import timeit

denyList = [
    'venv', 'node_modules', '.git', '.jest', 'android', 'ios', 'Trash', 'yarn',
    '.npm', '__pycache__'
]

run_count = 0


def get_files_and_folders(cur_path):
    all_files_and_folders = listdir(cur_path)

    # just files
    files = [
        file for file in all_files_and_folders
        if path.isfile(path.join(cur_path, file))
    ]

    # just folders
    folders = [
        folder for folder in all_files_and_folders
        if path.isdir(path.join(cur_path, folder))
    ]

    # add files to dir dict
    name = cur_path.split('/')
    name = name[len(name) - 1]

    return name, files, folders


def write_to_json(dir_structure):
    file = open('dir_structure.json', 'w')
    file.write(dumps(dir_structure))
    file.close()


def recurse_func(cdir, parent, folder):
    folder_data = get_files_and_folders(cdir)
    return {'files': folder_data[1], 'folders': {}}, folder_data[2]


def looper(cdir, parent, folders):
    global run_count

    for folder in folders:
        print('-' * 30)
        if folder not in denyList:
            try:
                print('cwd - ' + cdir)
                newdir = path.join(cdir, folder)

                data = recurse_func(newdir, parent, folder)
                parent['folders'][folder] = data[0]

                run_count += 1

                looper(newdir, parent['folders'][folder], data[1])
            except PermissionError:
                continue

        print('total calls to get here ' + str(run_count))
        print('-' * 30)


def main():
    init_dir = '/home/marvinkome'
    final_dict = {}

    name, files, folders = get_files_and_folders(init_dir)
    final_dict[name] = {'files': files, 'folders': {}}

    # loop all folders
    looper(init_dir, final_dict[name], folders)

    # return final dict
    # write_to_json(final_dict)


start_time = timeit.default_timer()
main()
print(timeit.default_timer() - start_time)
# print(run_count)
