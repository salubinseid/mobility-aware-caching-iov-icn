import matplotlib.pyplot as plt
import random 
import math 
import numpy as np 
from pyomo.environ import *


#============Parameters===================
#  Number of Video conents V = 10, 20, 30
#  Number of Roadside unit R = 5
#  Number of basestation   Bs = 1
#  User (vehicle) density  U = 50
#  Size of Vedio    [10 - 30]
#===============================


# The data here is vedio with size and popularity values 
# video files have different size and popularity

# Generate the popularity of the vedio using zipf 
#s = np.random.zipf(2, 10)
#print (s)
p = [13,11,8,3,2,1,1,1,1,1]  # popularity
size = [10,20,30]  # content size 
c_size = random.choice(size)
c_size = 500
print (c_size)

# ==================Network configuration=======================
T = 10  # second
t_ru = 0 #0.001 # Average latency from RRH to user  1ms (generate it)- 1ms
tB = 0.01 # Average latency from BBU pool to user 10ms 
tS = 10 * tB  # Average latency from source to user  

B_ru  = 1   # Bandwidth of user u in its associated RRU r 

Nr = B_ru * T # data size that can be obtained from RRH r during one time unit 
Nb = 10  # data size that can be obtained from BBU r during one time unit 

Nu = 400  # Requested data size in one unit time



# user - This define the probability that the user move to RSU   
#        user:   mobility_to_rsu, probability (qru)

users = {
         "u1":  {"R1": 0.7,"R2": 0.2, "R3": 0.1, "R4": 0.0, "R5":0},
         "u2":  {"R1": 0.6,"R2": 0.2, "R3": 0.1, "R4": 0.1, "R5":0},
         "u3":  {"R1": 0.7,"R2": 0.2, "R3": 0.1, "R4": 0.0, "R5":0},
         "u4":  {"R1": 0.7,"R2": 0.2, "R3": 0.1, "R4": 0.0, "R5":0},
         "u5":  {"R1": 0.7,"R2": 0.2, "R3": 0.1, "R4": 0.0, "R5":0},
         "u6":  {"R1": 0.7,"R2": 0.2, "R3": 0.1, "R4": 0.0, "R5":0},
         "u7":  {"R1": 0.7,"R2": 0.2, "R3": 0.1, "R4": 0.0, "R5":0},
         "u8":  {"R1": 0.7,"R2": 0.2, "R3": 0.1, "R4": 0.0, "R5":0},
         "u9":  {"R1": 0.7,"R2": 0.2, "R3": 0.1, "R4": 0.0, "R5":0},
         "u10":  {"R1": 0.7,"R2": 0.2, "R3": 0.1, "R4": 0.0, "R5":0}
         }

#         video_item:   popularity, filesize
content = { "C1":      (p[0], c_size),
            "C2":      (p[1], c_size),
            "C3":      (p[2], c_size),
            "C4":      (p[3], c_size),
            "C5":      (p[4], c_size),
            "C6":      (p[5], c_size),
            "C7":      (p[6], c_size),
            "C8":      (p[7], c_size),
            "C9":      (p[8], c_size),
            "C10":     (p[9], c_size),
            "C11":      (p[0], c_size),
            "C12":      (p[1], c_size),
            "C13":      (p[2], c_size),
            "C14":      (p[3], c_size),
            "C15":      (p[4], c_size),
            "C16":      (p[5], c_size),
            "C17":      (p[6], c_size),
            "C18":      (p[7], c_size),
            "C19":      (p[8], c_size),
            "C20":     (p[9], c_size),
            "C21":      (p[0], c_size),
            "C22":      (p[1], c_size),
            "C23":      (p[2], c_size),
            "C24":      (p[3], c_size),
            "C25":      (p[4], c_size),
            "C26":      (p[5], c_size),
            "C27":      (p[6], c_size),
            "C28":      (p[7], c_size),
            "C29":      (p[8], c_size),
            "C30":     (p[9], c_size)
            }
 
# RSU          bin:    capacity  (100, 500, 1000, 1500, 2000)
rsu = {    "R1":       1000,
            "R2":      1000,
            "R3":      1000,
            "R4":      1000,
            "R5":      1000}

# MainBS    name      Capacity       
mbs = {     "MBS1":    10000 }



#q_ru =  # The probability of user u moving to an candidate RRH r
U = len(users) #5 # number of users
model = ConcreteModel()

