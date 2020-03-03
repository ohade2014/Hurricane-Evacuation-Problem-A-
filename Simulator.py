import AI_ass1
import Agents
import math
global_k = 0

# function that moves agent to the next step - human and greedy
def human_fun (next_move, agent, w, info, k, terminated, time_to_execute, counter):
    agent.location = next_move
    agent.time += w
    if info[next_move][1] < agent.time:
        agent.terminate(info, k)
        terminated[0] = terminated[0] + 1
        time_to_execute[counter] = math.inf
    else:
        if info[next_move][0]:
            agent.total_rescue += agent.people_rescue_now
            agent.people_rescue_now = 0
        else:
            agent.people_rescue_now += info[next_move][2]
            info[next_move][2] = 0


# function that terminates the greedy agent
def Greedy_fun(agents, counter, info, k, terminated):
    agents[counter].terminate(info, k)
    terminated[0] += 1


# function that moves vandal to the next step
def vandal_fun(agents, counter, next_vet):
    agents[counter].location = next_vet


def main():
    graphs = AI_ass1.build_graph()
    graph = graphs[0]
    info = graphs[1]
    agents = []
    time_to_excute = []
    lambdas_to_execute = []
    limit = 10000

    print("Hi man how much human Agents do yo want to initialize? ")
    humans = int(input())
    print("Hi again how much greedy Agents do yo want to initialize? ")
    greedys = int(input())
    print("We almost done!! how much Vandal Agents do yo want to initialize? ")
    vandals = int(input())
    print("Gutcha! we added more agents! with AI!!! how much greedy AI agents do you want to initialize?")
    greedy_AI = int(input())
    print("Last but not least cheer for our special guest the A* , how much A* AI agents do you want to initialize?")
    a_star_AI = int(input())
    print("Do you know A* big brother? the A* real time , how much A* real time AI agents do you want to initialize?")
    a_star_AI_real = int(input())

    print("for the Ai agent what is the time for each expansion?")
    t = float(input())
    print("Last thing! enter K value for penalties")
    k = int(input())

    counter = 0
    for i in range(humans):
        print("Where human agent number " + str(i) + " will start")
        pos = int (input())
        agents.append(Agents.Human(pos, k, 0))
        time_to_excute.append(0)
        lambdas_to_execute.append(lambda: 1)
        counter += 1

    for i in range(greedys):
        print("Where greedy agent number " + str(i) + " will start")
        pos = int(input())
        agents.append(Agents.Greedy(pos, k, 0))
        time_to_excute.append(0)
        lambdas_to_execute.append(lambda: 1)
        counter += 1

    for i in range(vandals):
        print("Where vandal agent number " + str(i) + " will start")
        pos = int(input())
        agents.append(Agents.Vandal(pos, k, 0))
        time_to_excute.append(0)
        lambdas_to_execute.append(lambda: 1)
        counter += 1

    for i in range(greedy_AI):
        print("Where greedy ai agent number " + str(i) + " will start")
        pos = int(input())
        agents.append(Agents.Greedy_tree_search(pos, k, t))
        time_to_excute.append(0)
        lambdas_to_execute.append(lambda: 1)
        counter += 1
    for i in range(a_star_AI):
        print("Where a* ai agent number " + str(i) + " will start")
        pos = int(input())
        agents.append(Agents.A_star_tree_search(pos, k, t))
        time_to_excute.append(0)
        lambdas_to_execute.append(lambda: 1)
        counter += 1
    for i in range(a_star_AI_real):
        print("Where a* real time ai agent number " + str(i) + " will start")
        pos = int(input())
        agents.append(Agents.A_star_real_time_tree_search(pos, k, t))
        time_to_excute.append(0)
        lambdas_to_execute.append(lambda: 1)
        counter += 1

    counter = 0
    terminated = [0]
    while len(agents) > terminated[0]:
        if agents[counter].terminating == False:
            weight = 0
            if time_to_excute[counter] == 0:

                # execute lambda
                lambdas_to_execute[counter]()

                if agents[counter].terminating == False:
                    if len(agents) == terminated[0]:
                        break

                    # calculate next move
                    next_move = agents[counter].traverse(graph, info)
                    if next_move == "fail":
                        print("The search failed")
                        exit(0)

                    # create appropriate lambda of human agent and update time and lambda lists
                    if isinstance(agents[counter], Agents.Human):
                        for edge in graph[agents[counter].location]:
                            if edge[0] == next_move:
                                weight = edge[1]
                                fun = lambda weight = weight, next_move=next_move, counter = counter: human_fun(next_move, agents[counter], weight, info, k, terminated, time_to_excute, counter)
                                lambdas_to_execute[counter] = fun
                                time_to_excute[counter] = weight
                                break

                    # create appropriate lambda of greedy agent and update time and lambda lists
                    elif isinstance(agents[counter], Agents.Greedy):
                        if len(next_move) == 1:
                            agents[counter].terminate(info, k)
                            time_to_excute[counter] = math.inf
                        else:
                            # Calculate the road calculated in dijkstra
                            curr = next_move[1]
                            road = []
                            while curr != agents[counter].location:
                                    road.append(curr)
                                    curr = next_move[0][curr]
                            road.append(agents[counter].location)
                            total_time = 0
                            road.reverse()

                            for i in range(1, len(road)):
                                # find next vertex to go to
                                v=road[i]
                                for u in graph[road[i-1]]:
                                    if u[0] == road[i]:
                                        w1 = u[1]
                                        break

                                # if agent should terminate
                                if agents[counter].time + total_time + w1 > info[v][1]:
                                    fun = lambda counter = counter: Greedy_fun(agents, counter, info, k, terminated)
                                    time_to_excute[counter] = total_time + w1
                                    break
                                else :
                                    total_time += w1

                            # if step can be done, do it as its a human agent
                            if time_to_excute[counter] == 0:
                                fun = lambda total_time = total_time, counter = counter, next_move=next_move[1] : human_fun(next_move, agents[counter], total_time, info, k, terminated, time_to_excute, counter)
                                time_to_excute[counter] = total_time

                            lambdas_to_execute[counter] = fun

                    # create appropriate lambda of vandal search agent agent and update time and lambda lists
                    elif isinstance(agents[counter], Agents.Vandal):
                        for p in graph[agents[counter].location]:
                            if p == next_move[1]:
                                del p
                                break
                        for pi in graph[next_move[1]]:
                            if pi == agents[counter].location:
                                del pi
                                break
                        next_move2 = agents[counter].traverse(graph, info)
                        fun = lambda: vandal_fun(agents, counter, next_move2[1])
                        time_to_excute[counter] = next_move2[0]
                        lambdas_to_execute[counter] = fun

                    # calculate the result of the search tree made by search greedy agent
                    elif isinstance(agents[counter], Agents.Greedy_tree_search):
                        agents[counter].score = next_move
                        terminated[0] += 1
                    elif isinstance(agents[counter], Agents.A_star_tree_search):
                        agents[counter].score = next_move
                        terminated[0] += 1
                    elif isinstance(agents[counter], Agents.A_star_real_time_tree_search):
                        agents[counter].score = next_move
                        terminated[0] += 1

            else:
                time_to_excute[counter] -= 1
        counter += 1
        counter %= len(agents)

    for a in agents:
        print("The score is" + str(a.score))


if __name__ == "__main__":
    main()