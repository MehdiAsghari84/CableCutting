# import libraries
from pyomo.environ import *
from itertools import combinations


# General variables
Drums = [4500,2700,3000]
Pieces = [300,450,450,547,556,583,592,610,610,610,612,613,619,621,625,675,682]
Remains = []

Drums_count = len(Drums)
Pieces_count = len(Pieces)

# Create model
model = ConcreteModel()
model.piec = Set(initialize=range(Pieces_count))
model.drum = Set(initialize=range(Drums_count))

# Binary means only accepted value is 0 and 1
model.x = Var(model.piec*model.drum, initialize=0, within=Binary)


# Optimization function
def ObjRule(model):
   for k in model.drum:
      Remains.append( Drums[k] - sum(Pieces[i]*model.x[i,k] for i in model.piec))
   return (sum((comb[0]-comb[1])**2 for comb in combinations(Remains, 2)))

# Maximize the optimization function
model.value = Objective(rule=ObjRule, sense = maximize)

# Conditions

# Each piece should cut only one
model.single_selection = ConstraintList()
for p in model.piec:
   model.single_selection.add(sum( model.x[p,d] for d in model.drum ) == 1.0)


# Sum of cutting pieces from a drum should less than drum length
model.cutting_limitation = ConstraintList()
for d in model.drum:
   model.cutting_limitation.add(sum( Pieces[i]*model.x[i,d] for i in model.piec)<=Drums[d])

# Download and set solver
solvername='Couenne'

solverpath_folder='C:\\solver\\Couenne-0.1.1-win32-icl10.0\\bin' 

solverpath_exe='C:\\solver\\Couenne-0.1.1-win32-icl10.0\\bin\\Couenne.exe'

solver=SolverFactory(solvername,executable=solverpath_exe)


results = solver.solve(model,tee=True)


print(results)

# Print matrix of cutting
for r in model.piec:
   for c in model.drum:
      print('(',r,',',c,') = ' + str(model.x[r,c].value))
 