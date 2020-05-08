from os.path import dirname, join, realpath

directory_of_this_file = dirname(realpath(__file__))
data_dir = join(directory_of_this_file, 'data')
keywords_dir = join(data_dir, 'keywords')
letters_dir = join(data_dir, 'letters')