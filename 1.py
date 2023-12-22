import queue

# all dfas
dfalist = []

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
        nsaw_list = []
        nsaw_list.extend(list(self.state))
        while (not queue_.empty()) and flag:
            cur_state = queue_.get()
            if cur_state in nsaw_list :
                nsaw_list.remove(cur_state)
            if cur_state==q:
                flag = False
                break
            for alpha in alphabet:
                queue_.put(self.transition.get((cur_state,alpha)))
            nsaw_list.append(cur_state)
            if len(nsaw_list)==0:
                break

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
                        print(f'state name = {s}      size = {final_dict[s]}')
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

    def minimize(self): #debugging.....
        # ommit unreachable states
        unreachable_state = set()
        for st in self.state:
            if self.isunreachable(st):
                unreachable_state.add(st)
        state_without_unreachable = self.state - unreachable_state
        final_without_unreachable = self.final_state - unreachable_state

        alphabet = self.alphabet
        states = set()
        init_state = self.init_state
        final_state = set()
        transition = dict()

        finals = list(final_without_unreachable)
        non_finals = list(state_without_unreachable - set(finals))
        # print('final = ',finals,'nonfinal = ',non_finals)
        merge_state = []
        for state_index in range(len(non_finals)):
            for cmp_state_index in range(state_index,len(non_finals)):
                falg_list = []
                falg_list.append(self.state_equal(self,non_finals[state_index],non_finals[cmp_state_index]))
                for alpha in alphabet:
                    s1 = self.transition.get((non_finals[state_index],alpha))
                    s2 = self.transition.get((non_finals[cmp_state_index],alpha))
                    falg_list.append(self.state_equal(self,s1,s2))
                if all(falg_list):
                    for lst in merge_state:
                        if (non_finals[cmp_state_index] in lst) or (non_finals[state_index] in lst):
                            lst1 = set(lst)
                            lst1.add(non_finals[cmp_state_index])
                            lst1.add(non_finals[state_index])
                            lst1 = list(lst1)
                            index = merge_state.index(lst)
                            merge_state[index] = lst1
                    else:
                        merge = list({non_finals[state_index],non_finals[cmp_state_index]})
                        merge_state.append(merge)

        for state_index in range(len(finals)):
            for cmp_state_index in range(state_index,len(finals)):
                falg_list = []
                falg_list.append(self.state_equal(self,finals[state_index],finals[cmp_state_index]))
                for alpha in alphabet:
                    s1 = self.transition.get((finals[state_index],alpha))
                    s2 = self.transition.get((finals[cmp_state_index],alpha))
                    falg_list.append(self.state_equal(self,s1,s2))
                if all(falg_list):
                    for lst in merge_state:
                        if (finals[cmp_state_index] in lst) or (finals[state_index] in lst):
                            lst1 = set(lst)
                            lst1.add(finals[cmp_state_index])
                            lst1.add(finals[state_index])
                            lst1 = list(lst1)
                            index = merge_state.index(lst)
                            merge_state[index] = lst1
                            break
                    else:
                        merge = list({finals[state_index],finals[cmp_state_index]})
                        merge_state.append(merge)

        state_dict = dict()
        for state_lst in merge_state:
            """ (constructors states name)[states name] : 
            (alpha , set to tuple(next_state for any alpha)[transition], 
            is final or not [finals], )"""
            key = tuple(state_lst) #should be set
            
            value1 = list() #(alpha_,)
            for alpha_ in alphabet:
                tran = set()
                for state in  state_lst:
                    tran.add(self.transition.get((state,alpha_)))
                    for mrg in merge_state:
                        if tran.issubset(set(mrg)):
                            tran = set(mrg)
                value1.append((alpha_,tran))

            value2 = False
            for state in state_lst:
                if state in self.final_state:
                    value2 = True
                    break
            else:
                value2 = False

            state_dict[key] = (value1,value2)
        
        # print('state dict = ',state_dict,'mergeable = ',merge_state)

        for key_,val in state_dict.items():
            states.add(key_)
            if val[1]==True:
                final_state.add(key_)
            for i in val[0]:
                next_state = key_ if set(key_)==i[1] else tuple(i[1])
                transition[(key_,i[0])] = next_state 

        return dfa(alphabet,states,init_state,final_state,transition)


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

    def enter(self):
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
        self.enter()
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
