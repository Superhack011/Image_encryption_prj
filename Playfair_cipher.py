import numpy as np 
import time

start_time = time.time()

keyword = input("Enter the key : ")
message = input("Enter the plaintext : ")

# print("Keyword : ",keyword)
# print("Message : ", message)

matrix = []
keyword = keyword.replace(" ","").upper()

for ch in keyword:
    if ch not in matrix:
        matrix.append(ch)

ch = 'A'
while(ord(ch) < 91):
    if ch not in matrix:
        if ch != 'J': matrix.append(ch)

    ch = chr(ord(ch) + 1)

# print(matrix)

for i in message:
    message = message.replace(" ","").upper()

# print(message)

# print(len(message))

def encryption(p,q):
    if ((p//5) == (q//5)):
        p = p + 1
        q = q + 1
        if (p%5 == 0): p = p - 5;
        if (q%5 == 0): q = q - 5
    elif (p%5) == (q%5):
        p = (p+5)%25
        q = (q+5)%25
    else :
        if (p%5) < (q%5):
            temp = (q%5) - (p%5);
            p = p + temp
            q = q - temp
            # print(p,q)
        else :
            temp = (p%5) - (q%5);
            p = p - temp
            q = q + temp
    ans = matrix[p] + matrix[q]
    return ans

result = ""
i = 0;
while ( i < (len(message)-1)):
    x = message[i]
    y = message[i+1]

    if x != y:
        p = matrix.index(x)
        q = matrix.index(y)

        result += encryption(p,q)

        i+=2
    else : 
        p = matrix.index(x)
        q = matrix.index('X')

        result += encryption(p,q)

        i+=1

if i == len(message)-1 :
    # print(message[i])
    
    p = matrix.index(message[i])
    q = matrix.index('X')
    result += encryption(p,q)

end_time = time.time()

execution_time = end_time - start_time

print(f"The cipher text is : {result}")
print(f"The execution time of the program is {execution_time}.")