# sets - data instance
model.users = Set(initialize=users.keys())
model.video = Set(initialize=content.keys()) # video   
model.rsu = Set(initialize=rsu.keys())   # rsu
model.mbs = Set(initialize=mbs.keys())  # basestation

# params - data that must be supplied to perform the optimization
model.mobility_u_r    = Param(model.users, initialize= {u:users[u][r] for u in users for r in rsu})
model.popularity   = Param(model.video, initialize= {k:content[k][0] for k in content})
model.filesize  = Param(model.video, initialize= {k:content[k][1] for k in content})
model.rsu_capa = Param(model.rsu, initialize= rsu) # Cache capacity
model.mbs_capa = Param(model.mbs, initialize= mbs) # Cache capacity

# vars
model.X = Var(model.users, model.video, model.rsu, domain=NonNegativeIntegers)     # the amount from invoice i in bin j
model.X_used = Var(model.video, domain=Binary)


model.Y = Var(model.video, model.mbs, domain=NonNegativeIntegers)
model.Y_used = Var(model.video, domain=Binary)


def objective_rule_no_mob(model):
    return sum((tS - t_ru)*model.X[u, v, r] * model.popularity[v] + (model.Y[v,b] * model.popularity[v])
                             for v in model.video 
                             for r in model.rsu
                             for b in model.mbs
                             for u in model.users) / U

def objective_rule_with_mob(model):
    return sum(((tS - t_ru)*model.X[u, v, r] * model.popularity[v] * model.mobility_u_r[u]) + (model.Y[v,b] * model.popularity[v])
                             for v in model.video 
                             for r in model.rsu
                             for b in model.mbs
                             for u in model.users) / U

### Objective ###
model.OBJ = Objective(rule=objective_rule_with_mob, sense=maximize)

### constraints ###

# c1 
def rsu_bin_limit(self, b):
    return sum(model.X[u, i, b] for i in model.video for u in model.users) <= model.rsu_capa[b]
    #return sum(model.X[u, i, b] * Nu for i in model.video for u in model.users) <= min(model.rsu_capa[b], 500)

model.c1 = Constraint(model.rsu, rule=rsu_bin_limit)

# c2
def mbs_bin_limit(self, b):
    return sum(model.Y[i, b] for i in model.video) <= model.mbs_capa[b]
model.c2 = Constraint(model.mbs, rule=mbs_bin_limit)

# c3 all-or-nothing on rsu
def use_all_rsu(self, i):
    #return sum(model.X[u, i, b] * model.mobility_u_r[u]  for b in model.rsu for u in model.users) == model.X_used[i] * model.filesize[i]
    return sum(model.X[u, i, b] for b in model.rsu for u in model.users) == model.X_used[i] * model.filesize[i]

model.c3 = Constraint(model.video, rule=use_all_rsu)

# all-or-nothing on mbs
def use_all_mbs(self, i):
    return sum(model.Y[i, b] for b in model.mbs) == model.Y_used[i] * model.filesize[i]
model.c4 = Constraint(model.video, rule=use_all_mbs)

# c5 rsu
def rsu_cached_fraction(self, i):
    return (model.X[u, i, b] for b in model.rsu for u in model.users) <= min(1, 1)

#model.c5 = Constraint(model.video, rule=rsu_cached_fraction)

# c6 mbs
def mbs_cached_fraction(self, i):
    return (model.X[u, i, b] for b in model.rsu for u in model.users) <= min(1, 1)

#model.c6 = Constraint(model.video, rule=mbs_cached_fraction)



# constraint 5: For every item, the sum of bins in which it appears must be 1
#def atmost_once(self, i):
#    return sum(model.X[i, b] for b in model.mbs) == model.Y_used[i] * model.filesize[i]
#model.c4 = Constraint(model.video, rule=use_all_mbs)


# solve it...
solver = SolverFactory('cbc')
results = SolverFactory('cbc').solve(model)
results.write()

model.X.display()


print("ContentId  popularity  RSU or MBS  Cached Amount")
for c in model.video:
    for r in model.rsu:
          for u in model.users:
            if(model.X[u, c,r]()>0):
                print(c, content[c][0], r, model.X[u,c,r]())

print("")
for c in model.video:
    for m in model.mbs:
        if(model.Y[c,m]()>0):
            print(c, content[c][0], m, model.Y[c,m]())


print('Optimal Solution')
print('Objective: =', model.OBJ())


if 'ok' == str(results.Solver.status):
    print("Total Caching Profit = ",model.OBJ())
    
else:
    print("No Valid Solution Found")
