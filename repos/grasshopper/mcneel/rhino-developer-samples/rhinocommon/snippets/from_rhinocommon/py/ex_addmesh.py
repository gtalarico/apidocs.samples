import Rhino
import scriptcontext
import System.Guid

def AddMesh():
    mesh = Rhino.Geometry.Mesh()
    mesh.Vertices.Add(0.0, 0.0, 1.0) #0
    mesh.Vertices.Add(1.0, 0.0, 1.0) #1
    mesh.Vertices.Add(2.0, 0.0, 1.0) #2
    mesh.Vertices.Add(3.0, 0.0, 0.0) #3
    mesh.Vertices.Add(0.0, 1.0, 1.0) #4
    mesh.Vertices.Add(1.0, 1.0, 2.0) #5
    mesh.Vertices.Add(2.0, 1.0, 1.0) #6
    mesh.Vertices.Add(3.0, 1.0, 0.0) #7
    mesh.Vertices.Add(0.0, 2.0, 1.0) #8
    mesh.Vertices.Add(1.0, 2.0, 1.0) #9
    mesh.Vertices.Add(2.0, 2.0, 1.0) #10
    mesh.Vertices.Add(3.0, 2.0, 1.0) #11
    
    mesh.Faces.AddFace(0, 1, 5, 4)
    mesh.Faces.AddFace(1, 2, 6, 5)
    mesh.Faces.AddFace(2, 3, 7, 6)
    mesh.Faces.AddFace(4, 5, 9, 8)
    mesh.Faces.AddFace(5, 6, 10, 9)
    mesh.Faces.AddFace(6, 7, 11, 10)
    mesh.Normals.ComputeNormals()
    mesh.Compact()
    if scriptcontext.doc.Objects.AddMesh(mesh)!=System.Guid.Empty:
        scriptcontext.doc.Views.Redraw()
        return Rhino.Commands.Result.Success
    return Rhino.Commands.Result.Failure


if __name__=="__main__":
    AddMesh()
