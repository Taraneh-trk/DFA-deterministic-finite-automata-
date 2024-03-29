import queue
from tkinter import*
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import messagebox

# all dfas
dfalist = []
enter_counter = 0;alphabet_enter = [];state_enter = [];init_state_enter='';final_state_enter={};transition_enter=dict()

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
            dict_ = {'seq':'','seen_num':0}
            final_dict[final] = dict_
        if self.init_state in self.final_state:
            final_dict[self.init_state]['seen_num'] = final_dict[self.init_state]['seen_num']+1
            final_dict[self.init_state]['seq']+=self.init_state
        queue_ = queue.Queue(maxsize=0)
        queue_.put(self.init_state)
        alphabet = list(self.alphabet)
        counter=0
        while not queue_.empty():
            # print(final_dict)
            cur_state = queue_.get()
            saw_l = []
            for alpha in alphabet:
                state = self.transition.get((cur_state,alpha))
                istrap_ = self.istrap(state)
                if not istrap_:
                    temp = string_set_all.copy()
                    for char in temp:
                        char+=alpha
                        string_set_all.append(char)
                        if self.isaccept(char):
                            string_set_accept.add(char)
                if (not istrap_) and (state not in saw_l):
                    saw_l.append(state)
                    queue_.put(state)
                    if state in self.final_state:
                        final_dict[state]['seen_num'] = final_dict[state]['seen_num']+1
                        if final_dict[state]['seen_num'] >=2 and (state in final_dict[state]['seq']):
                            # print(f"state name = {s}      size = { final_dict[s] }")
                            return (False,{})
                        final_dict[state]['seq']+=cur_state
                    if cur_state in self.final_state:
                        final_dict[cur_state]['seq']+=cur_state
                        # final_dict[state]['seq']+=state
            counter+=1;
            if counter==(100*len(self.alphabet)*len(self.state)):
                break
            

        if self.init_state not in self.final_state:
            string_set_accept.remove('')
        return (flag,string_set_accept)


    def isaccept(self,x):
        # true  =>  x is accepted     /    false  =>  x is not accepted
        if x==' ':
            string = x
        string = x.strip()
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
        empty = set()
        if empty in merge_state:
            merge_state.remove(empty)
        empty = tuple()
        if empty in states:
            states.remove(empty)
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
        text_show.insert(INSERT,f'\nalphabet : {self.alphabet}')
        text_show.insert(INSERT,f'\nstates : {self.state}')
        text_show.insert(INSERT,f'\ninitial state : {self.init_state}')
        text_show.insert(INSERT,f'\nfinal states : {self.final_state}')
        text_show.insert(INSERT,'\ntransitions : ')
        for (cur_state,alpha),next_state in self.transition.items():
            text_show.insert(INSERT,f'\n{cur_state}   --({alpha})-->   {next_state}')
        text_show.insert(INSERT,f'\n')
