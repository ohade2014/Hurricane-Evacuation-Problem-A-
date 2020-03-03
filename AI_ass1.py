import Agents

def read_from_file (a):
    file=open(a,"r")
    file_by_lines= file.readlines()
    return file_by_lines

def build_graph():
    lines=read_from_file("C:\\Users\\ohadelyahu\\PycharmProjects\\Ass1_AI\\test_read_3.txt")
    adj_graph = {}
    vertex_info = {}
    for line in lines:
        if(line=="\n"):
            continue
        elif (line[:2]=="#N"):
            number_of_vertexs=line[3]
        elif (line[0:2]=="#V"):
            ###############
            row_splitted = line.split(' ')
            number_of_vertex = int(row_splitted[0][2])
            dead_line = int(row_splitted[1][1:])
            shelter = False
            number_of_pepole = 0
            if(row_splitted[2][0] == "S"):
                shelter = True
            else:
                number_of_pepole = int(row_splitted[2][1:-1])
            ###############
            '''
            number_of_vertex=int(line[2])
            dead_line= int(line[5])
            shelter=False
            number_of_pepole=0
            if(line[7]=="S"):
                shelter=True
            else:
                number_of_pepole= int(line[8])
            '''
            vertex_info[number_of_vertex]=[shelter,dead_line,number_of_pepole]
            adj_graph[number_of_vertex]=[]
        elif (line[0:2]=="#E"):
            ###############
            row_splitted = line.split(' ')
            vertex_from = int(row_splitted[1])
            vertex_to = int(row_splitted[2])
            vetex_weight = int(row_splitted[3][1:-1])
            ###############
            '''
            vertex_from=int(line[4])
            vertex_to=int(line[6])
            vetex_weight=int(line[9])
            '''
            adj_graph[vertex_from].append((vertex_to,vetex_weight))
            adj_graph[vertex_to].append((vertex_from,vetex_weight))
    return [adj_graph, vertex_info]



def main():
    #read_from_file("C:\\Users\\ohadelyahu\\PycharmProjects\\Ass1_AI\\test_read.txt");
    graphs = build_graph()
    graph = graphs[0]
    info = graphs[1]


if __name__ =="__main__":
    main()