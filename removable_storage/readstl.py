import numpy
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

myMesh = mesh.Mesh.from_file("removable_storage/cylinder.STL")

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(myMesh.vectors))


volume, cog, inertia = myMesh.get_mass_properties()
print("Volume                                  = {0}".format(volume))
print("Position of the center of gravity (COG) = {0}".format(cog))
print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0, :]))
print("                                          {0}".format(inertia[1, :]))
print("                                          {0}".format(inertia[2, :]))


# Auto scale to the mesh size
scale = myMesh.points.flatten('A')  # 'C', 'F', 'A', or 'K'
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()
