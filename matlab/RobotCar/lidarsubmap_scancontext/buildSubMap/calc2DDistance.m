function [dis] = calc2DDistance(xyt1, xyt2)
% YH
    dis = norm([xyt1(1), xyt1(2)]-[xyt2(1), xyt2(2)]);
end

