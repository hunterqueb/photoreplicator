[vertices,faces,normals,name] = stlRead('hinge.stl');
stlPlot(vertices,faces,name);

n = floor(length(vertices)/3);
X = reshape(vertices(:,1),3,n);  
Y = reshape(vertices(:,2),3,n);  
Z = reshape(vertices(:,3),3,n);  
C = zeros(3,n);   