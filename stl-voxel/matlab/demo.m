tic
file = 'cylinder1.stl';

[vertices,faces,normals,name] = stlRead(file);
stlPlot(vertices,faces,name);


[OUTPUTgrid] = VOXELISE(100,100,100,file,'xyz');

yzIm = squeeze(sum(OUTPUTgrid,1));
xzIm = squeeze(sum(OUTPUTgrid,2));
xyIm = squeeze(sum(OUTPUTgrid,3));

theta = 0:180;
[R1,xp1] = radon(yzIm,theta);
[R2,xp2] = radon(xzIm,theta);
[R3,xp3] = radon(xyIm,theta);

%Display the transform.
figure


subplot(1,3,1);
imshow(R1,[],'Xdata',theta,'Ydata',xp1,'InitialMagnification','fit');
xlabel('\theta (degrees)');
ylabel('x''');
colormap(gca,hot), colorbar;
title('yz Axis Image')

subplot(1,3,2);
imshow(R2,[],'Xdata',theta,'Ydata',xp2,'InitialMagnification','fit');
xlabel('\theta (degrees)');
ylabel('x''');
colormap(gca,hot), colorbar;
title('xz Axis Image')

subplot(1,3,3);
imshow(R3,[],'Xdata',theta,'Ydata',xp3,'InitialMagnification','fit');
xlabel('\theta (degrees)');
ylabel('x''');
colormap(gca,hot), colorbar;
title('xy Axis Image')


%Show the voxelised result:
figure;
subplot(1,3,1);
imagesc(yzIm);
colormap(gray(256));
xlabel('Z-direction');
ylabel('Y-direction');
axis equal tight
title('yz Axis Image')

subplot(1,3,2);
imagesc(xzIm);
colormap(gray(256));
xlabel('Z-direction');
ylabel('X-direction');
axis equal tight
title('xz Axis Image')

subplot(1,3,3);
imagesc(xyIm);
colormap(gray(256));
xlabel('Y-direction');
ylabel('X-direction');
axis equal tight
title('xy Axis Image')

% jumping to volexising the output, we can find certain vertices that can
% be deleted/selected
% say we get a list of vertices to be deleted if (x,y,z<0)
% minZ = 20;
% [rows, ~] = find(vertices(:,3) < minZ);
% list = vertices(rows,:);

% if we delete the list of vertices with z<0, we get half the file 
% (as the base is not closed)
% [newv,newf] = stlDelVerts(vertices,faces,list);
% stlPlot(newv,newf,name);
% the idea is that we can take verticies within a small delta to generate a
% cross secion which can then be used to create a ct scan

toc