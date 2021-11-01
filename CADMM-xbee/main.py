import yaml
from agent import agent
import time
import keyboard
import sys

import pickle

def main():
    fname = sys.argv[1]

    with open(fname,'r') as file:
        params = yaml.full_load(file)

    node = agent(params)

    while(True):
        ts = time.time()
        node.step()
        te = time.time()
        # print('Stepping time:', te-ts)
        time.sleep(params['Meta']['loop_rate'])
        if keyboard.is_pressed('q'):
          print('Exited by keypress\n')
          break
    
    # print(node.all_y)
    pickle.dump(node.all_y,open(params['Meta']['save_file'],"wb"))
    pickle.dump([node.cost.A, node.cost.b],open(params['Meta']['save_file_cost'],"wb"))

if __name__ == '__main__':
    main()
