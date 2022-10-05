def A1fromRC(r,c,r_end = None,c_end = None):
    start:str
    end:str
    iterable:list = [c]
    if r_end is not None and c_end is not None:
        iterable.append(c_end)
    for c in iterable:    
        result:str = ''
        n = 2
        m = 1
        while c > 0:
            if c <= 26: 
                result += chr(ord("@")+c)
                c -= c
            elif c <= 26*n:
                result += chr(ord("@")+((c-1) // 26))
                c -= 26* (n-1)
            elif c <= pow(26,m)*n
            else:
                pass
                n += 1
    return result+str(r)

if __name__ == "__main__":
    # print(A1fromRC(1,28))
    for i in range(0,pow(27,2)-26):
        print(A1fromRC(1,i))