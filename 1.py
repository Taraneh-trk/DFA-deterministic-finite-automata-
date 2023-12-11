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

    def isfinite(self):  #defective
        # true  =>  language is finite (not correct) /  false  =>  language is not finite  (correct)
        flag = True
        string_set = {}
        if self.isempty():
            return (True,string_set)
        final_dict = {}
        for final in self.final_state:
            final_dict[final] = 0
        queue_ = queue.Queue(maxsize=0)
        queue_.put(self.init_state)
        alphabet = list(self.alphabet)
        while True:
            cur_state = queue_.get()
            state_set = {cur_state}
            for alpha in alphabet:
                state = self.transition.get((cur_state,alpha))
                if not self.istrap(state):
                    queue_.put(state)
                    state_set.add(state)
            for s in state_set:
                if s in self.final_state:
                    final_dict[s] = final_dict.get(s)+1
                    if final_dict[s]>=2:
                        return (False,string_set)
            

        return (flag,string_set)


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
        pass

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
            print('\t7- exit')
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
        pass

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

if __name__=='__main__':
    menu = Menu()
