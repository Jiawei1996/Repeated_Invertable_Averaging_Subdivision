function fData = Euclid_trimal_subdivision(data, aveNum, w)
% ternary����ϸ��
sub_num = 5;
ave_num = 1 + 3*aveNum;
weight = w * ones(1, ave_num);

fData = data;
for i=1:sub_num
    fData = duplicate(fData);
    for j = 1:ave_num
        fData = averaging(fData, j, weight(j));
    end
end

% ������ƶ���ε����߳�
% maxL = max(sum(abs(fData - [fData(2:end,:); fData(1, :)]).^2,2).^(1/2));

% ������ƶ���ε�������ʣ�ÿ���㵽���ڽӵ��е�ľ��룩
% maxC = max(sum(abs( fData - ([fData(2:end,:);fData(1,:)]+[fData(end,:);fData(1:end-1,:)])./2 ).^2, 2).^(1/2));

% plot([data(:, 1); data(1, 1)], [data(:, 2); data(1, 2)], 'b-')
% hold on 
% plot([fData(:, 1); fData(1, 1)], [fData(:, 2); fData(1, 2)], 'r.')
% axis equal tight
% hold off
% title(['ƽ������:', num2str(aveNum), ', ����:', num2str(w), ...
%     '����:', num2str(maxL)])

end

function fData = duplicate(cData)
% ��ʼ�㸴��
len = size(cData, 1);
fData = zeros(3 * len, 2);
for i = 1:len
    fData(3*i-2:3*i, :) = ones(3, 2) * diag(cData(i, :));
end
end
function [fData, details] = withDetail_duplicate(cData, details)
% ��ϸ�ڳ�ʼ�㸴��
len = size(cData, 1);
d = details(1:2*len, :);
fData = zeros(3 * len, 2);
for i =1:len
    fData(3*i-2:3*i, :) = ones(3, 2) * diag(cData(i, :)) + ...
        [-(d(2*i-1, :)+d(2*i, :));d(2*i-1:2*i, :)];
end
details = details(2*len + 1:end, :);
end
function [cData, details] = reverse_duplicate(fData, details)
% ����㸴��
len = size(fData, 1);
cData = zeros(len / 3, 2);
tdetails = zeros(len / 3 * 2, 2);
for i = 1:size(cData, 1)
    cData(i, :) = mean(fData(3*i-2 : 3*i, :), 1);
    tdetails(2*i-1 : 2*i, :) = fData(3*i-1 : 3*i, :) - [cData(i, :); cData(i, :)];
end
details = [tdetails; details];
end
function data = averaging(data, k, weight)
% ��k��ƽ��
weightM = [1-weight, weight];
len = size(data, 1);
if mod(k, 3) == 1
    Range = [len, 1:len-1];
elseif mod(k, 3) == 2
    Range = 1:len;
else
    Range = [2:len, 1];
end
for i = 2:3:len
    data(Range(i-1), :) = weightM * data(Range([i-1, i]), :);
    data(Range(i+1), :) = weightM * data(Range([i+1, i]), :);
end
end
function data = reverse_averaging(data, k, weight)
% ��k������ƽ����������ƽ�����ֻ�в�����һ��
weightM = [1/(1-weight), -weight/(1-weight)];
len = size(data, 1);
if mod(k, 3) == 1
    Range = [len, 1:len];
elseif mod(k, 3) == 2
    Range = 1:len;
else
    Range = [2:len, 1];
end
for i = 2:3:len
    data(Range(i-1), :) = weightM * data(Range([i-1, i]), :);
    data(Range(i+1), :) = weightM * data(Range([i+1, i]), :);
end
end
