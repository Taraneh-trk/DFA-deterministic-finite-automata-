import queue

# all dfas
dfalist = []

def copy(self,me):
    new_list = []
    for s in self:
        st = s.copy()
        new_list.append(st)
    return new_list

class dfa:
    def __init__(self,alphabet,state,init_state,final_state,transition):
        self.alphabet =  alphabet #set of alphabet
        self.state = state       #sef of state
        self.init_state = init_state
        self.final_state = final_state #set of final state
        self.transition = transition #dictionary of  (cur_state,alphabet) : next_state

    def isunreachable(self,q):
        # q is examine state name
        #  true =>  q is unreachable  &  false =>  q is reachable
        flag = True 
        cur_state = self.init_state
        alphabet = list(self.alphabet)
        queue_ = queue.Queue(maxsize=0)
        queue_.put(cur_state)
        saw_list = [self.init_state]
        i=0;mox=len(self.state)*len(self.alphabet)
        while not queue_.empty():
            cur_state = queue_.get()
            saw_list.append(cur_state)
            if cur_state==q:
                flag = False
                break
            for alpha in alphabet:
                goes = self.transition.get((cur_state,alpha))
                if goes not in saw_list:
                    queue_.put(goes)
            if i==mox:  # mox=1000
                break
            i+=1

        return flag

    def isempty(self):
    # true -> lang is empty   &   false -> lang is NOT empty 
        if len(self.final_state)==0 : 
            return True
        
        for q in self.final_state : 
            if not self.isunreachable(q) :
                break
        else:
            return True
        
        return False

    def istrap(self,q):
        # true  =>  q is a trap    /    false  =>  q in NOT a trap
        saw_sat = set()
        alphabet = list(self.alphabet)
        for alpha in alphabet:
            saw_sat.add(self.transition.get((q,alpha)))
        if saw_sat=={q} and (q not in self.final_state):
            return True
        else:
            return False

    def hasloop(self,state,saw_state_set):
        # true =>  (it has aloop on itself)  and  (it is not final)  and  (it was sawn before)
        flag = False
        alphabet = list(self.alphabet)
        for alpha in alphabet:
            next_state = self.transition.get((state,alpha))
            if next_state==state:
                flag = True
                break
        return flag and (state not in self.final_state) and (state in saw_state_set)

    def isfinite(self):
        # true  =>  language is finite  /  false  =>  language is not finite  
        flag = True
        string_set_accept = {''}
        string_set_all = ['']
        if self.isempty():
            return (True,{})
        final_dict = {}
        for final in self.final_state:
            final_dict[final] = 0
        queue_ = queue.Queue(maxsize=0)
        queue_.put(self.init_state)
        alphabet = list(self.alphabet)
        counter=0
        while not queue_.empty():
            cur_state = queue_.get()
            state_set = set() 
            set_cur_state = set()
            for alpha in alphabet:
                state = self.transition.get((cur_state,alpha))
                if not self.istrap(state):
                    temp = string_set_all.copy()
                    for char in temp:
                        char+=alpha
                        string_set_all.append(char)
                        if self.isaccept(char):
                            string_set_accept.add(char)
                set_cur_state.add(state)
            for state in set_cur_state:
                if (not self.istrap(state)):
                    queue_.put(state)
                    state_set.add(state)

            for s in state_set:
                if s in self.final_state:
                    final_dict[s] = final_dict.get(s)+1
                    if final_dict[s]>=2:
                        # print(f'state name = {s}      size = {final_dict[s]}')
                        return (False,{})
            counter+=1;
            if counter==1000:
                break
            

        if self.init_state not in self.final_state:
            string_set_accept.remove('')
        return (flag,string_set_accept)


    def isaccept(self,x):
        # true  =>  x is accepted     /    false  =>  x is not accepted
        string = x
        cur_state = self.init_state
        if cur_state in self.final_state:
            flag = True
        else:
            flag = False
        while len(string)!=0:
            cur_state = self.transition.get((cur_state,string[0]))
            string = string[1:]  # omitting first character
            if cur_state in self.final_state:
                flag = True
            else:
                flag = False
        
        return flag

    def minimize(self): 
        if self.isempty():
            print('machine language is empty . ')
            return self
        # ommit unreachable states
        unreachable_state = set()
        for st in self.state:
            if self.isunreachable(st):
                unreachable_state.add(st)
        state_without_unreachable = self.state - unreachable_state
        final_without_unreachable = self.final_state - unreachable_state

        print(state_without_unreachable , final_without_unreachable)

        alphabet = self.alphabet
        states = set()
        init_state = self.init_state
        final_state = set()
        transition = dict()

        finals = list(final_without_unreachable)
        non_finals = list(state_without_unreachable - set(finals))
        # print('final = ',finals,'nonfinal = ',non_finals)
        
        merge_state_nf = [set(non_finals)]
        merge_state_next_nf = copy(merge_state_nf,'me')
        merge_state_f = [set(finals)]
        merge_state_next_f = copy(merge_state_f,'me')
        flag_repeat = False;level=0
        while flag_repeat == False:
            for s1 in non_finals:
                for s2 in non_finals[non_finals.index(s1)+1:]:
                    if not self.mergable(s1,s2,alphabet,merge_state_next_nf,merge_state_next_f):
                        merge_state_next_nf = self.seperate_in_merge_state(merge_state_nf,merge_state_next_nf,merge_state_next_f,s1,s2,alphabet)
                        # print('\nmerg : ',merge_state_next_nf)
            for s1 in finals:
                for s2 in finals[finals.index(s1)+1:]:
                    if not self.mergable(s1,s2,alphabet,merge_state_next_f,merge_state_next_nf):
                        merge_state_next_f = self.seperate_in_merge_state(merge_state_f,merge_state_next_f,merge_state_next_nf,s1,s2,alphabet)
            # print('level = ',level);level+=1
            if merge_state_nf == merge_state_next_nf and merge_state_f == merge_state_next_f:
                flag_repeat = True
            merge_state_nf = copy(merge_state_next_nf,'me')
            merge_state_f = copy(merge_state_next_f,'me')
            

        # print('\nmergables nf: ',merge_state_nf)
        # print('\nmergables f: ',merge_state_f)
        
        merge_state = merge_state_f + merge_state_nf

        # print(f'merge_state = {merge_state}')

        for s in merge_state:
            states.add(tuple(s))
            if init_state in s:
                init_state = tuple(s)
            for fs in self.final_state:
                if fs in s:
                    final_state.add(tuple(s))
            
        #transition
        for s in merge_state:
            name = tuple(s)
            for alpha in alphabet:
                # print(name," ")
                name0_alpha = self.transition.get((name[0],alpha))
                for q in states:
                    if name0_alpha in q:
                        name_alpha = q
                transition[(name,alpha)] = name_alpha

        return dfa(alphabet,states,init_state,final_state,transition)

    def mergable(self,s1,s2,alphabet,merge_state_nf,merge_state_f):
        for alpha in alphabet:
            s1_alpha = self.transition.get((s1,alpha))
            s2_alpha = self.transition.get((s2,alpha))
            if not self.is_in_one_set(merge_state_nf,merge_state_f,s1_alpha,s2_alpha):
                return False
        return True

    def is_in_one_set(self,merge_state_nf,merge_state_f,s1,s2):
        subset = {s1,s2}
        for st in merge_state_nf:
            if subset.issubset(st):
                return True
        for st in merge_state_f:
            if subset.issubset(st):
                return True
        return False

    def seperate_in_merge_state(self,merge_state,merge_state_next_nf,merge_state_next_f,s1,s2,alphabet):
        temp= list()
        index = 0
        flag_remove = False
        # print('merge in sep start',merge_state_next_nf)
        # print('merge before start : ',merge_state)
        mrg_temp = copy(merge_state,'me')
        for mrg in merge_state_next_nf:
            if {s1,s2}.issubset(mrg):
                index = merge_state_next_nf.index(mrg)
                mrg.remove(s2)
                temp.append(mrg)
                flag_remove = True
        if flag_remove == True:
            flag = False
            for mrg_index in range(len(merge_state_next_nf)):
                if mrg_index == index:
                    continue
                for s3 in merge_state_next_nf[mrg_index]:
                    if self.mergable(s2,s3,alphabet,merge_state,merge_state_next_f):
                        merge_state_next_nf[mrg_index].add(s2)
                        temp.append(merge_state_next_nf[mrg_index])
                        flag = True
                    else:
                        temp.append(merge_state_next_nf[mrg_index])
                    break
            if flag == False:
                temp.append({s2,})
            # print('merge in sep end',temp)
            merge_state = copy(mrg_temp,'me')
            # print('merge before end : ',merge_state)
            return temp
        return merge_state_next_nf



    def state_equal(self,other,s1,s2):
        # s1 belongs to self     /     s2 belongs to other
        # return true if (both s1 & s2 state are final) or (both s1 & s2 state are NOT final)
        if (s1 in self.final_state) and (s2 in other.final_state):
            return True
        elif (s1 not in self.final_state) and (s2 not in other.final_state):
            return True
        else:
            return False
        
    def isequal(self,other):
        saw_list = [(self.init_state,other.init_state),(None,None)]
        flag = self.state_equal(other,saw_list[0][0],saw_list[0][1])
        if flag==False:
            return False
        alphabet = list(self.alphabet)
        i = 0
        while(saw_list[i][0]!=None):
            state_s , state_o = saw_list[i][0] , saw_list[i][1];  i+=1
            for alpha in alphabet:
                new_tuple = (self.transition.get((state_s,alpha)),other.transition.get((state_o,alpha)))
                flag = self.state_equal(other,new_tuple[0],new_tuple[1])
                if flag==False:
                    return False
                if new_tuple not in saw_list:
                    saw_list.insert(len(saw_list)-1,new_tuple)
        
        return True
    
    def show(self):
        print(f'\nalphabet : {self.alphabet}')
        print(f'states : {self.state}')
        print(f'initial state : {self.init_state}')
        print(f'final states : {self.final_state}')
        print('transitions : \n')
        for (cur_state,alpha),next_state in self.transition.items():
            print(f'{cur_state}   --({alpha})-->   {next_state}')
        print()

