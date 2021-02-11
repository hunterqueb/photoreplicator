# Import Libraries
import PyQt5.QtGui as qg
import sys
from voxelfuse.voxel_model import VoxelModel
from voxelfuse.mesh import Mesh
from voxelfuse.plot import Plot

# Start Application
if __name__ == '__main__':
    app1 = qg.QApplication(sys.argv)

    # Import Models
    modelIn = VoxelModel.fromMeshFile('goodCylinder.STL')

    # Process Models
    modelResult = modelIn

    # Create and Export Mesh
    mesh1 = Mesh.fromVoxelModel(modelResult)
    mesh1.export('modelResult.stl')

    # Create and Export Plot
    plot1 = Plot(mesh1)
    plot1.show()
    app1.processEvents()
    plot1.export('result.png')

    app1.exec_()
