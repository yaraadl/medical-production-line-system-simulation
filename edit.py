"""
yara adel hassan mohamed 19100683
system modeling and simulation 
project 2  12th 

Scenario:
  A medication production line  has 5 proceeses workstations   with a limited number of buffer space between workstations that share a common
  buffer . units  randomly arrive at the packaging production factory , request one
  of the processe workstations  and starts performing each one of them  respectively untill being ready to be pushed into market .

  A medication production line control process observes theavailable space in workstations 

"""

import random
import simpy
from sympy import RR


wait_times=0
noinqueue=0
noofunits=0
throughput=0
average_inventory_level=0
blocking_probabilities=0

averagesystemflow=0
system_time=0
startblock=0
endblock=0
block_time=0
totalblocktime=0
RANDOM_unit= 42
STATION_SIZE = 5     # unites placed in front of the workstation
THRESHOLD = 10             # Threshold for calling the station adminstrator (in %)
buffer_SIZE = 5        # size
buffer_congestion_LEVEL = [0, 5]  # Min/max levels of congestion levels 
REFilLING_SPEED = 2        # liters / second
unit_adminstartion_TIME = 300      # Seconds it takes the adminstrator to arrive
T_INTER = [30, 300]        # Create a unit every [min, max] seconds
SIM_TIME = 100000            # Simulation time in seconds
queue_congestion_level=0
filling_time=6.5
capping_time=5
labeling_time=8
sealing_time=5
carton_packing_time=6
unitName=0
unit =0 
products=0
blocked=0
totaltime = 0 
def cartoon(unitName, env,cartoonpackingstation):
    global unit
    global blocked , block_time , totaltime
    started = env.now
    print(unitName,'arrived at cartton packing waitting for its turn at', env.now)
    with cartoonpackingstation.request() as req:
    
        yield req
        yield env.timeout(carton_packing_time)
        block_time+=env.now
        blocked+=1
    ended = env.now
    totaltime+=(ended - started)  
    unit +=1

def sealing(unitName, env,sealingstation,cartoonpackingstation):
    global blocked ,block_time , totaltime
    started = env.now
    print(unitName,'arrived at sealing waitting for its turn at', env.now)
    with sealingstation.request() as req:
        yield req
        yield env.timeout(sealing_time)
        block_time+=env.now
        blocked+=1
    ended = env.now
    totaltime+=(ended - started)  
    env.process(cartoon(unitName, env,cartoonpackingstation))

def labeling(unitName, env,labelingstation,sealingstation,cartoonpackingstation):
    global blocked ,block_time , totaltime
    started = env.now
    print(unitName,'arrived at labelling waitting for its turn at', env.now)
    with labelingstation.request() as req:
        yield req
        yield env.timeout(labeling_time)
        block_time+=env.now
        blocked+=1
    ended = env.now
    totaltime+=(ended - started)  
    env.process(sealing(unitName, env,sealingstation,cartoonpackingstation))


def capping(unitName, env, cappingstation, labelingstation,sealingstation,cartoonpackingstation):
    global blocked ,block_time , totaltime
    started = env.now
    print(unitName,'arrived at capping waitting for its turn at', env.now)
    with cappingstation.request() as req:
        yield req
        yield env.timeout(capping_time)
        block_time+=env.now
        blocked+=1
    ended = env.now
    totaltime+=(ended - started)  
    env.process(labeling(unitName, env,labelingstation,sealingstation,cartoonpackingstation))

def filling(unitName, env,fillingstation, cappingstation, labelingstation,sealingstation,cartoonpackingstation):
    global blocked , block_time , totaltime 
    started= env.now 
    print(unitName,'arrived at filling waitting for its turn at', env.now)

    with fillingstation.request() as req:
        yield req

        yield env.timeout(filling_time)
        block_time+=env.now
        blocked+=1
    ended  =env.now 
    totaltime+=(ended - started)  
    env.process(capping(unitName, env, cappingstation, labelingstation,sealingstation,cartoonpackingstation))


def unit_generator(env, fillingstation, cappingstation, labelingstation,sealingstation,cartoonpackingstation):
   
    """Generate new units that arrive at the station."""
    
    while True:
        env.process(filling('unit %d' % unit, env,fillingstation, cappingstation, labelingstation,sealingstation,cartoonpackingstation))
       
        yield env.timeout(8)
        
# Setup and start the simulation
print('work Station refilling with units')
random.seed(RANDOM_unit)
noofunits=noofunits+1

# Create environment and start processes
env = simpy.Environment()
fillingstation = simpy.Resource(env, 5)
cappingstation = simpy.Resource(env, 5)
labelingstation = simpy.Resource(env, 5)
sealingstation = simpy.Resource(env, 5)
cartoonpackingstation = simpy.Resource(env, 5)

env.process(unit_generator(env, fillingstation, cappingstation, labelingstation,sealingstation,cartoonpackingstation))




# Execute!

env.run(until=100000)

totalthrouput= unit/100000
print("throughput = %f" %totalthrouput)

average_inventory_level=blocked/5
print('average inventory level in buffer = %f' % average_inventory_level)

downprobabilities =((block_time%100)/100000)
print('downtime and blocking probabilities at bottleneck workstations = %f' % downprobabilities)

averagesystemflow=totaltime/100000
print('average system flow times = %f' % averagesystemflow)




