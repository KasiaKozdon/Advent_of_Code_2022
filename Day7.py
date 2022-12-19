#!/usr/bin/env python
# coding: utf-8
import unittest


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        

class Directory:
    def __init__(self, name, parent_dir):
        self.name = name
        self.parent_dir = parent_dir  # Directory class object
        self.children_dir = []  # Directory class object list
        self.file_inventory = []  # File class object list
        self.subdir_size = 0
        self.files_size = 0
        self.total_size = self.subdir_size + self.files_size
        self.update_parent_children()
        
    def update_file_size_sum(self):
        self.files_size = sum([file.size for file in self.file_inventory])
        
    def update_total_size(self):
        self.total_size = self.subdir_size + self.files_size
    
    def update_parent_size(self, delta):
        if self.parent_dir is not None:
            self.parent_dir.subdir_size += delta
            self.parent_dir.update_total_size()
            if self.parent_dir.parent_dir is not None:
                self.parent_dir.update_parent_size(delta)
                
    def update_parent_children(self):
        if self.parent_dir is not None:
            self.parent_dir.children_dir.append(self)
    

def parse_file_details(file_details):
    file_details = file_details.split(" ")
    file_size = int(file_details[0])
    file_name = file_details[1]
    return file_size, file_name


def parse_device_content(device_content_raw):
    change_dir = "$ cd"
    ignore = "$ ls"
    level_up = ".."
    directory = "dir"
    
    dir_dict = {}  # list of directory names as keys and Directory objects as values
    file_names = [] 
    file_objects = [] 
    current_path = [""]  # slightly redundant due to the possibility of using Directory.parent_dir and children_dir
    # to traverse the graph. Makes creation of unique names a bit simpler.

    for line in device_content_raw:
        if line.startswith(change_dir):
            switching_to = line.split()[-1]
            if switching_to == level_up:
                current_path.pop()
            else:
                current_path.append(switching_to)
                unique_name = '_'.join(current_path)
                if unique_name not in dir_dict.keys():
                    try:
                        parent_dir = dir_dict['_'.join(current_path[:-1])]
                    except:
                        parent_dir = None
                    new_dir = Directory(name=unique_name, parent_dir=parent_dir)
                    dir_dict[unique_name] = new_dir
        elif line.startswith(ignore):
            pass
        elif line.startswith(directory):
            pass
        else:
            file_size, file_name = parse_file_details(line)
            unique_name = '_'.join(current_path) + file_name
            file_object = File(unique_name, file_size)
            file_names.append(file_name)
            file_objects.append(file_object)
            new_dir.file_inventory.append(file_object)
            new_dir.files_size += file_size
            new_dir.total_size += file_size
            new_dir.update_parent_size(delta=file_size)
            
    [directory.update_total_size() for directory in dir_dict.values()]
            
    return dir_dict, file_objects


class Test(unittest.TestCase):
    def test_provided_examples(self):     
        with open("inputs/dummy7.txt") as f:
            device_content = f.readlines()
            device_content = [line.strip() for line in device_content]
        
        dir_dict, file_objects = parse_device_content(device_content)
        
        dir_e_size = dir_dict['_/_a_e'].total_size
        true_answer = 584
        self.assertEqual(true_answer, dir_e_size)

        dir_a_size = dir_dict['_/_a'].total_size
        true_answer = 94853
        self.assertEqual(true_answer, dir_a_size)
        
        dir_d_size = dir_dict['_/_d'].total_size
        true_answer = 24933642
        self.assertEqual(true_answer, dir_d_size)
        
        dir_root_size = dir_dict['_/'].total_size
        true_answer = 48381165
        self.assertEqual(true_answer, dir_root_size)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=3, exit=False)

            
with open("inputs/input7.txt") as f:
    device_content = f.readlines()
    device_content = [line.strip() for line in device_content]
    dir_dict, file_objects = parse_device_content(device_content)

    # PART A
    # Find all directories with total_size below 100000
    threshold = 100000
    small_dirs = [dir_dict[key].total_size for key in dir_dict.keys() if dir_dict[key].total_size < threshold]
    # Calculate the sum
    answer_a = sum(small_dirs)

    # PART B
    disk_space = 70000000
    required_space = 30000000
    available_space = disk_space - dir_dict["_/"].total_size
    candidates_to_delete = [dir_dict[key].total_size for key in dir_dict.keys() if available_space + dir_dict[key].total_size >= required_space]
    smallest_to_delete = min(candidates_to_delete)

print(f"Part a answer is: {answer_a}")
print(f"Part b answer is: {smallest_to_delete}")
