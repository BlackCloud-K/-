def bracket(string):
    stack_l = []
    stack_r = []
    result = [' '] * len(string)

    for i in range(len(string)):
        char = string[i]
        if char == '(':
            stack_l.append(i)
        elif char == ')':
            if stack_l:
                stack_l.pop()
            else:
                stack_r.append(i)

    for j in range(len(stack_l)):
        result[stack_l[j]] = 'x'

    for k in range(len(stack_r)):
        result[stack_r[k]] = '?'

    ans = ''.join(result)
    return ans


input_string = input("Input a string：")
print(bracket(input_string))
