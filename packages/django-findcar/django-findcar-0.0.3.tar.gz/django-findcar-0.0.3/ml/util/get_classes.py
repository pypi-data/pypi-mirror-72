import os
import sys
import json

# get list of classes and class-to-index object from folder names
def get_classes(folder_path):
    classes = os.listdir(folder_path)
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, class_to_idx

# if this file is run directly, print get_classes and output it
if (__name__ == '__main__'):
    if (len(sys.argv) != 2):
        print('Expected 1 argument: "folder_path"')
        sys.exit()

    classes, class_to_idx = get_classes(sys.argv[1])
    print(classes, class_to_idx)

    with open('classes.json', 'w') as fout:
        json.dump(classes, fout)
    
    with open('class_to_idx.json', 'w') as fout:
        json.dump(class_to_idx, fout)
