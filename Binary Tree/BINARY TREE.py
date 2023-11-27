"""
This module implements a binary tree data structure. It provides classes and functions to create a binary tree, 
add nodes to it, identify leaves and root nodes, and perform depth-first search (DFS) traversals. The module also 
includes visualization capabilities using matplotlib to graphically represent the binary tree structure, showing 
the nodes and their connections.
"""

import matplotlib.pyplot as plt
class binaryTree:
    def __init__(self,nNodes=0,parent= None, leftChild = None,rightChild = None):
        self.nNodes = nNodes
        self.prnt = parent
        self.l_child = leftChild
        self.r_child = rightChild
        # initialize tree structures, build default tree
        self.nodeChildren = {}
        self.nodeParent = {}
        self.treeXY={}
        self.addNodes(nNodes)

        
    def addTrio(self,parent,leftChild,rightChild):
        """
        Adds a trio of nodes (parent, left child, right child) to the binary tree.

        Parameters:
        parent : object
            The parent node.
        leftChild : object
            The left child of the parent node.
        rightChild : object
            The right child of the parent node.
        """
        dict_children={parent:(leftChild,rightChild)}
        self.nodeChildren.update(dict_children)
        dict_parent = {leftChild:parent,rightChild:parent}
        self.nodeParent.update(dict_parent)
        
    def setRoots(self):
        """
        Identifies and sets the root nodes of the binary tree.

        This function iterates through all nodes and finds those that are not listed as children of any other node, thus identifying them as roots.

        Returns:
        object: The first root node found in the binary tree.
        """
        self.roots=[]
        for p in self.nodes():
            if p not in self.nodeParent.keys():
                self.roots.append(p)
        return (self.roots[0])
    
    def dfsTraverseRecursive(self,node,dfsNodeList,xMaxLeaf=0,yNode=0):
        """
        Performs a depth-first search (DFS) traversal of the binary tree recursively, setting the x and y coordinates for each node.

        Parameters:
        node : object
            The current node being processed in the DFS traversal.
        dfsNodeList : list
            A list that accumulates the nodes in the order they are visited during DFS.
        xMaxLeaf : int, optional
            The maximum x-coordinate value among the leaf nodes, used for positioning the nodes (default is 0).
        yNode : int, optional
            The y-coordinate value for the current node (default is 0).

        Returns:
        tuple: A tuple containing the updated dfsNodeList and xMaxLeaf after processing the current node.
        """
        # traverse the tree using dfs. set x and y location as we go.
        # find my children
        if node in self.nodeChildren.keys():
            (cLeft,cRight)=self.nodeChildren[node]
            # traverse
            (dfsNodeList,xMaxLeaf)=self.dfsTraverseRecursive(cLeft,dfsNodeList,xMaxLeaf,yNode+1)
            # traverse right child
            (dfsNodeList,xMaxLeaf)=self.dfsTraverseRecursive(cRight,dfsNodeList,xMaxLeaf,yNode+1)
            # after we're done with both children, set parent x midway between children x location.
            self.treeXY[node] = ((self.treeXY[cLeft][0]+self.treeXY[cRight][0])/2,yNode)
            pass
        else:
            # node has no children. it's a leaf. set it's x
            self.treeXY[node]=(xMaxLeaf,yNode)
            xMaxLeaf+=1
            pass
        dfsNodeList.append(node)
        
        return (dfsNodeList,xMaxLeaf)

    def nodes(self):
        """
        Retrieves all the nodes present in the binary tree.

        The function creates a set of all nodes by combining the keys from nodeChildren and nodeParent dictionaries.

        Returns:
        set: A set of all nodes in the binary tree. If the tree is empty, returns a set containing a single root node {0}.
        """
        # return the set of all nodes in the tree
        nodes=set(self.nodeChildren.keys()).union(set(self.nodeParent.keys()))
        # note - if the tree is empty, return a single root node {0}
        if len(nodes) == 0 :
            nodes.add(0)
        return nodes
    
    def leaves(self):
        """
        Identifies and returns all the leaf nodes of the binary tree.

        A node is considered a leaf if it is not a parent to any other node.

        Returns:
        set: A set of all leaf nodes in the binary tree.
        """
        # return the set of all leaves in the tree
        # a node is a leaf if it's not in self.nodeChildren.keys():
        leaves=set()
        for p in self.nodes() :
            if p not in self.nodeChildren.keys():
                leaves.add(p)
        return leaves
    
    def dfsTraverse(self):
        """
        Performs a complete depth-first search (DFS) traversal of the binary tree.

        This function finds all root nodes and conducts a DFS traversal from each root, compiling a list of nodes visited in DFS order.

        Returns:
        list: A list of nodes representing the DFS traversal order of the binary tree.
        """
        self.setRoots()
        dfs=[]
        # each root node will be processed to append its dfs traversal to the dfs list
        # here we will only test / use trees with a single root
        for r in self.roots:
            dfs=self.dfsTraverseRecursive(r,dfs)
        return dfs
    
    def render(self,node):
        """
        Renders a visual representation of the binary tree using matplotlib.

        This function plots each node and its connections to its children, aligning the text based on the node's position.

        Parameters:
        node : object
            The node to be rendered in the plot.
        """

        xy=self.treeXY[node]
        # plot a vertical blue solid line at node.x from node.y to node.y+1
        plt.plot((xy[0], xy[0]), (xy[1], xy[1]+1), 'b-')
        # text align right for child 0, left for child 1
        if node in self.nodeParent.keys():
            # p is node's parent
            p=self.nodeParent[node]
            # cx are node's parent's two children. node should be one of them.
            cx=self.nodeChildren[p]
            # if node is the left child, align right
            if node is cx[0]:
                align ="right"
            # else align left
            else:
                align='left'
        else:
            # no parent - node is the root
            align='center'
        plt.text(xy[0],xy[1],str(node),horizontalalignment=align)
        # if node has children, draw a horizontal line in solid blue
        # between the two children x locations, at the children y location
        if node in self.nodeChildren.keys():
            (left, right) = self.nodeChildren[node]
           
            plt.plot((self.treeXY[left][0],self.treeXY[right][0]),(self.treeXY[left][1],self.treeXY[right][1]), 'b-')
            
            # now render the left child then the right child
            self.render(left)
            self.render(right)

    def addNodes(self,nNodes):
        """
        Adds a specified number of nodes to the binary tree.

        New nodes are added as children to existing leaf nodes. The function ensures the binary tree's structure is maintained.

        Parameters:
        nNodes : int
            The number of new nodes to be added to the tree.
        """
        # add nNodes new nodes to the tree
        n0=len(self.nodes()) # current nodes in tree
        nNodes=nNodes+n0 # target tree size
        while len(self.nodes())+2<=nNodes:
            print(len(self.nodes()))
            for l in self.leaves():
                if len(self.nodes())+2>nNodes:
                    break
                mm=max(self.nodes())
                self.addTrio(l,mm+1,mm+2)
        # after we add new nodes to the tree, we reset everyone's xy locations
        # by invoking a dfsTraverse
        self.dfsTraverse()

def myNumberOfNodes(emailAddress):
    """
    Generates a number of nodes based on the hash of an email address.

    This function is used to create a variable number of nodes for the binary tree based on the given email address.

    Parameters:
    emailAddress : str
        The email address used to generate the number of nodes.

    Returns:
    int: A calculated number of nodes based on the hash of the email address.
    """
    hash = 0
    for c in emailAddress:
        hash += ord(c)
    return 17+hash%15

if __name__=="__main__":
    node_no =myNumberOfNodes('to344@drexel.edu')
    def_tree = binaryTree(node_no)
    
    def_tree.render(def_tree.setRoots())
    
    # set the yticks, ylabel, xticks and xlabel too
    plt.ylabel("generation")
    plt.gca().invert_yaxis()
    plt.xticks (ticks=[0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0])
    plt.title ("binary tree with {} nodes".format(node_no))

    plt.show()