class   Menu:
    def __init__(self):
        pass
    def enter(self,note=''):
        try:
            label.config(text='last action : enter dfa')
            if note!='from equal':
                global enter_counter ; enter_counter=0
                dfalist.clear()
                text_show.insert(INSERT,'please enter dfa\'s data : (write them in the given order in the entry box)\n')
                text_entery.insert(INSERT,'1- dfa\'s alphabet: \n')
                text_entery.insert(INSERT,'2- set of dfa\'s states: \n')
                text_entery.insert(INSERT,'3- dfa\'s initial state: \n')
                text_entery.insert(INSERT,'4- set of dfa\'s final states: ')
            else:
                enter_counter=3
                text_entery.insert(INSERT,'1- dfa\'s alphabet: \n')
                text_entery.insert(INSERT,'2- set of dfa\'s states: \n')
                text_entery.insert(INSERT,'3- dfa\'s initial state: \n')
                text_entery.insert(INSERT,'4- set of dfa\'s final states: ')

        except:
            label.config(text='last action : error in entering dfa',fg='red')


    def isempty(self):
        try:
            label.config(text='last action : isempty ',fg='dodger blue')
            if dfalist[0].isempty() :
                text_show.insert(INSERT,'\nmachine language is empty . \n')
            else:
                text_show.insert(INSERT,'\nmachine language is NOT empty\n')
        except:
            label.config(text='last action : error in isempty ',fg='red')

    def isfinite(self):
        try:
            label.config(text='last action : isfinite ',fg='dodger blue')
            flag,string_set = dfalist[0].isfinite()
            if flag==True:
                text_show.insert(INSERT,'\nmachine language is finite . \n')
                text_show.insert(INSERT,f'number of strings in machine language = {len(string_set)} . \n')
                text_show.insert(INSERT,f'accepted strings by dfa are as follow : {string_set} \n')
            else:
                text_show.insert(INSERT,'\nmachine language is NOT finite . \n')
        except:
            label.config(text='last action : error in isfinite ',fg='red')

    def isaccept(self):
        try:
            label.config(text='last action : isaccept ',fg='dodger blue')
            text_entery.insert(INSERT,f'\nenter a string made of   {dfalist[0].alphabet}   that you want to know if it\'s in dfa language or not :')
            global enter_counter ; enter_counter = 2
            text_show.insert(INSERT,'\nyour entered string :  ')
        except:
            label.config(text='last action : error in isaccept ',fg='red')

    def minimize(self):
        try:
            label.config(text='last action : minimize dfa ',fg='dodger blue')
            mini_dfa = dfalist[0].minimize()
            text_show.insert(INSERT,'\nminimized dfa : \n')
            mini_dfa.show()
        except:
            label.config(text='last action : error in minimize dfa ',fg='red')

    def isequal(self):
        try:
            label.config(text='last action : isequal ',fg='dodger blue')
            text_show.insert(INSERT,'\n HINT : DFAS ALPHABET SHOULD BE THE SAME . \n')
            messagebox.showerror('error','DFAS ALPHABET SHOULD BE THE SAME')
            self.enter('from equal')
        except:
            label.config(text='last action : error in isequal ',fg='red')
    
    def show(self):
        dfalist[0].show()

    def delete(self):
        text_entery.delete("1.0","end")
        text_show.delete("1.0","end")

