def evaluate_postfix(expression):
    stack = []

    for ch in expression:
        if ch.isdigit():
            stack.append(int(ch))
        else:
            b = stack.pop()
            a = stack.pop()
            if ch == '+':
                stack.append(a + b)
            elif ch == '-':
                stack.append(a - b)
            elif ch == '*':
                stack.append(a * b)
            elif ch == '/':
                stack.append(int(a / b))

    return stack.pop()

# Example usage
expr = '231*+9-'
result = evaluate_postfix(expr)
print(f"Postfix Evaluation Result: {result}")
