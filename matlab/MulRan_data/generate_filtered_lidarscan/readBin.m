function ptcloud = readBin(bin_path, lidar_height)
   
%% Read 
fid = fopen(bin_path, 'rb'); raw_data = fread(fid, [4 inf], 'single'); fclose(fid);
points = raw_data(1:3,:)'; 
points(:, 3) = points(:, 3) + lidar_height; % z in car coord.

ptcloud = pointCloud(points);

end % end of function
