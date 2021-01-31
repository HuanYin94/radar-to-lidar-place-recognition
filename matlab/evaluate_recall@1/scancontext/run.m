%% KAIST 
%for i = 1:3298
%    radar_sc_kaist01{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Mulran/Kaist01_80/radar_sc/',...
%        int2str(i), '.txt']);
%    lidar_sc_kaist01{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Mulran/Kaist01_80/lidar_sc_occupy/',...
%        int2str(i), '.txt']); 
% end
% 
% for i = 1:3586
%    radar_sc_kaist02{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Mulran/Kaist02_80/radar_sc/',...
%        int2str(i), '.txt']);
%    lidar_sc_kaist02{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Mulran/Kaist02_80/lidar_sc_occupy/',...
%        int2str(i), '.txt']); 
% end
% 
% 
% radar_ringkey_kaist01 = scToRingkey(radar_sc_kaist01);
% radar_ringkey_kaist02 = scToRingkey(radar_sc_kaist02);
% lidar_ringkey_kaist01 = scToRingkey(lidar_sc_kaist01);
% lidar_ringkey_kaist02 = scToRingkey(lidar_sc_kaist02);
% 
% recall_1_kaist_ll_sc = calcRecall_1(lidar_ringkey_kaist02, lidar_ringkey_kaist01, ...
%     lidar_sc_kaist02, lidar_sc_kaist01, ...
%     pose_kaist_02, pose_kaist_01, 3, floor(length(lidar_ringkey_kaist02)*0.01));
% 
% 
% % recall_1_kaist_rr_sc = calcRecall_1(radar_ringkey_kaist02, radar_ringkey_kaist01, ...
% %     radar_sc_kaist02, radar_sc_kaist01, ...
% %     pose_kaist_02, pose_kaist_01, 3, floor(length(radar_ringkey_kaist02)*0.01));
% % 
% 
% recall_1_kaist_rl_sc = calcRecall_1(lidar_ringkey_kaist02, radar_ringkey_kaist01, ...
%     lidar_sc_kaist02, radar_sc_kaist01, ...
%     pose_kaist_02, pose_kaist_01, 3, floor(length(lidar_ringkey_kaist02)*0.01));

%% Oxford 07 to 01


% 
% for i = 1:8866
%    radar_sc_seq01{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Oxford/seq01_80/radar_sc/',...
%        int2str(i), '.txt']);
%    lidar_sc_seq01{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Oxford/seq01_80/lidar_sc_occupy/',...
%        int2str(i), '.txt']);
% end
% 
% for i = 1:7658
%    radar_sc_seq07{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Oxford/seq07_80/radar_sc/',...
%        int2str(i), '.txt']); 
%    lidar_sc_seq07{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Oxford/seq07_80/lidar_sc_occupy/',...
%        int2str(i), '.txt']);
% end
% 
% 
% radar_ringkey_seq01 = scToRingkey(radar_sc_seq01);
% radar_ringkey_seq07 = scToRingkey(radar_sc_seq07);
% lidar_ringkey_seq01 = scToRingkey(lidar_sc_seq01);
% lidar_ringkey_seq07 = scToRingkey(lidar_sc_seq07);
% 
% radar_ringkey_seq01_test = radar_ringkey_seq01(7600:8300);
% radar_ringkey_seq07_test = radar_ringkey_seq07(6350:6950);
% radar_sc_seq01_test = radar_sc_seq01(7600:8300);
% radar_sc_seq07_test = radar_sc_seq07(6350:6950);
% 
% lidar_ringkey_seq01_test = lidar_ringkey_seq01(7600:8300);
% lidar_ringkey_seq07_test = lidar_ringkey_seq07(6350:6950);
% lidar_sc_seq01_test = lidar_sc_seq01(7600:8300);
% lidar_sc_seq07_test = lidar_sc_seq07(6350:6950);
% 
% pose_xy_01_test = pose_xy_01(7600:8300,:);
% pose_xy_07_test = pose_xy_07_tr(6350:6950,:);
% 
% 
% recall_1_oxford_ll_sc = calcRecall_1(lidar_ringkey_seq01_test, lidar_ringkey_seq07_test, ...
%     lidar_sc_seq01_test, lidar_sc_seq07_test, ...
%     pose_xy_01_test, pose_xy_07_test, 3, floor(length(lidar_ringkey_seq01_test)*0.01));
% % 
% % 
% % recall_1_oxford_rr_sc = calcRecall_1(radar_ringkey_seq01_test, radar_ringkey_seq07_test, ...
% %     radar_sc_seq01_test, radar_sc_seq07_test, ...
% %     pose_xy_01_test, pose_xy_07_test, 3, floor(length(radar_ringkey_seq01_test)*0.01));
% 
% 
% recall_1_oxford_rl_sc = calcRecall_1(lidar_ringkey_seq01_test, radar_ringkey_seq07_test, ...
%     lidar_sc_seq01_test, radar_sc_seq07_test, ...
%     pose_xy_01_test, pose_xy_07_test, 3, floor(length(lidar_ringkey_seq01_test)*0.01));




%% Riverside


for i = 1:2214
   radar_sc_riverside01{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Mulran/Riverside01_80/radar_sc/',...
       int2str(i), '.txt']);
   lidar_sc_riverside01{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Mulran/Riverside01_80/lidar_sc_occupy/',...
       int2str(i), '.txt']); 
end

for i = 1:3252
   radar_sc_riverside02{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Mulran/Riverside02_80/radar_sc/',...
       int2str(i), '.txt']);
   lidar_sc_riverside02{i} = importdata(['/home/yinhuan/Data/radar_lidar_pr/Mulran/Riverside02_80/lidar_sc_occupy/',...
       int2str(i), '.txt']); 
end


radar_ringkey_riverside01 = scToRingkey(radar_sc_riverside01);
radar_ringkey_riverside02 = scToRingkey(radar_sc_riverside02);
lidar_ringkey_riverside01 = scToRingkey(lidar_sc_riverside01);
lidar_ringkey_riverside02 = scToRingkey(lidar_sc_riverside02);



recall_1_riverside_ll_sc = calcRecall_1(lidar_ringkey_riverside02, lidar_ringkey_riverside01, ...
    lidar_sc_riverside02, lidar_sc_riverside01, ...
    pose_riverside_02, pose_riverside_01, 3, floor(length(lidar_ringkey_riverside02)*0.01));


recall_1_riverside_rr_sc = calcRecall_1(radar_ringkey_riverside02, radar_ringkey_riverside01, ...
    radar_sc_riverside02, radar_sc_riverside01, ...
    pose_riverside_02, pose_riverside_01, 3, floor(length(radar_ringkey_riverside02)*0.01));


recall_1_riverside_rl_sc = calcRecall_1(lidar_ringkey_riverside02, radar_ringkey_riverside01, ...
    lidar_sc_riverside02, radar_sc_riverside01, ...
    pose_riverside_02, pose_riverside_01, 3, floor(length(lidar_ringkey_riverside02)*0.01));

