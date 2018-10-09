close all; clear; format longg; clc;
load('Flow_Rate_Per_Line.mat')
load('Mesh.mat')
%%%%%%%%%%%%%%%%
% This will plot the luminal tree structure from the file
% tree.txt that you made for us a long time ago.
% According to the lines there, I have computed the flow rates.
% These have a clear direction. 
% The cell array named:FF, contains the flow rate in each line.
% For instance, line 38 is the exit line. 
% NOTE THAT THERE IS NO NEGATIVE FLOW. THIS IS JUST NUMERICAL CRAP DUE TO 
% NATHANS CALCIUM MODEL'S INTERPOLATION. 

figure(1)
for i = 1:72
    plot3(b{i}(:,1),b{i}(:,2),b{i}(:,3),'LineWidth',5,'Color','r')
    hold on
    if i ==38
        plot3(b{i}(:,1),b{i}(:,2),b{i}(:,3),'LineWidth',5,'Color','b')
        hold on
    end
end
for i = 1:7 %(sa_tri{i},:)
%     trisurf(tri{i}...
%             ,p{i}(:,1),p{i}(:,2),p{i}(:,3),'FaceColor','w','FaceAlpha',0.1)
%     hold on
    trisurf(tri{i}(sa_tri{i},:)...
            ,p{i}(:,1),p{i}(:,2),p{i}(:,3),'FaceColor','w','FaceAlpha',0.1)
    hold on
end
ax = gca;
ax.LineWidth = 2.5;
ax.FontSize=20;
box off
grid on
title('Luminal Tree')


%%%% Cluster Fluid Flow rate.
figure(2)
plot(FF{38,1}(11500:10:31500),'LineWidth',2,'Color','b')
hold on
ax = gca;
ax.LineWidth = 2.5;
ax.FontSize=20;
box off
xlabel('"dt" Steps')
ylabel('Exit Line Flow Rate (\mum^3/sec)')


%%%% Spread of Flow rates.
figure(3)
for i = 1:72
    plot(FF{i,1},'LineWidth',2)
    hold on
end
hold on
ax = gca;
ax.LineWidth = 2.5;
ax.FontSize=20;
box off
xlabel('"dt" Steps')
ylabel('Individual Line Flow Rates (\mum^3/sec)')