class   Menu:
    def __init__(self):
        while True:
            print('options : ')
            print('\t1- enter a dfa')
            print('\t2- is the machine language empty ? ')
            print('\t3- is the machine language finite ? ')
            print('\t4- is x string accepted or not ? ')
            print('\t5- minimizing dfa')
            print('\t6- are the two dfa equal ?')
            print('\t7- show machine')
            print('\t8- exit')
            choose = int(input('enter your selection : \n'))
            if choose==1:
                self.enter()
            elif choose==2:
                self.isempty()
            elif choose==3:
                self.isfinite()
            elif choose==4:
                self.isaccept()
            elif choose==5:
                self.minimize()
            elif choose==6:
                self.isequal()
            elif choose==7:
                self.show()
            elif choose==8:
                exit()

    def enter(self,note=''):
        if note!='from equal':
            dfalist.clear()
        print('please enter dfa\'s data : ')
        alphabet = set(input('write each letter of your alphabet and leave a space between each of them : \n').strip(' ').split(' '))
        state = set(input('write state\'s name of your dfa and leave a space between each of them : \n').strip(' ').split(' '))
        init_state = input('write the name of initial state : \n')
        final_state = set(input('write final states name of your dfa and leave a space between each of them : \n').strip(' ').split(' '))
        if final_state=={''}:
            final_state.clear()
        transition = {}
        for cur_state in state:
            for alpha_transfer in alphabet:
                next_state = input(f'enter the state which   {cur_state}   goes with   {alpha_transfer}   : \n')
                transition[(cur_state,alpha_transfer)] = next_state

        dfalist.append(dfa(alphabet,state,init_state,final_state,transition))


    def isempty(self):
        if dfalist[0].isempty() :
            print('\tmachine language is empty . \n')
        else:
            print('\tNOT empty\n')
        # print(dfalist[0].isunreachable('q3'))

    def isfinite(self):
        flag,string_set = dfalist[0].isfinite()
        if flag==True:
            print('\nmachine language is finite . ')
            print(f'number of strings in machine language = {len(string_set)} . ')
            print(f'accepted strings by dfa are as follow : {string_set}\n')
        else:
            print('\nmachine language is NOT finite . \n')

    def isaccept(self):
        x = input(f'\nenter a string made of   {dfalist[0].alphabet}   that you want to know if it\'s in dfa language or not . \n')
        if dfalist[0].isaccept(x):
            print(f'\n{x} string is accepted by dfa . \n')
        else:
            print(f'\n{x} string is NOT accepted by dfa . \n')

    def minimize(self):
        mini_dfa = dfalist[0].minimize()
        print('\nminimized dfa : \n')
        mini_dfa.show()

    def isequal(self):
        print('\n HINT : DFAS ALPHABET SHOULD BE THE SAME . \n')
        self.enter('from equal')
        if dfalist[0].isequal(dfalist[1]):
            print('\ntwo dfas are equal . \n')
        else:
            print('\ntwo dfas are NOT equal . \n')
        temp = dfalist[0]
        dfalist.clear()
        dfalist.append(temp)
    
    def show(self):
        dfalist[0].show()

if __name__=='__main__':
    menu = Menu()
