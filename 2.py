# def isequal(self,other):
    #     # true  =>  two dfas are equal
    #     flag = self.state_equal(other,self.init_state,other.init_state)
    #     if flag==False:
    #         return flag

    #     cur_state_s = self.init_state
    #     alphabet_s = list(self.alphabet)
    #     queue_s = queue.Queue(maxsize=0)
    #     queue_s.put(cur_state_s)
    #     nsaw_list_s = []
    #     nsaw_list_s.extend(list(self.state))
    #     cur_state_o = other.init_state
    #     alphabet_o = alphabet_s
    #     queue_o = queue.Queue(maxsize=0)
    #     queue_o.put(cur_state_o)
    #     nsaw_list_o = []
    #     nsaw_list_o.extend(list(other.state))
    #     if len(nsaw_list_o)>=len(nsaw_list_s):
    #         mox = nsaw_list_o
    #     else:
    #         mox = nsaw_list_s

    #     while (not queue_s.empty()) and (not queue_o.empty()) and flag:
    #         cur_state_s = queue_s.get()
    #         cur_state_o = queue_o.get()
    #         if (cur_state_o in nsaw_list_o):
    #             nsaw_list_o.remove(cur_state_o)
    #         if (cur_state_s in nsaw_list_s):
    #             nsaw_list_s.remove(cur_state_s)
    #         flag = self.state_equal(other,cur_state_s,cur_state_o)
    #         if flag==False:
    #             print(f'cur-s = {cur_state_s} \t cur-o = {cur_state_o}')
    #             return flag
    #         for alpha_ in alphabet_s:
    #             queue_s.put(self.transition.get((cur_state_s,alpha_)))
    #             queue_o.put(other.transition.get((cur_state_o,alpha_)))
    #         if len(mox)==0:
    #             return True
            
    #     return True