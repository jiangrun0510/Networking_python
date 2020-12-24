from simulator.node import Node
import json

class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        # creat dict of sequence number vector for the node 
        self.sequence_number = {self.id : {self.id : 0}} 
        # creat dict of link_state to neighbors
        self.link_state = {self.id: {self.id: 0}}
        # creat dict of table for the node 
        self.table = {self.id:self.id}

        #used in check function
        self.ls = {self.id: {self.id: 0}} 
        self.ls_1 = {} 
        self.seqNum = {self.id:{self.id:0}}
    

    # Return a string
    def __str__(self):
        return json.dumps({'id': self.id, 'ls': self.link_state, 'sn': self.sequence_number})
    

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        if latency == -1 and neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
        elif neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

        self.link_state[self.id][neighbor] = latency
        
        # set sequence_number of links
        if neighbor not in self.sequence_number[self.id]:
            self.sequence_number[self.id][neighbor] = 0
        else:
            self.sequence_number[self.id][neighbor] += 1

        self.recal()
        self.send_to_neighbors(json.dumps({'id': self.id, 'ls': self.link_state, 'sn': self.sequence_number}))

    
    # Fill in this function
    def process_incoming_routing_message(self, m):
        
        message = json.loads(m)
        message_id, message_ls, message_sn = int(message['id']), message['ls'], message['sn']

        self.ls = message_ls
        self.seqNum = message_sn

        # print(self.ls)
        # print(self.seqNum)

        if self.check(): 
            self.send_to_neighbors(json.dumps({'id': self.id, 'ls': self.link_state, 'sn': self.sequence_number}))

        self.recal()
    # Return a neighbor, -1 if no path to destination
    # Return distance if destination in node's distance vector
    def get_next_hop(self, destination):
        pre_node = self.table[destination]
        src_node = destination
        # print(pre_node, src_node)

        while  pre_node != self.id:
            src_node = pre_node
            if src_node in self.table:
                pre_node = self.table[src_node]
            else:
                return -1
        return src_node

    # check identifier 
    def check(self):
        # print(self.ls)
        for key, vector in self.ls.items():
            key = int(key)
            self.ls_1[key] = {}
            for dst, latency in vector.items():
                dst = int(dst)
                self.ls_1[key].update({dst: latency})
        # print(self.ls_1)
        # print(self.sequence_number)
        check_result = False
        for key, state in self.seqNum.items():
            # print(k)
            key = int(key)
            for dst, seqNum in state.items():
                # print(dst)             
                dst = int(dst)
                
                # print(self.sequence_number)
                # print(self.link_state)
                if key not in self.sequence_number:
                    self.sequence_number[key] = {}
                if key not in self.link_state:
                    self.link_state[key] = {}
                # check sequence number and update link_state
                if  key not in self.sequence_number or dst not in self.sequence_number[key] or seqNum > self.sequence_number[key][dst]:
                    self.sequence_number[key][dst] = seqNum
                    self.link_state[key][dst] = self.ls_1[key][dst]
                    # print(self.sequence_number)
                    # print(self.link_state)
                    check_result = True
        # print(self.sequence_number)
        # print(self.link_state)            
        return check_result

    # calculate self.table
    def recal(self): 
        visited = {self.id: 0}
        unvisited = []
        for next_node, dist in self.link_state.items():
            unvisited.append(next_node)
        # print(unvisited)
        # print(visited)
        while True:
            minmum = None
            for node in unvisited:
                if node in visited:
                    if minmum is None or visited[node] < visited[minmum]:
                        minmum = node
            if minmum is None:
                break

            unvisited.remove(minmum)
            distance = visited[minmum]
            # print(unvisited)
            # print(visited)
            # print(self.link_state)
            for node, cost in self.link_state[minmum].items():
                if cost >= 0:
                    new_cost = distance + cost
                    if node not in visited or new_cost < visited[node]:
                        visited[node] = new_cost
                        self.table[node] = minmum  
            # print(self.table)
            # print(visited)

            if not unvisited: 
                break 
