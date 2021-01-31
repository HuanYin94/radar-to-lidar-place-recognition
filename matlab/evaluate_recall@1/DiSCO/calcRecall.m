function [recall_1] = calcRecall(fft_database_cells, fft_query_cells,...
    pose_database, pose_query, dis_th)
% YH for evalution code
    
    database_cnt = length(fft_database_cells);
    query_cnt = length(fft_query_cells);
    
    one_perc_cnt = ceil(database_cnt * 0.01);
    
    % build kd-tree
    disp('Build kd-tree')
    for i = 1:database_cnt
        fft_ = fft_database_cells{i}';
        X(i,:) = fft_(:)';
    end
    database = KDTreeSearcher(X);
    
    disp('Counting')
    recall_1_cnt = 0;
    recall_1perc_cnt = 0;
    find_list = [];
    correct_list = zeros(query_cnt,1);
    % every pose in query
    for i = 1:query_cnt
%         disp(i)
        fft_ = fft_query_cells{i}';
        [id_k1, D] = knnsearch(database, fft_(:)', 'K', 1);
        [id_k1perc, D_k1perc] = knnsearch(database, fft_(:)', 'K', one_perc_cnt);
        
        % recall@1
        if isClose(pose_query(i,:), pose_database(id_k1,:), dis_th) == 1
            recall_1_cnt = recall_1_cnt + 1;
            correct_list(i,1) = 1;
        end
        
        find_list(i,:) = id_k1;
        
%         % recall@1%
%         find_flag = 1;
%         k = 1;
%         while find_flag == 1 && k <= one_perc_cnt
%             if isClose(pose_query(i,:), pose_database(id_k1perc(k),:), dis_th) == 1
%                 recall_1perc_cnt = recall_1perc_cnt + 1;
%                 find_flag = 0;
%             end
%             k = k + 1;
%         end
    end
    
    recall_1 = recall_1_cnt / query_cnt;
    % output
    disp('recall@1');
    disp(recall_1);
    
%     recall_1perc = recall_1perc_cnt / query_cnt;
%     disp('recall@1%');
%     disp(recall_1perc);
    
end

