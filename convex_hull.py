from Tangent import Tangent
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

from Hull import Hull



import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False
		
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)
		
	def eraseHull(self,polygon):
		self.view.clearLines(polygon)
		
	def showText(self,text):
		self.view.displayStatusText(text)

	#Total Time Complexity: O(n) as it does O(n) operations where n is the size of the pts
	# in the left hull and the right hull about 4 times.
	#Total Space Complexity: O(P) where P is the number of points in the result hull
	def merge(self, leftHull, rightHull):
		resultHull = Hull([])
		#calls upper and lower Tangents to give us the right and left pts of the left and right hulls.
		#O(2n) to find both upper and lower tangent
		upLeftPtIndex, upRightPtIndex = Tangent.findUpper(self, leftHull, rightHull, leftHull.rightMostPointIndex, rightHull.leftMostPointIndex)
		lowLeftPtIndex, lowRightPtIndex = Tangent.findLower(self, leftHull, rightHull, leftHull.rightMostPointIndex, rightHull.leftMostPointIndex)
		#curr Index keeps track of the index spot in the result Hull
		currIndex = 0
		currLeftHullIndex = upLeftPtIndex
		resultHull.leftMostPointIndex = 0
		#while loop will add points to the result hull until we reach the left point of the lower tangent
		# will run potentially a total of O(L) times which is the amount of points in the left hull
		while currLeftHullIndex != lowLeftPtIndex:
			#adds points to result hull and increments the indeces
			resultHull.listOfPoints.append(leftHull.listOfPoints[currLeftHullIndex])
			currIndex = currIndex + 1
			currLeftHullIndex = leftHull.moveCounterClockwise(currLeftHullIndex)
			#if statement will make sure to keep the result's hull left most point accurate as new points are added
			if leftHull.listOfPoints[currLeftHullIndex].x() < resultHull.listOfPoints[resultHull.leftMostPointIndex].x():
				resultHull.leftMostPointIndex = currIndex
		resultHull.listOfPoints.append(leftHull.listOfPoints[lowLeftPtIndex])
		#Indeces & Hull updated so we are now looking at points in the right hull
		currIndex = currIndex + 1
		currRightHullIndex = lowRightPtIndex
		resultHull.rightMostPointIndex = currIndex
		# while loop will add points to the result hull until we reach the right point of the upper tangent
		# will run potentially a total of O(R) times where R is the amount of points in the right hull
		while currRightHullIndex != upRightPtIndex:
			# adds points to result hull and increments the indeces
			resultHull.listOfPoints.append(rightHull.listOfPoints[currRightHullIndex])
			currIndex = currIndex + 1
			currRightHullIndex = rightHull.moveCounterClockwise(currRightHullIndex)
			if rightHull.listOfPoints[currRightHullIndex].x() > resultHull.listOfPoints[resultHull.rightMostPointIndex].x():
				resultHull.rightMostPointIndex = currIndex
		resultHull.listOfPoints.append(rightHull.listOfPoints[upRightPtIndex])
		return resultHull

	#Total Time Complexity: O(nlogn) as merge is O(n) and we are doing it log(n)
	# times as the list of points is being cut in half every call
	#Total Space Complexity: O(n) due to us saving half the points in left and half the points in right
	def divideAndConquerHull (self, sortedHull):
		# Base case: Hull will only contain one point
		if len(sortedHull.listOfPoints) == 1:
			sortedHull.rightMostPointIndex = 0
			sortedHull.leftMostPointIndex = 0
			return sortedHull
		# leftHull will call divide and conquer recursively on the
		# sorted points until the left half of the given points
		leftHull = self.divideAndConquerHull(Hull(sortedHull.listOfPoints[0: int(len(sortedHull.listOfPoints) / 2)]))
		# rightHull will call divide and conquer recursively on the
		# sorted points starting at the second half of the given points
		rightHull = self.divideAndConquerHull(Hull(sortedHull.listOfPoints[int(len(sortedHull.listOfPoints)/2):]))
		#merge will combine left and right Hulls into one Hull
		return self.merge(leftHull, rightHull)


# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		points.sort(key=lambda p: p.x())
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		points = self.divideAndConquerHull(Hull(points)).listOfPoints
		polygon = [QLineF(points[i],points[(i+1)% len(points)]) for i in range(len(points))]

		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))



