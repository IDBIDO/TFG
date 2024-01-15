function [Mass, ElapseTime] = SENCEstimation(TestData, Forest,cldi,anomalylambdan)
global id
id=1;

NumInst = size(TestData, 1);

Mass = zeros(Forest.NumTree,5);
et = cputime;
for k = 1:Forest.NumTree
    trave=zeros(2,size(TestData,2));
    ano=anomalylambdan(k);
   
   Mass(k,:) = SENCMass(TestData, 1:NumInst, Forest.Trees{k, 1}, zeros(NumInst, 5),cldi,trave,ano);
end
ElapseTime = cputime - et;
