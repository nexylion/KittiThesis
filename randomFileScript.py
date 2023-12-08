import os
import random
if __name__ == '__main__':
    length=int(len(os.listdir("./results"))*0.1)

    for i in range(length):
        random_file=random.choice(os.listdir("./results"))
        os.rename("./results/"+random_file, "./test/"+random_file)
