import math
import Tree_search_node
import copy
import queue
import Simulator

class Agent:

    def __init__(self, loc, k, t):
        self.location = loc
        self.people_rescue_now = 0  # Number of people the Agent Holds
        self.total_rescue = 0
        self.time = 0
        self.terminating = False  # is Agent Terminated
        self.score = 0
        self.k = k
        self.t = t

    def terminate(self, info, k):
        # Loop counts all people that not on the agent and not been rescued
        not_rescue = 0
        for v in info:
            if info[v][2] != 0:
                not_rescue += info[v][2]

        # Calculate final score of the agent
        res = self.total_rescue - (not_rescue + 2*self.people_rescue_now + k)
        self.terminating = True
        self.score = res

    # abstract function defined in each agent
    def traverse(self, graph, info):
        pass


class Human (Agent):
    def __init__(self, loc, k, t):
        super().__init__(loc, k, t)

    def print_state(self, info):
        print("Location: " + str(self.location))
        print("People in the car: " + str(self.people_rescue_now))

        # Loop prints where there are people
        print("vertex with people: ")
        for v in info:
            if info[v][2] > 0:
                print("V" + str(v) + " : " + str(info[v][2]))

        print("Total people rescue:" + str(self.total_rescue))
        print("The time is: " + str(self.time))
        if self.terminating:
            print("Agent is terminate")
        else:
            print("Agent still in progress")

    # Ask from the user to insert the next move
    # The function assumes that the next move is neighbour of the current location
    def traverse(self, graph, info):
        self.print_state(info)
        next_move = int(input("please inset next move: "))
        return next_move


class Greedy (Agent):

    def __init__(self, loc, k, t):
        super().__init__(loc, k, t)

    def traverse(self, graph, info):
        # Calculate minimum distance from source to each other vertices
        source = self.location
        dist_prev = self.dijkstra(graph, source)
        dist = dist_prev[0]
        prev = dist_prev[1]

        # Find the next vertex to move to
        min_vet = source
        min_dis = math.inf
        for v in dist:
            # if agent not carrying people search for a vertex with people
            if self.people_rescue_now == 0:
                if info[v][2] != 0:
                    if min_dis > dist[v]:
                        min_vet = v
                        min_dis = dist[v]

            # If agent does carrying people search for a shelter
            else:
                if info[v][0]:
                    if min_dis > dist[v]:
                        min_vet = v
                        min_dis = dist[v]
        if min_vet == source:
            return [-1]
        else:
            return [prev, min_vet]

    '''    
    def dijkstra(self, graph, source):
        heap = set()
        dist = {}
        prev = {}
        for v in graph:
            if v == source:
                dist[source] = 0
            else:
                dist[v] = math.inf
            heap.add(v)
            prev[v] = None

        while len(heap) > 0:
            min_dist = math.inf
            key_min = source

            for h in heap:
                if dist[h] < min_dist:
                    min_dist = dist[h]
                    key_min = h

            u = key_min
            heap.remove(u)

            for v in graph[u]:
                alt = dist[u] + v[1]
                if alt < dist[v[0]]:
                    dist[v[0]] = alt
                    prev[v[0]] = u

        return [dist, prev]
        '''


class Vandal(Agent):

    def __init__(self, loc, k, t):
        super().__init__(loc, k, t)

    def traverse(self, graph, info):
        # Find lowest cost of neighbours edges and return it to be destroyed
        loc = self.location
        min_cost = math.inf
        min_vet = loc
        for v in graph[loc]:
            if min_cost > v[1]:
                min_vet = v[0]
                min_cost = v[1]
        return [min_cost, min_vet]



class A_star_real_time_tree_search (Agent):
    def __init__(self, loc, k, t):
        print("How much expansion do you allowed to your agent? ")
        self.limit = int(input())
        super().__init__(loc, k, t)

    def traverse(self, graph, info):
        source = self.location
        search_tree = Build_search_tree(graph, info, source, True, self.k, self.t, self.limit, True, [])
        while isinstance(search_tree, list):
            search_tree[0].time += self.t * self.limit
            search_tree = Build_search_tree(graph, info, search_tree[0].location, True, self.k, self.t, self.limit, True, search_tree[0])

        q2 = queue.PriorityQueue()
        q2.put(search_tree)
        curr = q2.get()

        while isGoalState(curr) == False:
            for ch in curr.childrens:
                q2.put(ch)
            curr = q2.get()
        # calculate score of the agent
        search_tree = curr
        sum_ppl = 0
        for ppl in search_tree.ppl_vex:
            sum_ppl += info[ppl][2]
        k = self.k
        if info[search_tree.location][0] and search_tree.time <= info[search_tree.loaction][1]:
            k = 0
        score = search_tree.people_rescued - (
                    search_tree.people_rescue_now * 2 + sum_ppl + k)  # @@@ need to add the k
        return score

