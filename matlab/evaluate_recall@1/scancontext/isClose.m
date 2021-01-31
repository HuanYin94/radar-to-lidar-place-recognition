function [flag] = isClose(pose_1, pose_2, dis_th)
% YH

    if norm(pose_1(1:2) - pose_2(1:2)) <= dis_th
        flag = 1;
    else
        flag = 0;
    end
end

