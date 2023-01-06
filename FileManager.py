import os
from Consts import FILE_CHUNK_SIZE
def divideFile(filename,directory='dividedfiles',outputdir='dividedfiles'):
    global FILE_CHUNK_SIZE
    if directory!='':
        directory+='/'
    # Open the file for reading in binary mode
    with open(directory+filename, 'rb') as f:
        # Get the size of the file
        file_size = os.path.getsize(directory+filename)
        # Calculate the number of partitions
        num_partitions = file_size // FILE_CHUNK_SIZE
        if file_size % FILE_CHUNK_SIZE != 0:
            num_partitions += 1

        # Iterate over the range of the number of partitions
        for i in range(num_partitions):
            # Move the file pointer to the desired position
            f.seek(i * FILE_CHUNK_SIZE)
            # Read a chunk of the file
            chunk = f.read(FILE_CHUNK_SIZE)
            # Write the chunk to a new file
            with open(outputdir+'/{}_{}.txt'.format(filename,i), 'wb') as partition:
                partition.write(chunk)
    # print(num_partitions)
    return num_partitions

def assembleFiles(myfile):
    filenames = os.listdir('./dividedfiles')
    print(filenames)
    # Create a new file for writing
    with open('assembledfiles/{}'.format(myfile), 'wb') as assembled:
        # Iterate over the list of file names
        for filename in filenames:
            # Open the file for reading
            with open("dividedfiles/{}".format(filename), 'rb') as f:
                # Read the contents of the file
                contents = f.read()
                # Write the contents to the new file
                assembled.write(contents)

#assembleFiles('FULLTEXT01.pdf')

# divideFile("FULLTEXT01.txt",'encryptedfiles')
