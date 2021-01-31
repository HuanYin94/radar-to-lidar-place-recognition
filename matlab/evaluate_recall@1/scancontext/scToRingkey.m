function [ringKeyCells] = scToRingkey(scancontextCells)
% S

for i=1:length(scancontextCells)
    sc = scancontextCells{i};
    ringKeyCells{i} = mean(sc, 2);
end

end

