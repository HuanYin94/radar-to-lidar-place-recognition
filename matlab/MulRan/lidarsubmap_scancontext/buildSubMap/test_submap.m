
start_dis_th = 64;
end_dis_th = 64;

id = 530;

lidar_path = '/home/yinhuan/Data/radar_loc/02.07/seq01_laser_pc/';

submap_start = id;

while calc2DDistance(pose_xy_01(id,:), pose_xy_01(submap_start,:)) < start_dis_th
    submap_start = submap_start - 1;
end

submap_end = id;

while calc2DDistance(pose_xy_01(id,:), pose_xy_01(submap_end,:)) < end_dis_th
    submap_end = submap_end + 1;
end

for i = submap_start:1:submap_end
    if i == submap_start
        lidar_pt = pcread([lidar_path, int2str(i), '.ply']);
        transform = getAffine3d(pose_xy_01(i,:));
        lidar_pt = pctransform(lidar_pt, transform);
        map_pt = lidar_pt;
    else
        lidar_pt = pcread([lidar_path, int2str(i), '.ply']);
        transform = getAffine3d(pose_xy_01(i,:));
        lidar_pt = pctransform(lidar_pt, transform);
        map_pt = pcmerge(map_pt, lidar_pt, 0.25);
    end
end

A = getAffine3d(pose_xy_01(id,:));

map_pt_center = pctransform(map_pt, invert(A));
    
pcshow(map_pt_center);
xlabel('X');


