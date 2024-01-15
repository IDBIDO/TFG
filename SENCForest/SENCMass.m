function mass = SENCMass(Data, CurtIndex, Tree, mass,cldi,trave,ano)
global flag
flag=0;

if Tree.NodeStatus == 0
    mass(CurtIndex,1) = double(Tree.high)<ano;
    if Tree.Size == 1
        mass(CurtIndex,3)=Tree.la;
        mass(CurtIndex,4)=Tree.id;
        flag=1;
    elseif  Tree.Size<1
        flag=1;
        mass(CurtIndex,4)=Tree.id;
    else
        tempdist=pdist2(Data(CurtIndex,:),Tree.center);      
        mass(CurtIndex,2)=(tempdist>Tree.dist*cldi);
        mass(CurtIndex,4)=Tree.id;
        
        %%%%%%%%%%%%%%%%%%%%%%label%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ter=Tree.la;
        Scoretrainl =  tabulate(ter);
        Scoretrainl=Scoretrainl(Scoretrainl(:,2)==max(Scoretrainl(:,2)),1);
        if size(Scoretrainl,1)>1
            mass(CurtIndex,3)=Scoretrainl(1,1);
        else
            mass(CurtIndex,3)=Scoretrainl;
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if  mass(CurtIndex,2)==1 && mass(CurtIndex,1)==1
            mass(CurtIndex,5)=1;
        else
            mass(CurtIndex,5)=0;
        end
    end
    
    return;
else
    
    LeftCurtIndex = CurtIndex(Data(CurtIndex, Tree.SplitAttribute) < Tree.SplitPoint);
    RightCurtIndex = setdiff(CurtIndex, LeftCurtIndex);
    trave(1,Tree.SplitAttribute)=1;
    trave(2,Tree.SplitAttribute)=Tree.SplitPoint;
    if ~isempty(LeftCurtIndex)
        mass = SENCMass(Data, LeftCurtIndex, Tree.LeftChild, mass,cldi,trave,ano);
        if flag==1        
            tempdist=pdist2(Data(CurtIndex,:),Tree.center);
            mass(CurtIndex,2)=(tempdist>Tree.dist*cldi);
            
            if   mass(CurtIndex,1)<ano    && mass(CurtIndex,2)==1
                mass(CurtIndex,5)=1;
            else
                mass(CurtIndex,5)=0;
            end
            ter=Tree.RightCurtIndexla;
            Scoretrainl =  tabulate(ter);
            Scoretrainl=Scoretrainl(Scoretrainl(:,2)==max(Scoretrainl(:,2)),1);
            if size(Scoretrainl,1)>1
                mass(CurtIndex,3)=Scoretrainl(1,1);
            else
                mass(CurtIndex,3)=Scoretrainl;
            end
            flag=0;
        end
    end
    if ~isempty(RightCurtIndex)
        mass = SENCMass(Data, RightCurtIndex, Tree.RightChild, mass,cldi,trave,ano);
        if flag==1 
            tempdist=pdist2(Data(CurtIndex,:),Tree.center);
            mass(CurtIndex,2)=(tempdist>Tree.dist*cldi);
            
            if   mass(CurtIndex,1)<ano    &&  mass(CurtIndex,2)==1       
                mass(CurtIndex,5)=1;
            else
                mass(CurtIndex,5)=0;             
            end
            ter=Tree.LeftCurtIndexla;
            Scoretrainl =  tabulate(ter);
            Scoretrainl=Scoretrainl(Scoretrainl(:,2)==max(Scoretrainl(:,2)),1);
            if size(Scoretrainl,1)>1
                mass(CurtIndex,3)=Scoretrainl(1,1);
            else
                mass(CurtIndex,3)=Scoretrainl;
            end
            flag=0;
        end
    end
end

