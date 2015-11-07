import mimetypes
import time
import sys
FAILURE = 'FAILURE'
global Counter
Counter=0
def solve(csp):
  """
  Solve a constraint satisfaction problem.
  csp is an object that should have properties:
    variables:  
      dictionary of variables and values they can take on
    constraints:
      list of constraints where each element is a tuple of 
      (head node, tail node, constraint function)
 """
  result = backtrack(csp['legacy_constraints'], csp['variables'], csp)
  if result == FAILURE: 
      return result,Counter
  return { k:v[0] for k,v in result.iteritems() },Counter # Unpack values wrapped in arrays.
  
def backtrack(assignments, unassigned, csp):
  """
  Main algorithm for solving a constraint satisfaction problem.
  """
  global Counter
  if finished(unassigned): 
      return assignments
  var = select_unassigned_variable(unassigned)
  values = order_values(var, assignments, unassigned, csp)
  del unassigned[var]
  
  for value in values:
    assignments[var] = [value]
    v = enforce_consistency(assignments, unassigned, csp)
    if any_empty(v): continue # A variable has no legal values.
    u = { var:val for var,val in v.iteritems() if var not in assignments }
    result = backtrack(assignments.copy(), u, csp)
    if result != FAILURE: 
        return result
    
    Counter=Counter+1
  return FAILURE

def finished(unassigned):
  return len(unassigned) == 0

def any_empty(v):
  return any((len(values) == 0 for values in v.itervalues()))

def partial_assignment(assignments, unassigned):
  """
  Merge together assigned and unassigned dictionaries (assigned
  values take priority).
  """
  v = unassigned.copy()
  v.update(assignments)
  return v

def enforce_consistency(assignments, unassigned, csp):
  """
  Enforces arc consistency by removing values from tail nodes of a 
  constraint, and if a node loses value, perform arc consistency on 
  that node.
  """

  def remove_inconsistent_values(head, tail, constraint, variables):
    """
    Checks if there are any inconsistent values in the tail. An 
    inconsistent value means that for a given value in the tail,
    there are no values in head that will satisfy the constraints.
    Returns whether there were inconsistent values in tail.
    """
    valid_tail_values = [t for t in variables[tail.strip().lower()] if any((constraint(h, t) for h in variables[head]))]
    removed = len(variables[tail.strip().lower()]) != len(valid_tail_values)
    variables[tail.strip().lower()] = valid_tail_values
    return removed

  def incoming_constraints(node):
    """
    All constraints where constraint head is the passed in node.
    """
    return [(h, t, c) for h, t, c in csp['constraints'] if h == node]
    
  queue, variables = csp['constraints'][:], partial_assignment(assignments, unassigned)
  while len(queue):
    head, tail, constraint = queue.pop(0)
    if remove_inconsistent_values(head, tail, constraint, variables):
      queue.extend(incoming_constraints(tail)) # Need to recheck constraint arcs coming into tail.
  return variables

def select_unassigned_variable(unassigned):
  """
  Picks the next variable to assign according to the 
  Minimum Remaining Values principle: choose the variable
  with the fewest legal values remaining. This helps 
  identify failure earlier.
  """
  return min(unassigned.keys(), key=lambda k: len(unassigned[k]))
    
def order_values(var, assignments, unassigned, csp):
  """
  Orders the values of an unassigned variable according to the
  Least Constraining Value principle: order values by the amount
  of values they eliminate when assigned (fewest eliminated at the
  front, most eliminated at the end). Keeps future options open.
  """
  def count_vals(vars):
    return sum((len(vars[v]) for v in unassigned if v != var)) 

  def values_eliminated(val):
    assignments[var] = [val]
    new_vals = count_vals(enforce_consistency(assignments, unassigned, csp)) 
    del assignments[var]
    return new_vals

  return sorted(unassigned[var], key=values_eliminated, reverse=True)
  
def add(towhat,newquay,where):
        info = towhat.get(newquay,[])
        info.append(where)
        towhat[newquay] = info
        
