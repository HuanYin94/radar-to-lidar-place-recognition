function [] = saveLasers(saveDir, ousterDir, ousterStampFile, ...
                            radarStampFile)
% by YH
% Loc/PR for MulRan
    
base2lidar = [-0.999982947984152,-0.00583983849243012,-5.22570603094484e-06,1.70420000000000;
                0.00583983848322059,-0.999982947996283,1.77587681343060e-06,-0.0210000000000000;
                -5.23598775595906e-06,1.74532925196952e-06,0.999999999984769,1.80470000000000;
                0,0,0,1];
base2radar = [0.999876632481661,-0.0157073173118207,0,1.50000000000000;
                0.0157073173118207,0.999876632481661,0,-0.0400000000000000;
                0,0,1,1.97000000000000;
                0,0,0,1];
            
% cannot read with full precision ?
lidar_time = csvread(ousterStampFile);
radar_time = csvread(radarStampFile);

fileNames = listDir(ousterDir);

% calibrations
lidar2radar = inv(base2lidar) * base2radar;

for i = 1:length(radar_time)
% for i = 266:length(radar_time)
    disp(i);
    
    [nn_timediff, id] = min(abs(lidar_time - radar_time(i)));
    
    fileName = fileNames{id};
    
    lidar_bin_file = [ousterDir, fileName];
    disp(lidar_bin_file)
    ptcloud = readBin(lidar_bin_file, 0.0); % N*3
    
    pt_points = ptcloud.Location;
    pt_points = [pt_points, ones(size(pt_points,1),1)]';
    
    pt_points_radarFrame = lidar2radar * pt_points;
    
%     pc = pointCloud(pt_points_radarFrame(1:3,:)');
%     pcshow(pc);
%     xlabel('x');
%     plot3(pt_points_radarFrame(1,:), pt_points_radarFrame(2,:), pt_points_radarFrame(3,:), 'k.');
% %     axis equal;
    pt_filter = pt_points_radarFrame;
       
    % DCC-01
%     pt_filter_id_Z = find(pt_points_radarFrame(3,:) > 1 | pt_points_radarFrame(3,:) < 0);
    pt_filter_id_Z = find(pt_points_radarFrame(3,:) > 2 | pt_points_radarFrame(3,:) < 0);
    pt_filter_id_origin_point = find(pt_points_radarFrame(1,:) < 1 & pt_points_radarFrame(1,:) > -1 & ...
                                pt_points_radarFrame(2,:) < 1 & pt_points_radarFrame(2,:) > -1);
    pt_filter_id = [pt_filter_id_Z, pt_filter_id_origin_point];    
    pt_filter(:, pt_filter_id) = [];
    
    
    % cloud process & save
   pt_filter(1,:) = pt_filter(1,:);
   pt_filter(2,:) = pt_filter(2,:);
%   pt_filter(3,:) = pt_filter(3,:);
   pt_filter(3,:) = zeros(1, size(pt_filter,2));
   pc = pointCloud(pt_filter(1:3,:)');
   pcshow(pc);
%    pcwrite(pc, [saveDir, num2str(i), '.ply']);
%    pcwrite(pc, '/home/yinhuan/test.ply');
    
%     close all;
%     figure;
%    plot3(pt_filter(1,:), pt_filter(2,:), pt_filter(3,:), 'b.');
%    axis equal;
end

end