class A_star_tree_search (Agent):
    def __init__(self, loc, k, t):
        super().__init__(loc, k, t)

    def traverse(self, graph, info):
        source = self.location
        search_tree = Build_search_tree(graph, info, source, True, self.k, self.t, 100000, False, [])
        if search_tree == "fail":
            return "fail"

        q2 = queue.PriorityQueue()
        q2.put(search_tree)
        curr = q2.get()

        while isGoalState(curr) == False:
            for ch in curr.childrens:
                q2.put(ch)
            curr = q2.get()

        # Search in the tree we build above and start going on the path from the tree result
        '''
        while isGoalState(search_tree) == False:
            # If the time expired and the step is illegal, break
            if search_tree.time > info[search_tree.location][1]:
                break

            # If step is Legal find the next state according to the tree result
            is_all_ter = True
            for ch in search_tree.childrens:
                if len(ch.childrens) > 0:
                    search_tree = ch
                    is_all_ter = False
                    break

            # in case the next move is for terminate
            if is_all_ter:
                search_tree = search_tree.childrens[-1]
        '''
        # calculate score of the agent
        search_tree = curr
        sum_ppl = 0
        for ppl in search_tree.ppl_vex:
            sum_ppl += info[ppl][2]
        k = self.k
        if info[search_tree.location][0]:
            k = 0
        score = search_tree.people_rescued - (search_tree.people_rescue_now * 2 + sum_ppl + k)  # @@@ need to add the k
        return score

class Greedy_tree_search (Agent):

    def __init__(self,loc, k, t):
        super().__init__(loc, k, t)

    def traverse(self, graph, info):
        source = self.location
        search_tree = Build_search_tree(graph, info, source, False, self.k, self.t, 0, False, [])
        if search_tree == "fail":
            return "fail"
        # Search in the tree we build above and start going on the path from the tree result
        while isGoalState(search_tree) == False:
            # If the time expired and the step is illegal, break
            if search_tree.time > info[search_tree.location][1]:
                break

            # If step is Legal find the next state according to the tree result
            is_all_ter = True
            for ch in search_tree.childrens:
                if len(ch.childrens) > 0:
                    search_tree = ch
                    is_all_ter = False
                    break

            # in case the next move is for terminate
            if is_all_ter:
                search_tree = search_tree.childrens[-1]

        # calculate score of the agent
        sum_ppl = 0
        for ppl in search_tree.ppl_vex:
            sum_ppl += info[ppl][2]
        k = self.k
        if info[search_tree.location][0]:
            k = 0
        score = search_tree.people_rescued - (search_tree.people_rescue_now*2 + sum_ppl + k) #@@@ need to add the k
        return score


def dijkstra(graph, source):
    heap = set()
    dist = {}
    prev = {}
    # Initialize all maps and variables
    for v in graph:
        if v == source:
            dist[source] = 0
        else:
            dist[v] = math.inf
        heap.add(v)
        prev[v] = None

    # Implement dijkstra
    while len(heap) > 0:
        min_dist = math.inf
        key_min = source

        for h in heap:
            if dist[h] < min_dist:
                min_dist = dist[h]
                key_min = h

        u = key_min
        heap.remove(u)

        for v in graph[u]:
            alt = dist[u] + v[1]
            if alt < dist[v[0]]:
                dist[v[0]] = alt
                prev[v[0]] = u

    return [dist, prev]


