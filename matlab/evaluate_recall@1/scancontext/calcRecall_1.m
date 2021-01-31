function [recall_1] = calcRecall_1(ringkey_database, ringkey_query, sc_database, sc_query, ...
    pose_database, pose_query, dis_th, numberCandidate)
% YH for evalution code
    
    database_cnt = length(ringkey_database);
    query_cnt = length(ringkey_query);
    
    one_perc_cnt = ceil(database_cnt * 0.01);
    
    % build kd-tree
    disp('Build kd-tree')
    for i = 1:database_cnt
        fft_ = ringkey_database{i}';
        X(i,:) = fft_;
    end
    database = KDTreeSearcher(X);
    
    disp('Counting')
    recall_1_cnt = 0;
    recall_1perc_cnt = 0;
    % every pose in query
    for i = 1:query_cnt
%         disp(i)
        fft_ = ringkey_query{i}';
        [candidates, D] = knnsearch(database, fft_, 'K', numberCandidate);        
        
        query_sc = sc_query{i};
        % find the nearest (top 1) via pairwise comparison
        nearest_idx = 0;
        min_dist = inf; % initialization 
        for ith_candidate = 1:length(candidates)
            candidate_node_idx = candidates(ith_candidate);
            candidate_img = sc_database{candidate_node_idx};

            distance_to_query = sc_dist(query_sc, candidate_img);

            if( distance_to_query < min_dist)
                nearest_idx = candidate_node_idx;
                min_dist = distance_to_query;
            end     
        end
        
        % recall@1
        if isClose(pose_query(i,:), pose_database(nearest_idx,:), dis_th) == 1
            recall_1_cnt = recall_1_cnt + 1;
        end
        
    end
    
    recall_1 = recall_1_cnt / query_cnt;
    % output
    disp('recall@1');
    disp(recall_1);
    
end

