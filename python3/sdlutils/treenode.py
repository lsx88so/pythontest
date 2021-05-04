#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, string, random, copy
#import pickle, json

class AttrDisplay:
    def gatherAttrs(self):
        return ",".join("{}={}"
                .format(k, getattr(self, k))
                for k in self.__dict__.keys())
        # attrs = []
        # for k in self.__dict__.keys():
        #   item = "{}={}".format(k, getattr(self, k))
        #   attrs.append(item)
        # return attrs
        # for k in self.__dict__.keys():
        #   attrs.append(str(k) + "=" + str(self.__dict__[k]))
        # return ",".join(attrs) if len(attrs) else 'no attr' 
    
    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())

#class treeNode(AttrDisplay):
class treeNode:
    """
    树结点，可以其它结点的子节点或父结点，每个结点只有一个父结点，可以有0或多个子节点

    结点结构说明：

    :param tag: 结点标记，唯一值，传入None时自行计算，作为判断是否同一个结点的依据
    
    :param parent: 父结点
    
    :param children: 子节点，类型：list
    
    :param data: 数据域，存储结点数据，类型可自定义
    
    :param index: 子节点序号，类型：int.
    """

    def __init__(self, tag=None, parent=None, children=None, data=None, index=None):
        """
        Node Struct：
        :param tag: Node label, unique value, passed into 'None' to calculate by itself,as the basis for judging whether the node is the same or not.
        :param parent: parent node
        :param children: child nodes,type is list
        :param data: data domain，saved node's data，the type can be defined yourself.
        :param index: child node index, type is int.
        """
        if children is None:
            children = []
        self.tag = tag if tag is not None else ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.index = index
        self.parent = parent
        self.children = children
        self.data = data
    
    def __str__(self):
        attrdict = ",".join("{}={}".format(k, getattr(self, k)) for k in self.__dict__.keys())
        
        return "[{}:{}]".format(self.__class__.__name__, attrdict)

    def __deepcopy__(self, memo):
        if memo is None:
            memo = {}
        result = self.__class__()
        memo[id(self)] = result
        #result.parent = self.parent
        #result.index = self.index

        result.data = copy.deepcopy(self.data)
        for node in self.children:
            result.children.append(copy.deepcopy(node))
        for i, _ in enumerate(result.children):
            result.children[i].parent = result
            result.children[i].index = i
        return result

    def Empty(self):
        '''检查结点是否有数据'''
        if self.data is None or len(self.data) == 0:
            return True
        return False

    def insertNode(self, dest_node):
        '''插入子节点，成功返回True，输入的节点不能是其它结点的子节点，否则插入失败，返回False'''
        if dest_node and not dest_node.parent:
            dest_node.parent = self
            dest_node.index = len(self.children)
            self.children.append(dest_node)
    
    #def insertNodeList(self, dest_node_list):
    #    '''插入子节点列表，输入的节点不能是其它结点的子节点'''
    #    node_len = len(dest_node_list)
    #    for i in range(node_len):
    #        if dest_node_list[i].parent:
    #            dest_node_list[i].parent.removeNode(dest_node_list[i])
    #        dest_node_list[i].parent = self
    #        dest_node_list[i].index = len(self.children)
    #        self.children.append(dest_node_list[i])
    
    def moveNode(self, dest_node):
        '''变更其它结点的子节点到本结点下，若无父结点，则直接插入'''
        if dest_node:
            if dest_node.parent:
                dest_node.parent.removeNode(dest_node)
            dest_node.parent = self
            dest_node.index = len(self.children)
            self.children.append(dest_node)

    def removeNode(self, dest_node):
        '''删除一个子节点'''
        if dest_node:
            delFlag = False
            for i, node in enumerate(self.children):
                if self.children[i].tag == dest_node.tag:
                    del self.children[i]
                    delFlag = True
                    break
            if delFlag:
                for j in range(i, len(self.children)):
                    self.children[j].index = j

    def removeNodeByIndex(self, node_index):
        '''通过子节点索引，删除子节点'''
        if node_index < len(self.children):
            del self.children[node_index]
            for j in range(node_index, len(self.children)):
                self.children[j].index = j

    def removeAllNodes(self):
        '''清空该结点的所有子节点'''
        self.children.clear()

    def clearAll(self):
        '''清空结点'''
        self.parent = None
        self.index = None
        self.children.clear()
        self.data.clear()

    @property
    def path(self):
        """返回该结点从根结点开始的路径（结点以对应的Tag表示）"""
        if self.parent:
            return '%s %s' % (self.parent.path.strip(), self.tag)
        return self.tag
    
    def search(self, tag):
        if self.tag == tag:
            return self
        for i, n in enumerate(self.children):
            if n.tag == tag:
                return self.children[i]
            ret = self.search(self.children[i])
            if ret:
                return ret
        return None
    
    def isExist(self, dest_node):
        '''
        判断给定结点是否在该结点下存在（以结点的Tag值为判断依据）
        返回值:
        (ret, tag, path)
        -1: 表示不存在，tag和path为None
        0: 结点本身
        1: 存在于子节点中
        tag: 该结点的tag值
        path: 从根结点到给定结点的路径
        '''
        if self.tag == dest_node.tag:
                return 0, self.tag, self.path
        for i, node in enumerate(self.children):
            if self.children[i].tag == dest_node.tag:
                return 1, self.tag, self.children[i].path
            if len(self.children[i].children) > 0:
                return self.children[i].isExist(dest_node)
        return -1, None, None

    def dumps(self, indent=0):
        """以树形打印"""
        tab = '    ' * (indent - 1) + ' |- ' if indent > 0 else ''
        print('%s%s' % (tab, self.tag))
        for obj in self.children:
            obj.printTag(indent + 1)
