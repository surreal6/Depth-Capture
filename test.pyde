def setup():
	size(200, 200, P3D)
	
def draw():
	rotateX(-.5)
	rotateY(-.5)
	background(0)
	fill(255,0,0)
	box(30)
	pushMatrix()
	translate(0,0,20)
	fill(0,0,255)
	box(5)
	popMatrix()