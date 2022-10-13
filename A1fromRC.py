##
# @file A1fromRC.py
# @author Ben Parnas
# @brief contains methods for converting collumns and rows to A1 notation

def A1fromRC(r,c,r_end = None,c_end = None):
    """!
    Converts a grid region of rows and columns to A1 notation. 
    Either locates a single cell, or a region of cels using start and stop
    values. 

    @param r the row to return, or lesser row if region
    @param c the collumn to return, or lesser collumn if region
    @param r_end if getting region, the larger row
    @param c_end if getting regions, the larger collumn
    @return a string with the cell, or region, in "A1" or "A1:Z1" notation 
    """
    start:str
    end:str
    iterable:list = [c]
    result_range:list(str)=[]
    #add the end regions if they are used
    if r_end is not None and c_end is not None:
        iterable.append(c_end)
    for c in iterable:    
        result:str = ''
        
        n = 2
        m = 1
        while c > 0:
            #select the value directly if in the range of the alphabet
            # if not, scale to the next letter
            #A-Z
            if c <= 26: 
                result += chr(ord("@")+c)
                c -= c
            #AA-ZZ
            elif c > 26 and c <= 26*n:
                result += chr(ord("@")+((c-1) // 26))
                c -= 26* (n-1)
            #AAA-ZZZ
            elif c > pow(26,2)+26 and c <= pow(26,2)*m:
                result += chr(ord("@")+((c-1) // pow(26,2)))
                c = c - pow(26,2) * (m-1)
            #keep counting up
            else:
                n += 1
                if n == 28:
                    m += 1
                    n = 2
                    if m >= 27:
                        raise RuntimeError("RC to A1: number of columns exceeded")
        result_range.append(result)
    if len(result_range) > 1:
        return (result_range[0]+str(r)+":"+result_range[-1]+str(r_end))
    else:
        return result_range[0]

if __name__ == "__main__":
    # print(A1fromRC(1,28))
    for i in range(700, 1710,10):
        print("{}:{}".format(i,A1fromRC(1,1,i,i)))
