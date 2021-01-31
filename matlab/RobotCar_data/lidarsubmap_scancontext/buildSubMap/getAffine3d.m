function [affine_matrix] = getAffine3d(xyt)
% YH
    
% rot = [cos(xyt(3)) sin(xyt(3)) 0; ...
%       -sin(xyt(3)) cos(xyt(3)) 0; ...
%                0          0  1];
% trans = [xyt(1), xyt(2), 0];
% affine_matrix = rigid3d(rot,trans);

    A = [cos(xyt(3)) sin(xyt(3)) 0 0; ...
         -sin(xyt(3)) cos(xyt(3)) 0 0; ...
         0 0 1 0; ...
         xyt(1) xyt(2) 0 1];
    affine_matrix = affine3d(A);
    
end

