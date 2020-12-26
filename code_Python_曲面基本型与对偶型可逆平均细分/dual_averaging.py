import numpy as np

def averaging(k, vertex, faces, number, weight):
    Range = range(number[0]) if k & 1 else range(-number[1], 0)
    weights = [1 - weight, weight]
    
    for fId in Range:
        face = faces[fId]
        centroid = np.mean([vertex[i] for i in face], axis=0)
        
        for vId in face:
            vertex[vId] = np.matmul(weights, [vertex[vId], centroid]).tolist()
    
    print("\n\t {}-th dual averaging is done!".format(k + 1))


def reverse_averaging(k, vertex, faces, number, weight):
    Range = range(number[0]) if k & 1 else range(-number[1], 0)
    weights = [1/(1 - weight), -weight/(1 - weight)]
    
    for fId in Range:
        face = faces[fId]
        centroid = np.mean([vertex[i] for i in face], axis=0)
        
        for vId in face:
            vertex[vId] = np.matmul(weights, [vertex[vId], centroid]).tolist()
    
    print("\n\t {}-th dual averaging is undone!".format(k + 1))