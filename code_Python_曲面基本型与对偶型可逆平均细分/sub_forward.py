# inFile = r"C:\Users\WeiGo\Desktop\网格数据\geometry_off\cube.off"
inFile = r"C:\Users\WeiGo\Desktop\Venus分解\dual\bm.off"
subNum = 1
aveNum = 2
# weights = [1/2]
weights = [3/4, 1/3]

import numpy as np
from read_write import read_off, write_off

from primal_faceSplit import faceSplit as ps
from primal_averaging import averaging as pa
from dual_vertexSplit import vertexSplit as vs
from dual_averaging import averaging as da
    
if __name__ == "__main__":
    
    init_sub = vs
    average = da 
    
    # 读入一个初始网格
    verts, faces = read_off(inFile)
    
    # # 基本型
    # for sub_i in range(subNum):
        
    #     faces, ringVertex, vvNumber, fvNumber = init_sub(verts, faces)
        
    #     for i in range(aveNum):
    #         average(i, verts, ringVertex, [vvNumber, fvNumber], weights[i])
        
    #     write_off("{}.off".format(sub_i + 1), verts, faces)
    
    # 对偶型
    for sub_i in range(subNum):
        
        faces, vfNumber, ffNumber = init_sub(verts, faces)
        
        for i in range(aveNum):
            average(i, verts, faces, [vfNumber, ffNumber], weights[i])
        
        write_off("dual_{}.off".format(sub_i + 1), verts, faces)
