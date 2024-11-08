import random
import string

class Person:
    def __init__(self, name, ticket, priority):
        self.name = name
        self.ticket = ticket
        self.priority = priority
        self.next = None

class Queue:
    def __init__(self):
        self.start = None
        self.end = None

def generate_random_ticket():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def add_person(queue, name, priority):
    new_person = Person(name, generate_random_ticket(), priority)
    
    if queue.start is None:  # Queue is empty
        queue.start = new_person
        queue.end = new_person
    else:
        if priority:
            current = queue.start
            previous = None
            next_node = current.next
            found_priority_block = False
            add_to_start = True
            
            # Traverse to find the last priority block
            while next_node is not None and not found_priority_block:
                # Check for a block of priority followed by non-priority
                if current.priority and (previous is None or not previous.priority) and not next_node.priority:
                    found_priority_block = True
                    add_to_start = False
                else:
                    if current.priority:
                        add_to_start = False
                    # Move to the next node
                    previous = current
                    current = next_node
                    next_node = next_node.next
            
            if found_priority_block:
                current.next = new_person
                new_person.next = next_node
            else:
                if add_to_start:
                    aux = queue.start
                    queue.start = new_person
                    new_person.next = aux
                else:
                    # Final case: add between two non-priority blocks if no suitable priority block is found
                    current = queue.start
                    next_node = current.next
                    previous = None
                    insertion_found = False
                    while next_node is not None and not insertion_found:
                        if not current.priority and (not next_node.priority or next_node is None) and (not previous.priority or previous is None):
                            insertion_found = True
                        else:
                            previous = current
                            current = next_node
                            next_node = next_node.next
                    if insertion_found:
                        current.next = new_person
                        new_person.next = next_node
                    else:
                        queue.end.next = new_person
                        queue.end = new_person
        else:  # Non-priority person
            queue.end.next = new_person
            queue.end = new_person

def remove_person(queue):
    if queue.start is not None:
        to_remove = queue.start
        queue.start = queue.start.next
        if queue.start is None:
            queue.end = None
        del to_remove

def next_person(queue):
    if queue.start is not None:
        return queue.start.name
    else:
        return "Queue is empty"

# Usage Example
queue = Queue()
add_person(queue, "Cyclops", False)
add_person(queue, "Jean Grey", True)
add_person(queue, "Storm", False)
add_person(queue, "Wolverine", True)
add_person(queue, "Professor X", False)
add_person(queue, "Beast", True)
add_person(queue, "Nightcrawler", False)
add_person(queue, "Colossus", True)

# Processing the queue
while queue.start is not None:
    print(next_person(queue))
    remove_person(queue)

# Expected output order:
# Jean Grey, Wolverine (priority block 1)
# Cyclops, Storm (non-priority block 2)
# Beast, Colossus (priority block 3)
# Professor X, Nightcrawler (non-priority block 4)
