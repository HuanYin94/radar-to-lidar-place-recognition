function [] = save_training_txt_random_triplet(pose, save_txt, sample_num, start_id, end_id)
% YH

% for seq01 on oxford, start_id = 300, end_id = 7580

% negative distance threshold
neg_th = 5.0; % meter
pos_th = 1.5;

pose_xy = pose(:,1:2);

% pose_num = length(pose);

% pose_tree = KDTreeSearcher(pose_xy);

% random anchers
ancher_id = randi([start_id, end_id], 1, sample_num);
postive_id = [];
negative_id = [];

for i = 1:sample_num
    disp(i);
    pose_cur = pose_xy(ancher_id(i),:);
    
    [Idx, D] = knnsearch(pose_xy, pose_cur, 'K', 5);
    
    flag = 1;
    while(flag == 1)
        % far from ID
        if rand() > 0.25
            % far from ancher id
            ancher_idx = repmat(ancher_id(i), 1, 5);
            diff_id = abs(Idx - ancher_idx);
            id = find(diff_id == max(diff_id));
            postive_id(i) = Idx(id(1));
        else
            % random pick
            postive_id(i) = Idx(randi([1,5],1,1));
        end

        pose_pos = pose_xy(postive_id(i),:);
        if norm(pose_pos - pose_cur) > pos_th
            flag = 1;
            postive_id(i) = [];
        else
            flag = 0;
        end
    
    end
    
    flag = 1; close_flag = 0;
    shocking_range = 50; delta_shocking = 50;
    if rand() > 0.75
        close_flag = 1;
    end
    while(flag == 1)
        if close_flag == 1
            negative_id(i) = randi([ancher_id(i) - shocking_range,...
                ancher_id(i) + shocking_range], 1, 1);
        else
            negative_id(i) = randi([start_id,end_id], 1, 1);
        end
        
        pose_neg = pose_xy(negative_id(i), :);
        if norm(pose_neg - pose_cur) > neg_th
            flag = 0;
        else
            flag = 1;
            shocking_range = shocking_range + delta_shocking;
        end
    end
    
    diff(i,:) = pose(postive_id(i),:) - pose(ancher_id(i),:);
end

labels = [ancher_id', postive_id', negative_id'];

dlmwrite(save_txt, labels, 'delimiter', ' ');

end

