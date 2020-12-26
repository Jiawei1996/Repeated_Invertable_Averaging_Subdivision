def read_off(file):
    with open(file, "r") as f:
        if 'OFF' != f.readline().strip():
            raise('Not a valid OFF header')
        n_verts, n_faces, n_dontknow = [
            int(s) for s in f.readline().strip().split(' ')]
        verts = [[float(s) for s in f.readline().strip().split(' ')]
                 for i_vert in range(n_verts)]
        faces = [[int(s) for s in f.readline().strip().split(' ')][1:]
                 for i_face in range(n_faces)]
        return verts, faces


def write_off(file, verts, faces):
    num_vertices = str(len(verts))
    num_faces = str(len(faces))
    num_edges = "0"
    vertex = "\n".join(" ".join(map(str, point)) for point in verts)
    faces = "\n".join(str(len(face)) + " " + " ".join(map(str, face))
                      for face in faces)

    assert isinstance(num_vertices, str) and isinstance(num_faces, str) and isinstance(
        vertex, str) and isinstance(num_edges, str) and isinstance(faces, str)

    content = "OFF\n{} {} {}\n{}\n{}".format(
        num_vertices, num_faces, num_edges, vertex, faces)

    with open(file, "w") as f:
        f.write(content)