# dividing file into chunks nad storing in the list
def split_file(chunk_size):
    sentences=[]
    with open('dummy.txt','r') as file:
        chunk_number = 1
        while True:
            chunk = file.readlines(chunk_size)
            sentences.extend(chunk)    
            if not chunk:
                 break
            chunk_number += 1
       
    return sentences   
        
if __name__ == '__main__':
    sentences = split_file(10)
    sentences = [i.lower().strip() for i in sentences ]
    for i in sentences:
        print(i)    