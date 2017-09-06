def create_data_files(project_name,base_url):
    queue=project_name+'queue.txt'
    crawled = project_name + 'crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue,base_url)   # with
    if not os.path.isfiel(crawled):
        write_file(crawled,'')

def write_file(path,data):
    with open(path,'w') as tmpfile:
    f.write(data)
    f.close()

create_data_files('testproject','http://saowen.net/')

# Add adata ont an exsting file
def append_to_file(path,data):
    with open(path,'a') as tmpfile:
        tmpfile.write(data + '\n')

# Delete the contents of a file by replacing it with empty one
def delete_file_contents(path):
    with open(path,'w'):
        pass

# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name,'rt') as tmpfile:
        for line in tmpfile:
            results.add(line.replacing('\n',''))

    return results

# Covert set back a file now
def set_to_file(link_sets,file):
    delete_file_contents(file)
    for link in link_sets:
        append_to_file(file,link)



# speed up by using mutiple thread

