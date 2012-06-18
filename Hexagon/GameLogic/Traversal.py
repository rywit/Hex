
class Traversal:
    
    @classmethod
    def makeNodes( cls, grid ):
    
        nodes = [];
    
        paddingrow = [ None for x in range( len( grid ) + 2 ) ] #@UnusedVariable
        nodes.append( paddingrow )
    
        startingNodes = set();
    
        rownum = 0
        while rownum < len( grid ):
            row = grid[ rownum ]
            isEnd = rownum == len( grid ) - 1
    
            ## Begin building up this row
            noderow = [ None ]
    
            colnum = 0
            while colnum < len( grid ):
    
                elem = row[ colnum ]
    
                if elem == 0:
                    noderow.append( None )
                else:
                    node = Node( "[%d, %d]" % ( rownum, colnum ), isEnd )
                    noderow.append( node )
                    if rownum == 0:
                        startingNodes.add( node )
    
                ## Increment col counter
                colnum += 1
    
            ## End iterating through columns
            noderow.append( None )
            nodes.append( noderow )
            rownum += 1
    
        ## Add empty  last row
        nodes.append( paddingrow )
    
        ## Hook up neighbors    
        rownum = 1
        while rownum < len( nodes ) - 1:
            row = nodes[ rownum ]
    
            colnum = 1
            while colnum < len( nodes ) - 1:
    
                elem = row[ colnum ]
    
                if elem:
    
                    top1 = nodes[ rownum - 1 ][ colnum ];
                    top2 = nodes[ rownum - 1 ][ colnum + 1 ];
                    left = nodes[ rownum ][ colnum - 1 ];
                    right = nodes[ rownum ][ colnum + 1 ];
                    bottom1 = nodes[ rownum + 1 ][ colnum - 1];
                    bottom2 = nodes[ rownum + 1 ][ colnum ];
    
                    for x in [ top1, top2, left, right, bottom1, bottom2 ]:
                        if x:
                            elem.siblings.append( x )
    
                colnum += 1
            rownum += 1
    
        return startingNodes

    @classmethod
    def hasTraversal( cls, node, seen ):
    
        ## Copy the set of visited nodes
        visited = seen.copy()
        visited.add( node.id )
    
        if node.endingNode:
            return True
    
        for sibling in node.siblings:
    
            ## If we've already visited this node, move on
            if sibling.id in visited:
                continue
    
            ## Otherwise, see if a traversal is found starting from here
            if cls.hasTraversal( sibling, visited ):
                return True
    
        return False

    @classmethod
    def checkForTraversal( cls, board ):

        ## Check for traversals from the top to the bottom        
        for node in cls.makeNodes( board ):
            if cls.hasTraversal( node, set() ):
                return True
    
        ## Transpose grid, check for traversals from the left to the right
        trans = zip( *board )

        for node in cls.makeNodes( trans ):
            if cls.hasTraversal( node, set() ):
                return True
    
        ## No traversals were found
        return False

## Class which defines a node
class Node:

    def __init__( self, nodeId, isEnd ):
        self.id = nodeId
        self.siblings = []
        self.endingNode = isEnd