def enter():
    global enter_counter
    if enter_counter == 0:
        enter_counter+=1
        enter_data = text_entery.get(1.0,END)
        lst = ['']*4;j=0;flag=False
        for i in range(len(enter_data)):
            if(flag==False and enter_data[i]==':'):
                flag = True
            elif (flag==False and enter_data[i]!='\n'):
                continue
            elif (flag==True and enter_data[i]=='\n'):
                j+=1;flag=False
            elif (flag==True and enter_data[i]!='\n'):
                lst[j]+=enter_data[i]
        # print(lst)
        alphabet = list(lst[0].split())
        state = list(lst[1].split())
        init_state = lst[2].strip()
        final_state = set(lst[3].split())
        if final_state=={''}:
            final_state.clear()
        text_entery.delete("1.0","end")#are equal ....
        text_show.delete("1.0","end")
        text_show.insert(INSERT,enter_data)
        text_show.insert(INSERT,'5 - dfa\'s transitions : \n')
        k=0
        for cur_state in state:
            for alpha_transfer in alphabet:
                text_entery.insert(INSERT,f'5-{k} {cur_state}---{alpha_transfer}---> : \n');k+=1
        global alphabet_enter ; alphabet_enter = alphabet ; global state_enter ; state_enter = state
        global init_state_enter ; init_state_enter = init_state ; global final_state_enter ; final_state_enter = final_state
    elif enter_counter==1:
        enter_counter = 0
        enter_data = text_entery.get(1.0,END)
        lst = ['']*(len(state_enter)*len(alphabet_enter));j=0;flag=False
        for i in range(len(enter_data)):
            if(flag==False and enter_data[i]==':'):
                flag = True
            elif (flag==False and enter_data[i]!='\n'):
                continue
            elif (flag==True and enter_data[i]=='\n'):
                j+=1;flag=False
            elif (flag==True and enter_data[i]!='\n'):
                # print(f'j = {j}  i = {i}')
                lst[j]+=enter_data[i]
        for i in range(len(lst)):
            lst[i]=lst[i].strip()
        # print(lst)
        transition = {};index=0
        for cur_state_index in range(len(state_enter)):
            for alpha_transfer_index in range(len(alphabet_enter)):
                transition[(state_enter[cur_state_index],alphabet_enter[alpha_transfer_index])] = lst[index];index+=1
        global transition_enter ; transition_enter = transition
        text_show.insert(INSERT,enter_data)
        text_entery.delete("1.0","end")

        dfalist.append(dfa(set(alphabet_enter),set(state_enter),init_state_enter,final_state_enter,transition_enter))
    elif enter_counter==2:
        x='';flag=False
        enter_data = text_entery.get(1.0,END)
        text_entery.delete("1.0","end")
        for i in range(len(enter_data)):
            if(flag==False and enter_data[i]==':'):
                flag = True
            elif (flag==True):
                # print(f'j = {j}  i = {i}')
                x+=enter_data[i]
        x = x.strip()
        text_show.insert(INSERT,f'{x} \n')
        if dfalist[0].isaccept(x):
            text_show.insert(INSERT,f'\n{x} string is accepted by dfa . \n')
        else:
            text_show.insert(INSERT,f'\n{x} string is NOT accepted by dfa . \n')
    elif enter_counter==3:
        enter_counter+=1
        enter_data = text_entery.get(1.0,END)
        lst = ['']*4;j=0;flag=False
        for i in range(len(enter_data)):
            if(flag==False and enter_data[i]==':'):
                flag = True
            elif (flag==False and enter_data[i]!='\n'):
                continue
            elif (flag==True and enter_data[i]=='\n'):
                j+=1;flag=False
            elif (flag==True and enter_data[i]!='\n'):
                lst[j]+=enter_data[i]
        # print(lst)
        alphabet = list(lst[0].split())
        state = list(lst[1].split())
        init_state = lst[2].strip()
        final_state = set(lst[3].split())
        if final_state=={''}:
            final_state.clear()
        text_entery.delete("1.0","end")
        text_show.insert(INSERT,enter_data)
        text_show.insert(INSERT,'5 - dfa\'s transitions : \n')
        k=0
        for cur_state in state:
            for alpha_transfer in alphabet:
                text_entery.insert(INSERT,f'5-{k} {cur_state}---{alpha_transfer}---> : \n');k+=1
        alphabet_enter = alphabet ; state_enter = state
        init_state_enter = init_state ; final_state_enter = final_state

    elif enter_counter==4:
        enter_data = text_entery.get(1.0,END)
        lst = ['']*(len(state_enter)*len(alphabet_enter));j=0;flag=False
        for i in range(len(enter_data)):
            if(flag==False and enter_data[i]==':'):
                flag = True
            elif (flag==False and enter_data[i]!='\n'):
                continue
            elif (flag==True and enter_data[i]=='\n'):
                j+=1;flag=False
            elif (flag==True and enter_data[i]!='\n'):
                # print(f'j = {j}  i = {i}')
                lst[j]+=enter_data[i]
        for i in range(len(lst)):
            lst[i]=lst[i].strip()
        # print(lst)
        transition = {};index=0
        for cur_state_index in range(len(state_enter)):
            for alpha_transfer_index in range(len(alphabet_enter)):
                transition[(state_enter[cur_state_index],alphabet_enter[alpha_transfer_index])] = lst[index];index+=1
        transition_enter = transition
        text_show.insert(INSERT,enter_data)
        text_entery.delete("1.0","end")

        dfalist.append(dfa(set(alphabet_enter),set(state_enter),init_state_enter,final_state_enter,transition_enter))

        if dfalist[0].isequal(dfalist[1]):
            text_show.insert(INSERT,'two dfas are equal . \n')
        else:
            text_show.insert(INSERT,'two dfas are NOT equal . \n')
        temp = dfalist[0]
        dfalist.clear()
        dfalist.append(temp)


