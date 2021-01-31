function [] = saveLiDARSC_occupy(pt_dir, save_sc, num_sector, num_ring, max_range)
% YH 

ply_cnt = length(dir(strcat(pt_dir, '*.ply')));

for i = 1:ply_cnt
    disp(i);
    pt = pcread([pt_dir, int2str(i), '.ply']);
    img = Ptcloud2ScanContext_occupy(pt, num_sector, num_ring, max_range);
%     gray_img = mat2gray(img);
%     imwrite(gray_img, [save_sc, int2str(i), '.png']);
    dlmwrite([save_sc, num2str(i), '.txt'], img,...
            'delimiter', ' ', 'precision','%.1f');
end

end

