# fineMeshPath = r"C:\Users\WeiGo\Desktop\New Folder\primal\primal_Venus.off"
fineMeshPath = r"C:\Users\WeiGo\Desktop\Venus分解\dual\dual_Venus.off"
rsub = 5
rave = 1
weight = [1/2]
# weight = [3/4, 1/3]

from primal_averaging import reverse_averaging as ra
from primal_faceSplit import reverse_faceSplit as rf, refine_reverse_faceSplit as rrf
from preparation import primal_Info as pi, dual_info as di
from dual_averaging import reverse_averaging as dra 
from dual_vertexSplit import reverse_vertexSplit as drv 

from read_write import *

if __name__ == "__main__":
    
    pre = di 
    rev_initSub = drv 
    rev_avg = dra
    
    vertex, faces = read_off(fineMeshPath)
    
    # 基本型
    # for i in range(rsub):
    #     vvNumber, fvNumber, ringVertex, valences = pre(vertex, faces)
    #     for j in range(rave - 1, -1, -1):
    #         rev_avg(j, vertex, ringVertex, [vvNumber, fvNumber], weight[j])
    #
    #     # 未调整
    #     # vertex, faces = rev_initSub(vertex, ringVertex, [vvNumber, fvNumber])
    #
    #     # 调整
    #     vertex, faces = rev_initSub(vertex, ringVertex, [vvNumber, fvNumber], valences)
    #     write_off("reverse_{}.off".format(i + 4), vertex, faces)
    
    # 对偶型
    for i in range(rsub):
        vfNumber, ffNumber = pre(vertex, faces)
        
        for j in range(rave - 1, -1, -1):
            rev_avg(j, vertex, faces, [vfNumber, ffNumber], weight[j])
            
        vertex, faces = rev_initSub(vertex, faces, [vfNumber, ffNumber])
    
        write_off("reverse_{}.off".format(i + 1), vertex, faces)