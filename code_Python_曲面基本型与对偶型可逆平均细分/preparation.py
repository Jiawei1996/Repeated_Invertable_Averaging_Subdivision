def primal_Info(vertex, faces):
    # 返回点点数、面点数、1-环邻接点集、顶点的度
    
    vertexNumber = len(vertex)
    faceNumber = len(faces)
    ringVertex = [[] for _ in range(vertexNumber)]
    ringFaces = [[] for _ in range(vertexNumber)]
    
    # 记录每个点的度，等于邻接面的个数
    valence = [0] * vertexNumber
    for faceId, face in enumerate(faces):
        for vId in face:
            valence[vId] += 1
            ringFaces[vId].append(faceId)
    
    # 由度和面的个数推算出面点的个数
    t, p = 0, 0
    while t != faceNumber:
        p -= 1
        if p < - faceNumber:
            raise ValueError("计算面点数失败")
        t += valence[p]
    fvNumber = -p
    vvNumber = (vertexNumber + 2) // 2 - fvNumber
    
    # 计算1-环邻接点
    for idx in set(range(vvNumber)) | set(range(vertexNumber - fvNumber, vertexNumber)):
        ringFace = ringFaces[idx]
        faceId = ringFace.pop()
        tId = faces[faceId].index(idx)
        ringVertex[idx].extend([faces[faceId][tId - 3], faces[faceId][tId - 2]])
        tV = faces[faceId][tId - 1]
        while ringFace:
            for i, faceId in enumerate(ringFace):
                if tV in faces[faceId]:
                    tId = faces[faceId].index(tV)
                    ringVertex[idx].extend([ tV, faces[faceId][tId - 3]])
                    tV = faces[faceId][tId - 2]
                    ringFace.pop(i)
                    break 
    
    return vvNumber, fvNumber, ringVertex, valence


def dual_info(vertex, faces):
    vertexNumber = len(vertex)
    vfNumber = 0
    t = 0
    while t != vertexNumber:
        t += len(faces[vfNumber])
        vfNumber += 1
    
    ffNumber = (len(faces) + 2) // 2 - vfNumber
    
    return vfNumber, ffNumber