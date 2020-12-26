import numpy as np 

def averaging(k, vertex, ringVertex, number, weight):
    # k: 第几次平均
    # vertex：顶点集
    # ringVertex：1-环邻接点集
    # number：[点点数，面点数]
    # weight：平滑参数
    
    flag = k & 1 # 0: vv, 1: fv
    Range = range(number[0]) if flag == 0 else range(-number[1], 0)
    w1 = [1 - weight, weight / 2, weight / 2]
    # w1 = [(1 - weight)**2, 2*(1 - weight)*weight, (weight)**2]
    w2 = [1 - weight, weight]
    
    for idx in Range:
        ring = ringVertex[idx]
        
        # 更新面点或点点
        edgeVCent = np.mean([vertex[ring[i]] for i in range(0, len(ring), 2)], axis=0)
        centroid = np.mean([vertex[ring[i]] for i in range(1, len(ring), 2)], axis=0)
        vertex[idx] = np.matmul(w1, [vertex[idx], edgeVCent, centroid]).tolist()
        
        # 更新边点
        for i in range(0, len(ring) - 1, 2):
            v0, e, v1 = ring[i - 1], ring[i], ring[i + 1]
            
            # 防止重复对边点平均
            if ringVertex[e] != flag:
                vertex[e] = np.matmul(w2, [
                    vertex[e], np.mean([vertex[v0], vertex[v1]], axis=0)
                ]).tolist()
                ringVertex[e] = flag 
    
    print("\n\t {}-th average is done !".format(k + 1))
    

def reverse_averaging(k, vertex, ringVertex, number, weight):
    flag = k & 1 # 0: vv, 1: fv
    Range = range(number[0]) if flag == 0 else range(-number[1], 0)
    
    w1 = [1/(1 - weight), -weight/(2*(1 - weight)), -weight/(2*(1 - weight))]
    w2 = [1/(1 - weight), -weight/(1 - weight)]
    
    for idx in Range:
        ring = ringVertex[idx]
        
        # 更新边点
        for i in range(0, len(ring) - 1, 2):
            v0, e, v1 = ring[i - 1], ring[i], ring[i + 1]
            
            # 防止重复对边点平均
            if ringVertex[e] != flag:
                vertex[e] = np.matmul(w2, [
                    vertex[e], np.mean([vertex[v0], vertex[v1]], axis=0)
                ]).tolist()
                ringVertex[e] = flag 
        
        # 更新面点或点点
        edgeVCent = np.mean([vertex[ring[i]] for i in range(0, len(ring), 2)], axis=0)
        centroid = np.mean([vertex[ring[i]] for i in range(1, len(ring), 2)], axis=0)
        vertex[idx] = np.matmul(w1, [vertex[idx], edgeVCent, centroid]).tolist()
    
    print("\n\t {}-th average is undone !".format(k + 1))