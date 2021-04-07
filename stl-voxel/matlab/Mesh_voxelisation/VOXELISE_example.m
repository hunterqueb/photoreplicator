
%Plot the original STL mesh:
figure
[stlcoords] = READ_stl('hinge.stl');
xco = squeeze( stlcoords(:,1,:) )';
yco = squeeze( stlcoords(:,2,:) )';
zco = squeeze( stlcoords(:,3,:) )';
[hpat] = patch(xco,yco,zco,'b');
camlight('headlight');
material('dull');
axis equal

%Voxelise the STL:
[OUTPUTgrid] = VOXELISE(100,100,100,'hinge.stl','xyz');

yzIm = squeeze(sum(OUTPUTgrid,1));
xzIm = squeeze(sum(OUTPUTgrid,2));
xyIm = squeeze(sum(OUTPUTgrid,3));



%Show the voxelised result:
figure;
subplot(1,3,1);
imagesc(yzIm);
colormap(gray(256));
xlabel('Z-direction');
ylabel('Y-direction');
axis equal tight

subplot(1,3,2);
imagesc(xzIm);
colormap(gray(256));
xlabel('Z-direction');
ylabel('X-direction');
axis equal tight

subplot(1,3,3);
imagesc(xyIm);
colormap(gray(256));
xlabel('Y-direction');
ylabel('X-direction');
axis equal tight