def start_():
        global menu_bar,text_show,text_entery,label
        menu_bar = tk.Menu(window)
        option_menu = tk.Menu(menu_bar,tearoff=0)
        option_menu.add_command(label='1- enter a dfa',command=menu.enter)
        option_menu.add_command(label='2- is the machine language empty ? ',command=menu.isempty)
        option_menu.add_command(label='3- is the machine language finite ?',command=menu.isfinite)
        option_menu.add_command(label='4- is x string accepted or not ?',command=menu.isaccept)
        option_menu.add_command(label='5- minimizing dfa',command=menu.minimize)
        option_menu.add_command(label='6- are the two dfa equal ?',command=menu.isequal)
        option_menu.add_command(label='7- show machine',command=menu.show)
        option_menu.add_command(label='8- delete all data in boxes',command=menu.delete)
        option_menu.add_command(label='9- exit',command=quit)
        menu_bar.add_cascade(label='..........................options.......................... ',menu=option_menu)
        window.config(menu=menu_bar)

        frame = LabelFrame(image_lable,text='DFA\'s data',fg='dodger blue',bg='lightblue1')
        frame.pack(padx=5,pady=5)

        frame_show = LabelFrame(frame,text='show box',fg='dodger blue',bg='lightblue1')
        frame_show.pack(padx=5,pady=5)

        scrollbar_ = Scrollbar(frame_show)
        scrollbar_.pack( side = RIGHT, fill=BOTH , expand=True)

        text_show = Text(frame_show,height=15,width=120,yscrollcommand = scrollbar_.set,background='azure',fg='dodger blue')
        text_show.pack(side = LEFT, fill = BOTH)

        scrollbar_.config( command = text_show.yview )

        frame_entry = LabelFrame(frame,text='entry box',fg='dodger blue',bg='lightblue1')
        frame_entry.pack(padx=5,pady=5)

        scrollbar = Scrollbar(frame_entry)
        scrollbar.pack( side = RIGHT, fill=BOTH , expand=True)

        text_entery = Text(frame_entry,height=15,width=120,yscrollcommand = scrollbar.set,background='azure',fg='dodger blue')

        text_entery.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = text_entery.yview )

        btm = Button(frame,text='enter data',fg='dodger blue',command=enter,width=120,bg='lavender blush')
        btm.pack(anchor='center',padx=5)

        label = Label(frame,text='last action : nothing',border=6,fg='dodger blue',width=119,bg='misty rose')
        label.pack(anchor='center')

        ob.pack_forget()

        messagebox.showerror('error','DO NOT WRITE OR CLICK IN SHOW BOX')


if __name__=='__main__':
    window = Tk()
    window.title("Deterministic Finite Aoutumata (DFA)")
    window.iconbitmap('icon.ico')
    window.state('zoomed')
    w=window.winfo_screenwidth()
    h=window.winfo_screenheight()
    cavas = Canvas(window,width=w,height=h)
    cavas.pack()
    image = ImageTk.PhotoImage(file='dfa.jpg')
    image_lable = Label(cavas,image=image)
    image_lable.pack(ipadx=600,ipady=600)
    ob = Button(image_lable,text='click here to start',fg='dodger blue',height=1,width=20,font=('na',30),command=start_,bg='azure')
    ob.pack(anchor='center',pady=20)
    messagebox.showinfo('author','this app is created by taraneh')
    menu = Menu()

    window.mainloop()