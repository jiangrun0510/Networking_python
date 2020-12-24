from simulator.node import Node
import json

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        # creat dict of distance vector for the node 
        self.distance_vector = {self.id: [0, self.id]}
        # creat dict of distance amount value to neighbors
        self.old_val = {self.id:[0, self.id]}
        # creat dict of other nodes' distance vector 
        self.otherdv = {}
        # sequence number
        self.seqNum = {self.id: 0}

    def __str__(self):
        return json.dumps({'id':self.id, 'distance_vector':self.distance_vector,'sn':self.seqNum[self.id]})
        
    
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        if latency == -1 and neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
        else:
            self.neighbors.append(neighbor)
            self.old_val[neighbor] = [latency, neighbor]

        if self.recal():
            self.seqNum[self.id] += 1
            self.send_to_neighbors(json.dumps({'id':self.id,'distance_vector':self.distance_vector, 'sn':self.seqNum[self.id]}))
        # print(self.seqNum)

    def process_incoming_routing_message(self, m):
        message = json.loads(m)
        message_id, message_distance_vector, message_sn = int(message['id']), message['distance_vector'], message['sn']
        if message_id in self.seqNum:
            if message_sn < self.seqNum[message_id]:
                return 1
        else:
            self.seqNum[message_id] = message_sn    

        self.otherdv[message_id] = message_distance_vector
        #print(message_sn[self.id])
        #print(self.seqNum[message_id])
        
        if self.recal():
            self.seqNum[self.id] += 1
            # print(self.id, self.old_val)
            self.send_to_neighbors(json.dumps({'id':self.id, 'distance_vector':self.distance_vector, 'sn':self.seqNum[self.id]}))

    # Return a neighbor, -1 if no path to destination
    # Return distance if destination in node's distance vector
    def get_next_hop(self, destination):
        if destination in self.distance_vector:
            return self.distance_vector[destination][1]

        else:
            return -1
    # recalcute dv table
    def recal(self):
        new_distance_vector = dict(self.old_val)
        #print(new_distance_vector)
        # print(self.otherdv)
        # print(self.distance_vector[self.id])

        for neighbor_node, neighbor_distance_vector in self.otherdv.items():
            #print(neighbor,new_distance_vector)
            #print(neighbor_distance_vector)
            for destination_id, destination_vector in neighbor_distance_vector.items():
                destination_id = int(destination_id)
                if neighbor_node in self.old_val:
                    distance = self.old_val[neighbor_node][0] + destination_vector[0]
                  
                else:
                    distance =10000
                # print(destination_id,destination_vector)
                if destination_id not in new_distance_vector or distance < new_distance_vector[destination_id][0]:
                    

                    new_distance_vector[destination_id] = [distance, neighbor_node]
                    #print(new_distance_vector)
        #recalculate the table and replace with new one if True
        if new_distance_vector != self.distance_vector:
            recalculate = True
            # print(1)
        else:
            recalculate = False
            # print(2)
        self.distance_vector = new_distance_vector
        #print('     ')
        return recalculate




