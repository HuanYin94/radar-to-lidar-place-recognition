function [] = saveLasers(saveDir, ousterDir, ousterStamp, ...
                            radarStamp, base2lidar, base2radar)
% by YH
% for MulRan
    
% cannot read with full precision ?
lidar_time = csvread(ousterStamp);
radar_time = csvread(radarStamp);

fileNames = listdir(ousterDir);

% calibrations
lidar2radar = inv(base2lidar) * base2radar;

for i = 1:length(radar_time)
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

    pt_filter = pt_points_radarFrame;
    
    % Kaist
    %     pt_filter_id = find(pt_points_radarFrame(3,:) > 0.6 | pt_points_radarFrame(3,:) < 0.5);
    
    % DCC
%     pt_filter_id = find(pt_points_radarFrame(3,:) > 0.6 | pt_points_radarFrame(3,:) < 0.4);
    
    % RiverSide 0908
    pt_filter_id = find(pt_points_radarFrame(3,:) > 0.8 | pt_points_radarFrame(3,:) < 0.2);

    pt_filter(:, pt_filter_id) = [];
    
    % cloud process & save
   pt_filter(1,:) = pt_filter(1,:);
   pt_filter(2,:) = pt_filter(2,:);
   pt_filter(3,:) = zeros(1, size(pt_filter,2));
   pc = pointCloud(pt_filter(1:3,:)');
   pcwrite(pc, [saveDir, num2str(i), '.ply']);
    
end

end

