class Tangent:
    def __init__(self, leftHull, rightHull):
        self.leftHull = leftHull
        self.rightHull = rightHull

    #Total Time Complexity: O(1) even though we are dividing,
    # it will be lower because the length of the input isn't growing
    #Total Space Complexity: O(1)
    def findSlope(self, pt1, pt2):
        #returns the slope of two given points
        return (pt2.y() - pt1.y()) / (pt2.x() - pt1.x())

    #finds upper tangent given two hulls and the right most pt of the left hull and left most point of the right hull
    #Total Time Complexity: O(n) Total Space Complexity: O(1)
    def findUpper(self, leftHull, rightHull, rightMostPtIndexL, leftMostPointIndexR):
        #sets curr index for left and right hull to the right most and left most pts respectively
        currLeftPtIndex = rightMostPtIndexL
        currRightPtIndex = leftMostPointIndexR
        done = 0
        #sets the points that will be after the first points for left and right hulls
        newPt = leftHull.moveCounterClockwise(currLeftPtIndex)
        newPtR = rightHull.moveClockwise(currRightPtIndex)
        #while loop will make sure slopes are checked until we have the upper most tangent
        #TC: O(n) where n is the number of pts in the left and right hulls SC: O(1) as we have about 7 different
        # variables that we are keeping track of so this is just O(1)
        while done == 0:
            done = 1
            #find initial slope and next slope so we can compare the two
            slope = Tangent.findSlope(self, leftHull.listOfPoints[currLeftPtIndex], rightHull.listOfPoints[currRightPtIndex])
            nextSlope = Tangent.findSlope(self, leftHull.listOfPoints[newPt], rightHull.listOfPoints[currRightPtIndex])
            #will continually move left hull point counterclockwise and test the slope stops once we have a next
            #slope that isn't decreasing as much as the previous one
            while slope > nextSlope:
                #moves curr pt in the left hull and updates slope and next slope
                currLeftPtIndex = leftHull.moveCounterClockwise(currLeftPtIndex)
                slope = nextSlope
                newPt = leftHull.moveCounterClockwise(currLeftPtIndex)
                nextSlope = Tangent.findSlope(self, leftHull.listOfPoints[newPt],
                                               rightHull.listOfPoints[currRightPtIndex])
                done = 0
            nextSlopeR = Tangent.findSlope(self, leftHull.listOfPoints[currLeftPtIndex], rightHull.listOfPoints[newPtR])
            # will continually move right hull point clockwise and test the slope. Stops once we have a next
            # slope that isn't as increasing as the previous one
            while slope < nextSlopeR:
                # moves curr pt in the right hull and updates slope and next slope
                currRightPtIndex = rightHull.moveClockwise(currRightPtIndex)
                slope = nextSlopeR
                newPtR = rightHull.moveClockwise(currRightPtIndex)
                nextSlopeR = Tangent.findSlope(self, leftHull.listOfPoints[currLeftPtIndex], rightHull.listOfPoints[newPtR])
                done = 0
        return currLeftPtIndex, currRightPtIndex

    # finds lower tangent given two hulls and the right most pt of the left hull and left most point of the right hull
    # Total Time Complexity: O(n) Total Space Complexity: O(1)
    def findLower(self, leftHull, rightHull, rightMostPtIndexL, leftMostPointIndexR):
        # sets curr index for left and right hull to the right most and left most pts respectively
        currLeftPtIndex = rightMostPtIndexL
        currRightPtIndex = leftMostPointIndexR
        done = 0
        newPt = leftHull.moveClockwise(currLeftPtIndex)
        newPtR = rightHull.moveCounterClockwise(currRightPtIndex)
        # while loop will make sure slopes are checked until we have the lower most tangent
        #TC: O(n) where n is the number of pts in the left and right hulls SC: O(1) as we have about 7 different
        # variables that we are keeping track of so this is just O(1)
        while done == 0:
            done = 1
            # find initial slope and next slope so we can compare the two
            slope = Tangent.findSlope(self, leftHull.listOfPoints[currLeftPtIndex], rightHull.listOfPoints[currRightPtIndex])
            nextSlope = Tangent.findSlope(self, leftHull.listOfPoints[newPt], rightHull.listOfPoints[currRightPtIndex])
            # will continually move left hull point clockwise and test the slope stops once we have a next
            # slope that isn't increasing as much as the previous one
            while slope < nextSlope:
                # moves curr pt in the left hull and updates slope and next slope
                currLeftPtIndex = leftHull.moveClockwise(currLeftPtIndex)
                slope = nextSlope
                newPt = leftHull.moveClockwise(currLeftPtIndex)
                nextSlope = Tangent.findSlope(self, leftHull.listOfPoints[newPt], rightHull.listOfPoints[currRightPtIndex])
                done = 0
            nextSlopeR = Tangent.findSlope(self, leftHull.listOfPoints[currLeftPtIndex],
                                               rightHull.listOfPoints[newPtR])
            # will continually move right hull point counterclockwise and test the slope. Stops once we have a next
            # slope that isn't decreasing more than the previous one
            while slope > nextSlopeR:
                # moves curr pt in the right hull and updates slope and next slope
                currRightPtIndex = rightHull.moveCounterClockwise(currRightPtIndex)
                slope = nextSlopeR
                newPtR = rightHull.moveCounterClockwise(currRightPtIndex)
                nextSlopeR = Tangent.findSlope(self, leftHull.listOfPoints[currLeftPtIndex], rightHull.listOfPoints[newPtR])
                done = 0
        return currLeftPtIndex, currRightPtIndex
