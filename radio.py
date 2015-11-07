'''
Created on 03-Nov-2015

@author: debasis
'''
import sys
import mimetypes

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
            it = iter(words)
            legacy_constraints.update(dict(zip(it, it)))
    return legacy_constraints
            
'''Check Input constraint file'''
def valid_constraint_file(file):
    if mimetypes.guess_type(file)[0] == 'text/plain':
        return True
    else:
        return False

             
def adjacentStates():
    states_dictionary={}
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
            if item not in allstates:
                states_dictionary.setdefault(item,[])
                allstates.append(item)
            if col_index<len(row)-1:
                if adjacentstates[row_index][col_index+1] not in states_dictionary[item]:
                    add(states_dictionary,item,adjacentstates[row_index][col_index+1])
                    #states_dictionary.setdefault(item,[]).
                    #states_dictionary.update({item:adjacentstates[row_index][col_index+1]})
                    #states_dictionary[item]=''childparentmap.update({ls[counter+1]:ls[i]})
                    #states_dictionary[item].append(adjacentstates[row_index][col_index+1])
            if  col_index>0:
                if adjacentstates[row_index][col_index-1] not in states_dictionary[item]:
                    add(states_dictionary,item,adjacentstates[row_index][col_index-1])
                    
    return states_dictionary,allstates
                    
                    
def check_valid(graph):
    for node,nexts in graph.iteritems():
        assert(node not in nexts) # # no node linked to itself
        for next in nexts:
            assert(next in graph and node in graph[next]) # A linked to B implies B linked to A

def check_solution(graph, solution):
    if solution is not None:
        for node,nexts in graph.iteritems():
            assert(node in solution)
            frequency = solution[node]
            for next in nexts:
                assert(next in solution and solution[next] != frequency)

def find_best_candidate(graph, guesses):
    if True: #optimised
        # Optimisations are to be put here. Ideas would be to take the node with the most uncolored neighboors or the one with the smallest possible number of frequencies or both
        candidates_with_add_info = [
            (
            -len({guesses[neigh] for neigh in graph[n] if neigh     in guesses}), # nb_forbidden_colors
            -len({neigh          for neigh in graph[n] if neigh not in guesses}), # minus nb_uncolored_neighbour
            n
            ) for n in graph if n not in guesses]
        candidates_with_add_info.sort()
        candidates = [n for _,_,n in candidates_with_add_info]
        #candidates=['Tennessee', 'Missouri', 'Pennsylvania', 'Colorado', 'Wyoming', 'Massachusetts', 'South_Dakota', 'Idaho', 'Arizona', 'Wisconsin', 'Indiana', 'Kentucky', 'Georgia', 'Arkansas', 'Texas', 'Oklahoma', 'Oregon', 'New_York', 'Maryland', 'Iowa', 'Minnesota', 'West_Virginia', 'Virginia', 'Alabama', 'Mississippi', 'Nevada', 'New_Hampshire', 'Vermont', 'Maine', 'Nebraska', 'Kansas', 'Connecticut', 'Rhode_Island', 'Delaware', 'New_Jersey', 'North_Carolina', 'South_Carolina', 'Montana', 'Michigan', 'Ohio', 'North_Dakota', 'Alaska', 'Florida', 'Louisiana', 'California', 'Utah', 'New_Mexico', ' Nevada', 'Hawaii', 'Illinois', 'Washington']
        #print (candidates)
        #print guesses
    else:
        candidates = [n for n in graph if n not in guesses]
        candidates.sort() # just to have some consistent performances
    if candidates:
        candidate = candidates[0]
        assert(candidate not in guesses)
        return candidate
    #assert(set(graph.keys()) == set(guesses.keys()))
    return None

nb_calls = 0

def solve(graph, frequencies, guesses, depth):
    global nb_calls
    #nb_calls += 1
    n = find_best_candidate(graph, guesses)
    if n is None:
        return guesses # Solution is found
    for c in frequencies - {guesses[neigh] for neigh in graph[n] if neigh in guesses}:
        assert(n not in guesses)
        assert(all((neigh not in guesses or guesses[neigh] != c) for neigh in graph[n]))
        guesses[n] = c
        indent = '  '*depth
        #print "%sTrying to give frequency %s to %s" % (indent,c,n)
        if solve(graph, frequencies, guesses, depth+1):
            #print "%sGave frequency %s to %s" % (indent,c,n)
            return guesses
        else:
            del guesses[n]
            #print "%sCannot give frequency %s to %s" % (indent,c,n)
            nb_calls += 1
    return None


def solve_problem(graph, frequencies,legacy_constraints):
    check_valid(graph)
    solution = solve(graph, frequencies, legacy_constraints, 0)
    check_solution(graph,solution)
    return solution

#Read the constraint file
file_path=sys.argv[1]
if(valid_constraint_file(file_path)):
    united_stated_of_america,allstates=adjacentStates()
    #print united_stated_of_america["Michigan"]
    united_stated_of_america = {n:neigh for n,neigh in united_stated_of_america.iteritems() if neigh}
    frequencies  = {'A', 'B', 'C', 'D'}
    legacy_constraints=file_read(file_path)
    #print legacy_constraints
    solution=solve_problem(united_stated_of_america, frequencies,legacy_constraints)
    
    if solution:
        print len(solution)
        file_write(solution) 
    else:
        print "No solution found\n"
    print "Number of backtracks :" ,nb_calls
else:
    print "Unsupported format or the file doesn't exist. Please provide the file in TXT format.Please provide the filename in the format xyz.txt as the argument,where xyz is your file name"

