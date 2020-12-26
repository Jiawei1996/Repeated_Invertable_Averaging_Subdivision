import numpy as np

def vertexSplit(vertex, faces):
    vertex_number, face_number = len(vertex), len(faces)
    
    ringfaces = [[] for __ in range(vertex_number)]
    ringNewpoint = [[] for __ in range(vertex_number)]
    
    # 判断边上是否以生成新边面
    hasEface = [{} for __ in range(vertex_number)]
    
    # vfaces:vertex-faces, efaces:edge-faces
    vfaces, efaces = [], []
    
    for idx, face in enumerate(faces):
        for vId in face:
            ringfaces[vId].append(idx)
    
    
    for vId in range(vertex_number):
        
        ringFace = ringfaces[vId]
        # 将顶点vId的1-环邻接面有序化
        flag = len(ringFace)
        orderedRingFaces = [ringFace.pop()]
        t = faces[orderedRingFaces[-1]].index(vId)
        nextPId = faces[orderedRingFaces[-1]][t - 1]
        while ringFace:
            for idx, fId in enumerate(ringFace):
                if nextPId in faces[fId]:
                    orderedRingFaces.append(fId)
                    t = faces[fId].index(vId)
                    nextPId = faces[fId][t - 1]
                    ringFace.pop(idx)
                    break 
        assert flag == len(orderedRingFaces)
        ringfaces[vId] = orderedRingFaces
        
        # 添加新点
        vertex.extend([vertex[vId]] * (flag - 1))
        ringNewpoint[vId] = [vId] + list(range(vertex_number, vertex_number + flag - 1))
        vertex_number += flag - 1
        
        # 添加新点面
        vfaces.append(ringNewpoint[vId])
    
    
    # 生成新边面，并更新新面面
    for fId, face in enumerate(faces):
        
        ringfaceIdx = []
        for vId in face:
            ringfaceIdx.append(ringfaces[vId].index(fId))
        
        for vId in range(len(face)):
            v1, v2 = face[vId - 1], face[vId]
            if v2 not in hasEface[v1]:
                hasEface[v1][v2] = 1
                hasEface[v2][v1] = 1
                
                idx1 = ringfaceIdx[vId - 1]
                t1, t2 = ringfaces[v1][idx1 - 1], ringfaces[v1][idx1 + 1 - len(ringfaces[v1])]
                if v2 in faces[t1]:
                    idx2 = idx1 - 1
                    v2_idx2 = ringfaces[v2].index(t1)
                else:
                    idx2 = idx1 + 1 - len(ringfaces[v1])
                    v2_idx2 = ringfaces[v2].index(t2)
                
                
                efaces.append([ringNewpoint[v1][idx1], ringNewpoint[v1][idx2], 
                               ringNewpoint[v2][v2_idx2], ringNewpoint[v2][ringfaceIdx[vId]]])
        
        # 更新面面
        for idx, vId in enumerate(face):
            face[idx] = ringNewpoint[vId][ringfaceIdx[idx]]
    
    print("\n vertex split is done ! size: {} -points".format(len(vertex)))
    return vfaces + efaces + faces, len(vfaces), face_number


def reverse_vertexSplit(vertex, faces, number):
    vfNumber, ffNumber = number[0], number[1]
    newVertex = []
    
    indexSet = [0] * len(vertex)
    for face in faces[:vfNumber]:
        
        for vId in face:
            indexSet[vId] = len(newVertex)
        newVertex.append(np.mean([vertex[i] for i in face], axis=0).tolist())
    
    newFaces = faces[-ffNumber:]
    for idx, face in enumerate(newFaces):
        
        newFaces[idx] = [indexSet[i] for i in face]
    
    print("\n reverse vertex split is done! size is {} points.".format(len(newVertex)))
    return newVertex, newFaces