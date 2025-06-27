class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return

        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def display(self):
        temp = self.head
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")

    def reverse(self):
        prev = None
        curr = self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

# Main code with user input
ll = LinkedList()

n = int(input("Enter number of values to append: "))
for i in range(n):
    val = int(input(f"Enter value {i+1}: "))
    ll.append(val)

print("\nOriginal Linked List:")
ll.display()

ll.reverse()
print("Reversed Linked List:")
ll.display()