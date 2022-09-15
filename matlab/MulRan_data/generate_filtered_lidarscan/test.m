% xyz = readBin_old('/home/yinhuan/Data/bypy/Kaist01/Ouster/1561000444390857630.bin');

pt_filter = pt_points_radarFrameCopy;
pt_filter_id = find(pt_points_radarFrameCopy(3,:) > 1.0 | pt_points_radarFrameCopy(3,:) < 0.5);
pt_filter(:, pt_filter_id) = [];

figure;
plot3(pt_filter(1,:), -1*pt_filter(2,:), pt_filter(3,:), 'k.');
axis equal;

figure;
plot3(pt_points_radarFrameCopy(1,:), pt_points_radarFrameCopy(2,:), pt_points_radarFrameCopy(3,:), 'k.');
axis equal;
