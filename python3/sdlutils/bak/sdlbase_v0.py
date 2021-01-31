#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, string, random, copy

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

class sdlNode(AttrDisplay):
    def __init__(self, parent=None, children=None, field_type=None, field_name=None, field_length=None, field_value=None, seq=None, tag=None):
        """
        结点数据结构
        :param parent:  父节点
        :param children: 子节点，列表结构
        :param field_type: 数据域，数据类型，类型string
        :param field_name: 数据域，字段名，类型string
        :param field_length: 数据域，字段定义的长度，类型string
        :param field_value: 数据域，字段值，类型string
        :param seq: 对应树的真实子节点序号，类型int
        """
        if children is None:
            children = []
        self.tag = tag if tag is not None else ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.parent = parent
        self.children = children
        self.field_type = field_type
        self.field_name = field_name
        self.field_length = field_length
        self.field_value = field_value
        self.seq = seq
    
    def __deepcopy__(self, memo):
        if memo is None:
            memo = {}
        result = self.__class__()
        memo[id(self)] = result
        result.parent = self.parent
        result.children = []
        result.field_type = self.field_type
        result.field_name = self.field_name
        result.field_length = self.field_length
        result.field_value = self.field_value
        result.seq = self.seq
        for node in self.children:
            result.children.append(copy.deepcopy(node))
        for i, node in enumerate(result.children):
            result.children[i].parent = result
        return result

    def Empty(self):
        if not self.field_name and not self.field_value:
            return True
        return False

    def insertNode(self, dest_node):
        dest_node.parent = self
        self.children.append(dest_node)
    
    def insertNodeList(self, dest_node_list):
        node_len = len(dest_node_list)
        for i in range(node_len):
            dest_node_list[i].parent = self
            self.children.append(dest_node_list[i])
    
    def removeNode(self, dest_node):
        for i, node in enumerate(self.children):
            if self.children[i].tag == dest_node.tag:
                del self.children[i]
                break

    def removeNodeByIndex(self, node_index):
        del self.children[node_index]

    def removeAllNodes(self):
        self.children.clear()

    def clearAll(self):
        self.parent = None
        self.children.clear()
        self.field_type = None
        self.field_name = None
        self.field_length = None
        self.field_value = None
        self.seq = None

    def isExist(self, dest_node):
        for i, node in enumerate(self.children):
            if self.children[i].tag == dest_node.tag:
                return True
            if len(self.children[i].children) > 0:
                return self.children[i].isExist(dest_node)
        return False

    def dump(self):
        pass
