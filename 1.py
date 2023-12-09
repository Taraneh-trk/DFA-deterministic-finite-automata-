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

    def isempty(self):
    # true -> lang is empty   &   false -> lang is NOT empty 
        if len(self.final_state)==0 : 
            return True
        
        for q in self.final_state : 
            if not self.isunreachable(q) :
                return False
        else:
            return True

    def isfinite(self):
        pass
    def isaccept(self):
        pass
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
        # true  =>  two dfas are equal
        flag = self.state_equal(other,self.init_state,other.init_state)
        if flag==False:
            return flag

        cur_state_s = self.init_state
        alphabet_s = list(self.alphabet)
        queue_s = queue.Queue(maxsize=0)
        queue_s.put(cur_state_s)
        saw_list_s = []
        cur_state_o = other.init_state
        alphabet_o = list(other.alphabet)
        queue_o = queue.Queue(maxsize=0)
        queue_o.put(cur_state_o)
        saw_list_o = []

        while (not queue_s.empty()) and (not queue_o.empty()) and flag:
            cur_state_s = queue_s.get()
            cur_state_o = queue_o.get()
            flag = self.state_equal(other,cur_state_s,cur_state_o)
            if flag==False:
                return flag
            for alpha_s,alpha_o in alphabet_s,alphabet_o:
                queue_s.put(self.transition.get((cur_state_s,alpha_s)))
                queue_o.put(other.transition.get((cur_state_o,alpha_o)))
            # if cur_state_s in saw_list_s :
            #     break
            # if cur_state_s==q:
            #     flag = False
            #     break
            # for alpha in alphabet_s:
            #     queue_s.put(self.transition.get((cur_state_s,alpha)))
            # saw_list_s.append(cur_state_s)
        return True

    def isunreachable(self,q):
        # q is examine state name
        #  true =>  q is unreachable  &  false =>  q is reachable
        flag = True 
        cur_state = self.init_state
        alphabet = list(self.alphabet)
        queue_ = queue.Queue(maxsize=0)
        queue_.put(cur_state)
        saw_list = []
        while (not queue_.empty()) and flag:
            cur_state = queue_.get()
            if cur_state in saw_list :
                break
            if cur_state==q:
                flag = False
                break
            for alpha in alphabet:
                queue_.put(self.transition.get((cur_state,alpha)))
            saw_list.append(cur_state)
            
        return flag

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
        pass

    def isaccept(self):
        pass

    def minimize(self):
        pass

    def isequal(self):
        self.enter()
        if dfalist[0].isequal(dfalist[1]):
            print('two dfas are equal . ')
        else:
            print('two dfas are NOT equal . ')
        temp = dfalist[0]
        dfalist.clear()
        dfalist.append(temp)

if __name__=='__main__':
    menu = Menu()
