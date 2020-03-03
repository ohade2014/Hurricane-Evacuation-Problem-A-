

class Tree_search_node:

    def __init__(self, loc, num_of_people, people_rescued, time, terminated, shelters, peop, ppl_vex, h, info):
        self.location = loc
        #self.there_is_people
        self.people_rescue_now = num_of_people
        self.people_rescued = people_rescued
        self.time = time
        self.terminated = terminated
        self.childrens = []
        self.shelters = shelters
        self.peop = peop
        self.ppl_vex = ppl_vex
        self.h = h
        self.info = info

    def __lt__(self, other):
        if self.h == other.h:
            return self.location < other.location
        else:
            return self.h < other.h
