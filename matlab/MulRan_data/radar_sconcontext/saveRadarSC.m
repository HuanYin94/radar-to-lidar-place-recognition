function [] = saveRadarSC(radar_polar_dir, save_dir, ...
    num_sector, num_ring, max_range)
% YH
        
    % osdir in scancontext
    files = dir(radar_polar_dir); files(1:2) = []; files = {files(:).name};
    
    range_end = floor(max_range / 0.06);
    
    for i = 1:length(files)
        disp(i);
        radar_polar = imread([radar_polar_dir, files{i}]);
        radar_polar = radar_polar(1:range_end,:);
        radar_polar = double(radar_polar) / 255;
        radar_polar = imresize(radar_polar, [num_ring, num_sector]);
        dlmwrite([save_dir, num2str(i), '.txt'], radar_polar,...
            'delimiter', ' ', 'precision','%.5f');
    end
    
end

