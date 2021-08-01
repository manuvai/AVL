# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:51:33 2019

@author: mrehua
"""

import copy

class AVL:
    class __Node:
        def __init__(self,val,g = None,d = None):
            self.val = val
            self.g = g
            self.d = d
            self.bal = 0
        
        def prefixe(self):
            def __prefixe(root,L):
                if root == None:
                    return
                else:
                    L.append(root.val)
                    __prefixe(root.g,L)
                    __prefixe(root.d,L)
                    return L
            return __prefixe(self,[])
        
        def drot_d(self):
            def __rot(root):
                b = copy.deepcopy(root)
                b.g = b.g.rot_g()
                
                return b.rot_d()
            return __rot(self)
        
        def drot_g(self):
            def __rot(root):
                b = copy.deepcopy(root)
                b.d = b.d.rot_d()
                
                return b.rot_g()
            return __rot(self)
        
        def rot_g(self):
            def __rot(root):
                b = copy.deepcopy(root.d)
                a = root.bal
                bb = b.bal
                
                root.d = b.g
                b.g = root
                
                b.g.bal = a - max(bb,0) - 1
                b.bal = min(a-2,a+bb-2,bb-1)
                return b
            
            return __rot(self)
            
        def rot_d(self):
            def __rot(root):
                b = copy.deepcopy(root.g)
                a = root.bal
                bb = b.bal
                
                """
                
                
                """
                root.g = b.d
                b.d = root
                
                b.d.bal = a - min(bb,0) + 1
                b.bal = max(a+2,a+bb+2,bb+1)
                
                return b
            return __rot(self)
        
        def getHeight(self):
            if not self.d and not self.g:
                return 0
            elif not self.g:
                return 1 + self.d.getHeight()
            elif  not self.d:
                return 1 + self.g.getHeight()
            else:
                return 1 + max(self.d.getHeight(),self.g.getHeight())
            
        def balance(self):
            def __balance(root):
                if (root.bal == 2):
                    if (root.d != None and root.d.bal >= 0):
                        return root.rot_g()
                    elif root.d != None:
                        return root.drot_g()
                    else:
                        return root
                    
                elif root.bal == -2:
                    if (root.g != None and root.g.bal <= 0):
                        return root.rot_d()
                    elif root.g != None:
                        return root.drot_d()
                    else:
                        return root
                else:
                    return root
            return __balance(self)
        
        
    def __init__(self):
        self.root = None
    
    def ajout(self,x):
        def __ajout(root,x):
            if root == None:
                return (AVL.__Node(x),1)
            elif x == root.val:
                return (root,0)
            elif x > root.val:
                root.d , h = __ajout(root.d,x)
            else:
                root.g , h = __ajout(root.g,x)
                h = -h
            if h == 0:
                return (root,0)
            else:
                root.bal = root.bal + h
                root = root.balance()
                
                if root.bal == 0:
                    return (root,0)
                else:
                    return (root,1)
        self.root,temp  = __ajout(self.root,x)
        self.rebalance()
        
    def insert(self,val):
        def __insert(root,val):
            if root == None:
                return AVL.__Node(val)

            if val < root.val:
                root.g = __insert(root.g,val)
            else:
                
                root.d = __insert(root.d,val)
            
            return root
           
        self.root = __insert(self.root,val)
        
    def enleve(self,x):
        def __min(root):
            if root.g == None:
                return root.val
            else:
                return __min(root.g)
            return
        
        def __otermin(root):
            if root.g == None:
                return root.d,1
            else:
                root.g,h = __otermin(root.g)
                h = -h
            
            if h == 0:
                return root,0
            else:
                root.bal = root.bal + h
                root = root.balance()
                
                if root.bal == 0:
                    return root,-1
                else:
                    return root,0
            return
        
        def __enleve(root,x):
            if root == None:
                return root,0
            elif x > root.val:
                root.d , h = __enleve(root.d , x)
            elif x < root.val:
                root.g , h = __enleve(root.g , x)
                h = -h
            elif root.g == None:
                return (root.d, -1)
            elif root.d == None:
                return (root.g, -1)
            else:
                root.val = __min(root.d)
                root.d, h = __otermin(root.d)
            
            if h == 0:
                return root,0
            else:
                root.bal = root.bal +h
                root = root.balance()
                if root.bal == 0:
                    return root,-1
                else:
                    return root,0
        
        self.root,temp = __enleve(self.root,x)
        self.rebalance()
        
    def rebalance(self):
        def __rebalance(root):
            response = None
            
            if root != None:
                response = copy.deepcopy(root)
                
                response.d = __rebalance(response.d)
                
                response = response.balance()
                
                response.g = __rebalance(response.g)
            
            return response
        self.root = __rebalance(self.root)
        
    def __str__(self):
        self.affiche()
        return ''
            
    def affiche(self):
        def __affiche(root,s,f):
            if root != None:
                if root.d != None:
                    __affiche(root.d,s+1,f)
                else:
                    __affiche(None,s+1,f)

                for i in range(s):
                    print("  ",end='')
                print(str(root.val))

                if root.g != None:
                    __affiche(root.g,s+1,f)
                else:
                    __affiche(None,s+1,f)
                    
                    
            else:
                if s < f:
                    __affiche(None,s+1,f)
                    for i in range(s):
                        print("  ",end="")
                    print("-\n",end='')
                    
                    __affiche(None,s+1,f)
        s = 0
        f = self.root.getHeight()
        __affiche(self.root,s,f)
        
        
        

def main():
    A = AVL()
    T = [4,3,1,6,7,5,2,8]
    
    for i in T:
        A.ajout(i)
        A.affiche()
        print('----------------')
    return
 

if __name__ == "__main__":
    main()
