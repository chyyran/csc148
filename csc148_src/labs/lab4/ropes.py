from stack import Stack


def input_rope():
    undo = Stack()
    rope = Stack()
    input_val = ''
    while not input_val == 'EXIT':
        input_val = input('Enter a string: ')
        if input_val == 'UNDO':
            if not rope.is_empty():
                value = rope.pop()
                print(value)
                undo.push(value)
            else:
                print('Nothing to undo.')
        elif input_val == 'REDO':
            if not undo.is_empty():
                value = undo.pop()
                print(value)
                rope.push(value)
            else:
                print('Nothing to redo')
        else:
            rope.push(input_val)

    reverse(rope)

    while not rope.is_empty():
        print(rope.pop())


def reverse(stack: Stack) -> None:
    """Reverse all the elements of <stack>.

    Do nothing if the stack is empty.

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> reverse(stack)
    >>> stack.pop()
    1
    >>> stack.pop()
    2
    """
    temp = Stack()
    temp2 = Stack()
    while not stack.is_empty():
        temp.push(stack.pop())

    while not temp.is_empty():
        temp2.push(temp.pop())

    while not temp2.is_empty():
        stack.push(temp2.pop())

if __name__ == '__main__':
    input_rope()