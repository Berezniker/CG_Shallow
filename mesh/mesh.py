import numpy as np


def obj_parser(objFilePath: str,
               sep: str = None,
               texture: bool = True,
               normal: bool = True) -> np.array:
    vertices, textures, normals = list(), list(), list()
    faces = list()
    with open(objFilePath, mode='r') as objFile:
        for line in objFile:
            if line.startswith('v'):
                vertices.append(line.split()[1:])
            if line.startswith('vt') and texture:
                textures.append(line.split()[1:])
            if line.startswith('vn') and normal:
                normals.append(line.split()[1:])
            if line.startswith('f'):
                faces.append(line.split()[1:])

    result = list()
    for face in faces:
        temp = list()
        for f in face:
            v, vt, vn = f, "", ""
            if sep is not None:
                v, vt, vn = f.split(sep=sep)
            if v:
                temp += vertices[int(v) - 1]
            if vt and texture:
                temp += textures[int(vt) - 1]
            if vn and normal:
                temp += normals[int(vn) - 1]
        result.append(temp)

    return np.array(result, dtype=np.float32).ravel()


cube = obj_parser("./mesh/cube.obj", sep='/')
# sphere = obj_parser("./mesh/sphere.obj", sep='/')
