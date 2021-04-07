%radon transform mk1
%the radon command returns the Radon Transform of a 2-D grayscale
%image I for angles in the range [0, 179] degrees. The Radon transform 
%is the projection of the image intensity along a radial line oriented 
%at a specific angle.
%R = radon(I)

%R = radon(I,theta)
%returns the Radon transform for the angles specified by theta.

%[R,xp] = radon(_)
%returns a vector xp containing the radial coordinates corresponding 
%to each row of the image.

%make the axes scale visible for this image
iptsetpref('ImshowAxesVisible','on');

%Create a sample image.
I = zeros(100,100);
I(25:75, 25:75) = 1;

%Calculate the Radon transform.
theta = 0:180;
[R,xp] = radon(I,theta);

%Display the transform.
imshow(R,[],'Xdata',theta,'Ydata',xp,'InitialMagnification','fit');
xlabel('\theta (degrees)');
ylabel('x''');
colormap(gca,hot), colorbar;