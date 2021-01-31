function [] = saveLidarSubMaps(lidar_path, save_path, pose_xy, ...
    start_dis_th, end_dis_th, rotate_max, travel_dis_th)
% YH

files = dir(lidar_path); files(1:2) = []; files = {files(:).name};
total_cnt = length(files);

% the last radar has no pose, not count
total_cnt = total_cnt - 1;

for id = 1:total_cnt
% for id = 1160:total_cnt    
    disp(id);
    
    submap_start = id;
    while calc2DDistance(pose_xy(id,:), pose_xy(submap_start,:)) < start_dis_th ...
            && submap_start > 1 && abs(pose_xy(id,3) - pose_xy(submap_start,3)) < rotate_max
        submap_start = submap_start - 1;
    end
    
    submap_end = id;
    while calc2DDistance(pose_xy(id,:), pose_xy(submap_end,:)) < end_dis_th ...
            && submap_end < total_cnt && abs(pose_xy(id,3) - pose_xy(submap_end,3)) < rotate_max
        submap_end = submap_end + 1;
    end
    
    last_i = submap_start;
    for i = submap_start:1:submap_end
        % filter the stoppings
        if i > submap_start && ...
            calc2DDistance(pose_xy(i,:), pose_xy(last_i,:)) < travel_dis_th
            continue;
        else
            last_i = i;
        end
        
        if i == submap_start
            lidar_pt = pcread([lidar_path, int2str(i), '.ply']);
            transform = getAffine3d(pose_xy(i,:));
            lidar_pt = pctransform(lidar_pt, transform);
            map_pt = lidar_pt;
        else
            lidar_pt = pcread([lidar_path, int2str(i), '.ply']);
            transform = getAffine3d(pose_xy(i,:));
            lidar_pt = pctransform(lidar_pt, transform);
            map_pt = pcmerge(map_pt, lidar_pt, 0.0001);
        end
    end
    
    A = getAffine3d(pose_xy(id,:));

    map_pt_center = pctransform(map_pt, invert(A));
    pcshow(map_pt_center)
    pcwrite(map_pt_center, [save_path, int2str(id), '.ply']);

end


end

