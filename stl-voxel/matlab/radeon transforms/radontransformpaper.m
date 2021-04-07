function [ res ] = myradon(f)

[N,M] = size(f);

% Center of the image
m = round(M/2);
n = round(N/2);

% The total number of rho's  is the number of pixels on the diagonal, since
% this is the largest straight line on the image when rotating
rhomax = ceil(sqrt(M^2 + N^2));
rc = round(rhomax/2);
mt = max(theta);

% Preallocate the matrix used to store the result
% add 1 to be sure, could also be subtracted when checking bounds
res = cast(zeros(rhomax+1,mt),'double');

tic
for t = 1:45 % below 45 degrees, use y as variable
    costheta = cos(t*pi/180);
    sintheta = sin(t*pi/180);
    a = -costheta/sintheta; % y = ax + b
    for r = 1:rhomax
        rho = r - rc;
        b = rho/sintheta; % y = ax + b
        ymax = min(round(-a*m+b),n-1);
        ymin = max(round(a*m+b),-n);
        for y = ymin:ymax
            x = (y-b)/a;
            xfloor = floor(x); % The integer part of x
            xlow = 1 - xup;    % The decimals of x
            x = xfloor;
            x = max(x,-m);
            x = min(x,m-2);
            res(rhomax - r + 1,mt-t) = res(rhomax - r + 1,mt-t) + xlow*f(y+n+1,x+m+1);
            res(rhomax - r + 1,mt-t) = res(rhomax - r + 1,mt-t) + xup*f(y+n+1,x+m+2);
            
        end
    end
end
for t = 46:90
    costheta = cos(t*pi/180);
    sintheta = sin(t*pi/180);
    a = -costheta/sintheta; % y = ax + b
    for r = 1:rhomax
        rho = r - rc;
        b = rho/sintheta;   % y = ax + b
        xmax = min(round((-n-b)/a),m-1);
        xmin = max(round((n-b/a),-m));
        for x = xmin:xmax
            y = a*x+b;
            yfloor = floor(y);
            yup = y - yfloor;
            ylow = 1 - yup;
            y = yfloor;
            y = max(y,-n);
            y = min(y,n-2);
            res(rhomax - r + 1,mt-t) = res(rhomax - r + 1,mt-t) + ylow*f(y+n+1,x+m+1);
            res(rhomax - r + 1,mt-t) = res(rhomax - r + 1,mt-t) + yup*f(y+n+2,x+m+1);
        end
    end
end
for t = 91:135
    costheta = cos(t*pi/180);
    sintheta = sin(t*pi/180);
    a = -costheta/sintheta; % y = ax + b
    for r = 1:rhomax
        rho = r - rc;
        b = rho/sintheta; % y = ax + b
        xmax = min(round((n-b)/a),m-1);
        xmin = max(round((-n-b)/a),-m);
        for x = xmin:xmax
            y = a*x+b;
            yfloor = floor(y);
            y = max(y,-n);
            y = min(y,n-2);
            res(rhomax - r + 1,mt-t) = res(rhomax - r + 1,mt-t) + ylow*f(y+n+1,x+m+1);
            res(rhomax - r + 1,mt-t) = res(rhomax - r + 1,mt-t) + yup*f(y+n+2,x+m+1);
        end
    end
end
for t = 136:179 % above 135 degrees, use y as variable
    costheta = cos(t*pi/180);
    sintheta = sin(t*pi/180);
    a = -costheta/sintheta; % y = ax + b
    for r = 1:rhomax
        rho = r - rc;
        b = rho/sintheta;   % y = ax + b
        ymax = min(round(a*m+b),n-1);
        ymin = max(round(-a*m+b),-n);
        for y = ymin:ymax
            x = (y-b)/a;
            xfloor = floor(x);
            xup = xfloor;
            x = max(x,-m);
            x = min(x,m-2);
            res(rhomax - r + 1,mt-t) = res(rhomax - r + 1,mt-t) + xlow*f(y+n+1,x+m+1);
            res(rhomax - r + 1,mt-t) = res(rhomax - r + 1,mt-t) + xup*f(y+n+1,x+m+1);
        end
    end
end
for t = 180 % the sum-line is vertical
    rhooffset = roun((rhomax - M)/2);
    for x = 1:M % cannot use r as x in both res and f since theyre not same size
        r = x + rhooffset;
        r = rhomax - r + 1;
        for y = 1:N
            res(r,t) = res(r,t) + f(y,x);
        end
    end
end
toc
rhoaxis = (1:rhomax+1) - rc;
figure
imagesc(1:180,rhoaxis,res);
colormap(hot), colorbar
end