def expand_node(tree_state, info, graph, is_a_star, k, t):
    # Initial new state properties
    for v in graph[tree_state.location]:
        people_rescued = tree_state.people_rescued
        loc = v[0]
        num_of_people = tree_state.people_rescue_now
        if loc in tree_state.ppl_vex:
            num_of_people += info[loc][2]
        ppl_vex = copy.deepcopy(tree_state.ppl_vex)
        if loc in ppl_vex:
            ppl_vex.remove(loc)
        w = 0
        for e in graph[tree_state.location]:
            if e[0] == loc:
                w = e[1]
                break
        if info[loc][0] and tree_state.time + w <= info[loc][1]:
            people_rescued += num_of_people
            num_of_people = 0

        for e in graph[tree_state.location]:
            if e[0] == loc:
                time = tree_state.time + e[1]
                break
        if is_a_star == False:
            time += t# add expand time in case we are in greedy agent
        # ---- H value calculate ----
        sum_ppl = 0
        # Calculate total number of people in all world
        for p in info:
            sum_ppl += info[p][2]

        ppl_resc = people_rescued
        if info[loc][1] >= time:
            # Calculate how much people can be rescued
            for pe in tree_state.peop[loc]:
                if pe[0] in ppl_vex:
                    for shelter in tree_state.shelters[pe[0]]:
                        if time + pe[1] + shelter[1] <= info[shelter[0]][1] and time + pe[1] <= info[pe[0]][1]:
                            ppl_resc += info[pe[0]][2]
                            break

            # Calculate if the people on the car can be rescued
            for shelter in tree_state.shelters[loc]:
                if time + shelter[1] <= info[shelter[0]][1]:
                    ppl_resc += num_of_people
                    break

        h = sum_ppl - ppl_resc
        # Create the new node
        if time <= info[loc][1]:
            new_tree = Tree_search_node.Tree_search_node(loc, num_of_people, people_rescued, time, False, tree_state.shelters, tree_state.peop, ppl_vex, h, info)
        else:
            if is_a_star:
                res = 0
                for p in tree_state.ppl_vex:
                    res += info[p][2]
                res += tree_state.people_rescue_now * 2 + k
                h += res
            else:
                h = sum_ppl - tree_state.people_rescued
            new_tree = Tree_search_node.Tree_search_node(loc, tree_state.people_rescue_now, tree_state.people_rescued, time, True, tree_state.shelters, tree_state.peop, tree_state.ppl_vex, h, info)
        tree_state.childrens.append(new_tree)

    # Calculate final h value
    if info[tree_state.location][0]:
        ppl_resc = (tree_state.people_rescued + tree_state.people_rescue_now)
        h = sum_ppl - ppl_resc
    else:
        h = sum_ppl - tree_state.people_rescued
    if is_a_star:
        res = 0
        for p in tree_state.ppl_vex:
            res += info[p][2]
        if info[tree_state.location][0] == False:
            res += tree_state.people_rescue_now*2 + k
        h += res

    if h == tree_state.h:
        h -= 1
    tree_state.childrens.append(Tree_search_node.Tree_search_node(tree_state.location, tree_state.people_rescue_now, tree_state.people_rescued, tree_state.time, True, tree_state.shelters, tree_state.peop, tree_state.ppl_vex, h, info))


def Build_search_tree(graph, info, locat, is_a_star, k, t, limit, is_a_star_real_time, root):

    number_of_expnsion = 0
    # Map of List of pairs which each key is vertex
    # and the value is List of the distances from the key vertex to all vertices that are shelters
    shel_info = {}

    # Map of List of pairs which each key is vertex
    # and the value is List of the distances from the key vertex to all vertices with people
    peop_info = {}

    # List of vertices which has people at the moment
    ppl_vex = []

    # Initialize all Maps above
    for v in info:
        if info[v][2] != 0:
            ppl_vex.append(v)
        dij_v = dijkstra(graph, v)
        dist = dij_v[0]
        peop_info[v] = []
        shel_info[v] = []
        for i in range(1, len(dist) + 1):
            if info[i][0]:
                shel_info[v].append([i, dist[i]])
            elif info[i][2] != 0:
                peop_info[v].append([i, dist[i]])

    # create node from the next level in the tree
    if isinstance(root, list):
        ppl_vex.remove(locat)
        tree = Tree_search_node.Tree_search_node(locat, info[locat][2], 0, t * limit, False, shel_info, peop_info, ppl_vex, 0, info)
    else:
        tree = root
    q = queue.PriorityQueue()
    q.put(tree)
    state = q.get()

    # expand tree until we get goal state, use priority queue to take each time the lowest heiuristic value
    if is_a_star_real_time:
        while (isGoalState(state) != True) and number_of_expnsion < limit:
            number_of_expnsion += 1
            expand_node(state, info, graph, is_a_star, k, t)
            for child in state.childrens:
                q.put(child)
            state = q.get()
        if number_of_expnsion == limit and (isGoalState(state) != True):
            return [state]
        else:
            return tree
    else:
        while isGoalState(state) != True:
            if number_of_expnsion == limit and is_a_star:
                return "fail"
            expand_node(state, info, graph, is_a_star, k, t)
            for child in state.childrens:
                q.put(child)
            state = q.get()
        return tree

def isGoalState(state):
    return (len(state.ppl_vex) == 0 and state.people_rescue_now == 0) or state.terminated