'''Write the result to a file'''        
def file_write(solution):        
        file = open("result.txt", "w")
        for key in solution:
            file.write(key)
            file.write(' ')
            file.write(solution[key])
            file.write("\n")
        file.close()
        
        
'''Read legacy constraint file'''
    
def file_read(path):
    legacy_constraints={}  
    with open(path) as f:
        for line in f:
            words = line.split()
            if words:
                #it = iter(words)
                legacy_constraints[words[0].strip().lower()]=words[1].strip()
    return legacy_constraints
            
'''Check Input constraint file'''
def valid_constraint_file(file):
    if mimetypes.guess_type(file)[0] == 'text/plain':
        return True
    else:
        return False
    
def adjacentStates():
    states_dictionary={}
    new_states_dictionary={}
    allstates=[]
    adjacentstates=[["Alaska"],
                    ["Alabama","Mississippi","Tennessee","Georgia","Florida"],
                    ["Arkansas","Missouri","Tennessee","Mississippi","Louisiana","Texas","Oklahoma"],
                    ["Arizona","California","Nevada","Utah","Colorado","New_Mexico"],
                    ["California","Oregon"," Nevada","Arizona"],
                    ["Colorado","Wyoming","Nebraska","Kansas", "Oklahoma", "New_Mexico", "Arizona", "Utah"],
                    ["Connecticut", "New_York", "Massachusetts","Rhode_Island"],
                    ["Delaware", "Maryland","Pennsylvania", "New_Jersey"],
                    ["Florida", "Alabama","Georgia"],
                    ["Georgia", "Florida", "Alabama", "Tennessee", "North_Carolina", "South_Carolina"],
                    ["Hawaii"],
                    ["Iowa", "Minnesota", "Wisconsin", "Illinois", "Missouri", "Nebraska", "South_Dakota"],
                    ["Idaho", "Montana", "Wyoming", "Utah", "Nevada", "Oregon", "Washington"],
                    ["Illinois", "Indiana", "Kentucky", "Missouri", "Iowa", "Wisconsin"],
                    ["Indiana", "Michigan", "Ohio", "Kentucky", "Illinois"],
                    ["Kansas", "Nebraska", "Missouri", "Oklahoma", "Colorado"],
                    ["Kentucky", "Indiana", "Ohio", "West_Virginia", "Virginia", "Tennessee", "Missouri", "Illinois"],
                    ["Louisiana", "Texas", "Arkansas", "Mississippi"],
                    ["Massachusetts", "Rhode_Island", "Connecticut", "New_York", "New_Hampshire" ,"Vermont"],
                    ["Maryland", "Virginia", "West_Virginia", "Pennsylvania","Delaware"],
                    ["Maine", "New_Hampshire"],
                    ["Michigan", "Wisconsin", "Indiana", "Ohio"],
                    ["Minnesota", "Wisconsin", "Iowa", "South_Dakota", "North_Dakota"],
                    ["Missouri", "Iowa", "Illinois", "Kentucky", "Tennessee", "Arkansas", "Oklahoma", "Kansas", "Nebraska"],
                    ["Mississippi", "Louisiana", "Arkansas", "Tennessee", "Alabama"],
                    ["Montana", "North_Dakota", "South_Dakota", "Wyoming", "Idaho"],
                    ["North_Carolina", "Virginia", "Tennessee", "Georgia", "South_Carolina"],
                    ["North_Dakota", "Minnesota", "South_Dakota", "Montana"],
                    ["Nebraska", "South_Dakota", "Iowa", "Missouri", "Kansas", "Colorado", "Wyoming"],
                    ["New_Hampshire", "Vermont", "Maine", "Massachusetts"],
                    ["New_Jersey", "Delaware", "Pennsylvania", "New_York"],
                    ["New_Mexico", "Arizona", "Utah", "Colorado", "Oklahoma", "Texas"],
                    ["Nevada", "Idaho", "Utah", "Arizona", "California", "Oregon"],
                    ["New_York", "New_Jersey", "Pennsylvania", "Vermont", "Massachusetts", "Connecticut"],
                    ["Ohio", "Pennsylvania", "West_Virginia","Kentucky", "Indiana", "Michigan"],
                    ["Oklahoma", "Kansas" ,"Missouri", "Arkansas", "Texas", "New_Mexico", "Colorado"],
                    ["Oregon", "California", "Nevada", "Idaho","Washington"],
                    ["Pennsylvania", "New_York", "New_Jersey", "Delaware", "Maryland", "West_Virginia", "Ohio"],
                    ["Rhode_Island", "Connecticut", "Massachusetts"],
                    ["South_Carolina", "Georgia", "North_Carolina"],
                    ["South_Dakota", "North_Dakota", "Minnesota", "Iowa", "Nebraska", "Wyoming", "Montana"],
                    ["Tennessee", "Kentucky", "Virginia", "North_Carolina", "Georgia", "Alabama", "Mississippi", "Arkansas", "Missouri"],
                    ["Texas", "New_Mexico", "Oklahoma", "Arkansas", "Louisiana"],
                    ["Utah", "Idaho", "Wyoming", "Colorado", "New_Mexico", "Arizona", "Nevada"],
                    ["Virginia", "North_Carolina", "Tennessee", "Kentucky", "West_Virginia", "Maryland"], 
                    ["Vermont", "New_York", "New_Hampshire", "Massachusetts"],
                    ["Washington", "Idaho", "Oregon"],
                    ["Wisconsin", "Michigan", "Minnesota", "Iowa", "Illinois"],
                    ["West_Virginia", "Ohio", "Pennsylvania", "Maryland", "Virginia", "Kentucky"],
                    ["Wyoming", "Montana", "South_Dakota", "Nebraska", "Colorado", "Utah", "Idaho"]]
    
    for row_index, row in enumerate(adjacentstates):
        for col_index, item in enumerate(row):
            item=item.strip().lower()
            if item not in allstates:
                states_dictionary.setdefault(item,[])
                new_states_dictionary.setdefault(item,[])
                allstates.append(item)
            if col_index<len(row)-1:
                if adjacentstates[row_index][col_index+1] not in states_dictionary[item]:
                    add(states_dictionary,item,adjacentstates[row_index][col_index+1])
                    add(new_states_dictionary,item,adjacentstates[row_index][col_index+1])
                    #states_dictionary.setdefault(item,[]).
                    #states_dictionary.update({item:adjacentstates[row_index][col_index+1]})
                    #states_dictionary[item]=''childparentmap.update({ls[counter+1]:ls[i]})
                    #states_dictionary[item].append(adjacentstates[row_index][col_index+1])
            if  col_index>0:
                if adjacentstates[row_index][col_index-1] not in states_dictionary[item]:
                    add(states_dictionary,item,adjacentstates[row_index][col_index-1])
                    add(new_states_dictionary,item,adjacentstates[row_index][col_index-1])
                    
    return states_dictionary,new_states_dictionary,allstates

if __name__ == '__main__':
    start=time.time()
file_path=sys.argv[1]
if(valid_constraint_file(file_path)):
    states_dictionary,data,allstates = adjacentStates()
    #print len(allstates)
    #print len(set(allstates))
    us = {}
    us['variables'] = { state:['A', 'B', 'C', 'D'] for state in data.keys() }
    us['constraints'] = [(s1, s2, lambda x,y: x != y) for s1 in data.keys() for s2 in data[s1]]
    legacy_constraints=file_read(file_path)
    us['legacy_constraints']=legacy_constraints
    #print legacy_constraints
    for key, item in us['variables'].items():
        if key in legacy_constraints:
            del us['variables'][key]
            
    #print len(us['variables'])
    #print len(legacy_constraints)
    result,backtracks = solve(us)
    #print len(result)
    status = 'SUCCESS'
    if result == 'FAILURE':
      status = 'FAILURE'
    else:
        file_write(result)
    print status
    print "Number of backtracks:",backtracks
      
else:
    print "Unsupported format or the file doesn't exist. Please provide the file in TXT format.Please provide the filename in the format xyz.txt as the argument,where xyz is your file name"
    
end=time.time()
print end-start
