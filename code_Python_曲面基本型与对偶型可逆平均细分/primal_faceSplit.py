import numpy as np

def faceSplit(vertex, faces):
    # vertex is changed in-places, just return newfaces.
    
    verNumber = len(vertex)
    faceNumber = len(faces)
    
    # 记录旧边上是否有边点
    hasEdgeV = [{} for _ in range(verNumber)]
    # 记录每个旧点的邻接新面
    ringFaces = [[] for _ in range(verNumber)]
    vertex.extend([None] * (verNumber + 2*faceNumber - 2))
    newfaces = []
    pEdgeV = verNumber
    pFacev = 2*verNumber + faceNumber - 2
    
    # 记录每个点的1-环邻接点，格式为：边点-面点 或 边点-点点
    ringVertex = [[] for _ in range(len(vertex))]
    
    
    for face in faces:
        
        # add face-vertex
        vertex[pFacev] = np.mean(
            [vertex[idx] for idx in face],
            axis = 0
        ).tolist()
        
        # add edge-vertex
        for idx in range(len(face)):
            v0Id, v1Id = face[idx - 1], face[idx]
            if v1Id not in hasEdgeV[v0Id]:
                hasEdgeV[v0Id][v1Id] = pEdgeV
                hasEdgeV[v1Id][v0Id] = pEdgeV
                
                vertex[pEdgeV] = np.mean(
                    [vertex[v0Id], vertex[v1Id]],
                    axis= 0
                ).tolist()
                
                pEdgeV += 1
        
        # construct new faces: edge-vertex, vertex, edge-vertex, face-vertex
        for idx in range(-1, len(face) - 1):
            v0Id, v1Id, v2Id = face[idx - 1], face[idx], face[idx + 1]
            
            # 记录点点v1的邻接新面
            ringFaces[v1Id].append(len(newfaces))
            
            # 添加新面
            newfaces.append(
                [hasEdgeV[v1Id][v0Id], v1Id, hasEdgeV[v1Id][v2Id], pFacev]
            )
            
            # 记录每个面点的1-环邻接点，格式为：边点-点点
            ringVertex[pFacev].extend([hasEdgeV[v1Id][v0Id], v1Id])

        pFacev += 1
    
    # 记录每个点点的1-环邻接点，格式为：边点-面点
    for idx in range(verNumber):
        ringFace = ringFaces[idx]
        faceId = ringFace.pop()
        tId = newfaces[faceId].index(idx)
        ringVertex[idx].extend([newfaces[faceId][tId - 3], newfaces[faceId][tId - 2]])
        tV = newfaces[faceId][tId - 1]
        while ringFace:
            for i, faceId in enumerate(ringFace):
                if tV in newfaces[faceId]:
                    tId = newfaces[faceId].index(tV)
                    ringVertex[idx].extend([ tV, newfaces[faceId][tId + 1]])
                    tV = newfaces[faceId][tId - 2]
                    ringFace.pop(i)
                    break 
        assert len(ringVertex[idx]) & 1 == 0
        
        
    print("\n Face Split is done. ")
    return newfaces, ringVertex, verNumber, faceNumber


def reverse_faceSplit(vertex, ringVertex, number):
    
    vvNumber, fvNumber = number[0], number[1]
    # 由面点的1-环邻接点构造旧面，只保留点点
    oldfaces = [[ringVertex[fvId][i] for i in range(1, len(ringVertex[fvId]), 2)] for fvId in range(-fvNumber, 0)]
    
    print("\n reverse face split is done. ")
    return vertex[:vvNumber], oldfaces

def refine_reverse_faceSplit(vertex, ringVertex, number, valences):
    
    vvNumber, fvNumber = number[0], number[1]
    # 由面点的1-环邻接点构造旧面，只保留点点
    oldfaces = [[ringVertex[fvId][i] for i in range(1, len(ringVertex[fvId]), 2)] for fvId in range(-fvNumber, 0)]
    
    # 调整点点的位置
    for vId in range(vvNumber):
        vv = np.array(vertex[vId])
        
        t = 2 + 5/16 * valences[vId]
        sum_de = np.array([0., 0., 0.])
        sum_df = np.array([0., 0., 0.])
        for idx, Id in enumerate(ringVertex[vId]):
            if idx & 1:
                sum_df += np.array(vertex[Id]) - vv 
            else:
                sum_de += np.array(vertex[Id]) - vv 
        
        vertex[vId] = (vv + 1/t * sum_de + .5/t * sum_df ).tolist()
        
    print("\n refine reverse face split is done. ")
    return vertex[:vvNumber], oldfaces
