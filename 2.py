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


# cur_state = self.init_state
#         saw_list = [cur_state]
#         alphabet = list(self.alphabet)
#         flag = True
#         i=0
#         while True:
#             saw_set = set()
#             for alpha in alphabet:
#                 state = self.transition.get((saw_list[i],alpha));i+=1
                
#             for state in saw_set:
#                 if state in self.final_state:
#                     final_dict[state] = final_dict.get(state)+1
#                     if final_dict[state]>=2:
#                         flag = False
#                         break
#             if flag==False:
#                 break

#         return flag

# print(all([True,True,1,1,0]))



# minimize
# merge_state = []
#         for state_index in range(len(non_finals)):
#             for cmp_state_index in range(state_index,len(non_finals)):
#                 falg_list = []
#                 falg_list.append(self.state_equal(self,non_finals[state_index],non_finals[cmp_state_index]))
#                 for alpha in alphabet:
#                     s1 = self.transition.get((non_finals[state_index],alpha))
#                     s2 = self.transition.get((non_finals[cmp_state_index],alpha))
#                     falg_list.append(self.state_equal(self,s1,s2))
#                 if all(falg_list):
#                     for lst in merge_state:
#                         if (non_finals[cmp_state_index] in lst) or (non_finals[state_index] in lst):
#                             lst1 = set(lst)
#                             lst1.add(non_finals[cmp_state_index])
#                             lst1.add(non_finals[state_index])
#                             lst1 = list(lst1)
#                             index = merge_state.index(lst)
#                             merge_state[index] = lst1
#                     else:
#                         merge = list({non_finals[state_index],non_finals[cmp_state_index]})
#                         merge_state.append(merge)

#         for state_index in range(len(finals)):
#             for cmp_state_index in range(state_index,len(finals)):
#                 falg_list = []
#                 falg_list.append(self.state_equal(self,finals[state_index],finals[cmp_state_index]))
#                 for alpha in alphabet:
#                     s1 = self.transition.get((finals[state_index],alpha))
#                     s2 = self.transition.get((finals[cmp_state_index],alpha))
#                     falg_list.append(self.state_equal(self,s1,s2))
#                 if all(falg_list):
#                     for lst in merge_state:
#                         if (finals[cmp_state_index] in lst) or (finals[state_index] in lst):
#                             lst1 = set(lst)
#                             lst1.add(finals[cmp_state_index])
#                             lst1.add(finals[state_index])
#                             lst1 = list(lst1)
#                             index = merge_state.index(lst)
#                             merge_state[index] = lst1
#                             break
#                     else:
#                         merge = list({finals[state_index],finals[cmp_state_index]})
#                         merge_state.append(merge)

        # state_dict = dict()
        # for state_lst in merge_state:
        #     """ (constructors states name)[states name] : 
        #     (alpha , set to tuple(next_state for any alpha)[transition], 
        #     is final or not [finals], )"""
        #     key = tuple(state_lst) #should be set
            
        #     value1 = list() #(alpha_,)
        #     for alpha_ in alphabet:
        #         tran = set()
        #         for state in  state_lst:
        #             tran.add(self.transition.get((state,alpha_)))
        #             for mrg in merge_state:
        #                 if tran.issubset(set(mrg)):
        #                     tran = set(mrg)
        #         value1.append((alpha_,tran))

        #     value2 = False
        #     for state in state_lst:
        #         if state in self.final_state:
        #             value2 = True
        #             break
        #     else:
        #         value2 = False

        #     state_dict[key] = (value1,value2)
        
        # print('state dict = ',state_dict,'\nmergeable = ',merge_state)

        # for key_,val in state_dict.items():
        #     states.add(key_)
        #     if val[1]==True:
        #         final_state.add(key_)
        #     for i in val[0]:
        #         next_state = key_ if set(key_)==i[1] else tuple(i[1])
        #         transition[(key_,i[0])] = next_state 


# lst = [{1,2},{3,4}]
# print(lst)

# index = 0 
# temp = []
# flag = False
# for s in lst:
#     if {1}.issubset(s):
#         index = lst.index(s)
#         s.remove(1)
#         temp.append(s)
# for i in range(len(lst)):
#     if i == index:
#         continue
#     for s in lst[i]:
#         lst[i].add(1)
#         temp.append(lst[i])
#         break

# if flag == False:
#     temp.append({1})

# print(temp)

# s = set()
# string = 'taras'
# print({string,})

st = {1,2,3,4}
s1=tuple(st)
s2=tuple(st)
print(s1)
print(s2)