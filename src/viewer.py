import OpenGL

OpenGL.ERROR_CHECKING = True

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Viewer(object):
    def __init__(self, drawFunc, name="Contrasty Viewer"):
        super(Viewer, self).__init__()

        self.glutWindow = glutCreateWindow(name)
        self.window = self
        self.drawFunc = drawFunc

        glutReshapeWindow(800, 600)

        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)

        glutMainLoop()

    def reshape(self, width, height):
        glutSetWindow(self.glutWindow)

        if height == 0:
            height = 1

        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluOrtho2D(0, width, 0, height) #image size!

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def display(self):
        glutSetWindow(self.glutWindow)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.drawFunc()

        glutSwapBuffers()

glutInit("")
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH | GLUT_MULTISAMPLE)