class Hull:
    def __init__(self, listOfPoints, rightMostPoint = 0, leftMostPoint = 0):
        self.listOfPoints = listOfPoints
        self.rightMostPointIndex = rightMostPoint
        self.leftMostPointIndex = leftMostPoint

    def setRightMostPointIndex(self, rightMostPtIndex):
        self.rightMostPointIndex = rightMostPtIndex

    def setLeftMostPointIndex(self, leftMostPtIndex):
        self.leftMostPointIndex = leftMostPtIndex

    #will take a pt index and will give the next in the list unless it is the last element,
    # in which case it will return the first element
    #Total Time Complexity: O(1) & Total Space Complexity: O(1)
    def moveCounterClockwise(self, startPtIndex):
        if len(self.listOfPoints) != (startPtIndex + 1): #TC: O(1) SC: O(1)
            return startPtIndex + 1 #TC: O(1) SC: O(1)
        return 0 #TC: O(1) SC: O(1)

    # will take a pt index and give the previous pt in the list unless it is the first pt,
    # then it will give the last point
    # Total Time Complexity: O(1) & Total Space Complexity: O(1)
    def moveClockwise(self, startPtIndex):
        if startPtIndex != 0: #TC: O(1) SC: O(1)
            return startPtIndex - 1 #TC: O(1) SC: O(1)
        return len(self.listOfPoints) - 1 #TC: O(1) SC: O(1)
