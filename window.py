import pyglet
import color_to_RGB
import time
from pyglet.window import key

class Window():
    
    def __init__(self, particle_canvas, title='Particle Life', debug = False):
        # Particle canvas object
        self.particle_canvas = particle_canvas
        
        # Create window
        self.window_size = {'Width': particle_canvas.canvas_size['Width'], 'Height': particle_canvas.canvas_size['Height']}
        self.title = title
        self.window = pyglet.window.Window(self.window_size['Width'] + particle_canvas.UI_space, self.window_size['Height'], self.title)
        
        # Pyglet particle rendering
        self.batch = pyglet.graphics.Batch()
        self.vertex_list = self.createNewVertexList()

        # UI Shit
        self.space_between_labels = 14
        self.font_size = 10 
        self.selected_attraction_matrix_element = [0,0]
        self.first_bracket_space = 10
        self.bracket_space = 27
        self.ui_batch = pyglet.graphics.Batch()

        # All labels

        # Create FPS label
        self.fps_label = pyglet.text.Label("FPS: ",
                         font_size=self.font_size,
                         batch=self.ui_batch,
                         x=2, y=self.window.height  - self.space_between_labels)
        
        
        # Create number of particles label
        self.particle_count_label = pyglet.text.Label("Particles: " + str(len(self.particle_canvas.particles)),
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.fps_label.y - (self.space_between_labels*3))
        # Create label how to adjust number of particles
        self.adjust_particle_count_label = pyglet.text.Label("Q/A to increase/decrease",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.particle_count_label.y - self.space_between_labels)
        
        # Create number of colors label
        self.number_of_colors_label = pyglet.text.Label("Number of colors: " + str(self.particle_canvas.number_of_colors),
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_particle_count_label.y - (self.space_between_labels*2))
        # Create label how to adjust number of colors
        self.adjust_number_of_colors_label = pyglet.text.Label("W/S to increase/decrease",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.number_of_colors_label.y - self.space_between_labels)
        
        # Create attraction matrix label
        self.attraction_matrix_label = pyglet.text.Label("Attraction matrix: random fun",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_number_of_colors_label.y - (self.space_between_labels*2))
        # Create label how to adjust attraction matrix
        self.adjust_attraction_matrix_label = pyglet.text.Label("1-6 to change matrix",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.attraction_matrix_label.y - self.space_between_labels)
        # Create label how to adjust attraction matrix
        self.adjust_attraction_matrix_label2 = pyglet.text.Label("0 for random matrix",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_attraction_matrix_label.y - self.space_between_labels)

        # Create attraction matrix label
        self.adjust_attraction_matrix_label3 = pyglet.text.Label("Manually adjust attraction matrix",
                        font_size=self.font_size-1,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_attraction_matrix_label2.y - (self.space_between_labels*2))
        
        # Create label how to adjust attraction matrix
        self.adjust_attraction_matrix_label4 = pyglet.text.Label("Arrow keys to move",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_attraction_matrix_label3.y - self.space_between_labels)
        
        # Create 2nd label how to adjust attraction matrix
        self.adjust_attraction_matrix_label5 = pyglet.text.Label("+/- to increase/decrease",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_attraction_matrix_label4.y - self.space_between_labels)

        # Example of matrix to show how it works
        
        #  |  R |  O |  Y |  G |  B |  P
        # R| 0.3|-0.5|-0.3| 0.3| 0.5| 0.3
        # O|-0.5| 0.3|-0.5|-0.3|-0.5|-0.3
        # Y|-0.3|-0.5| 0.3|-0.5|-0.3|-0.5
        # G| 0.3|-0.3|-0.5| 0.3|-0.5|-0.3
        # B| 0.5|-0.5|-0.3|-0.5| 0.3|-0.5
        # P| 0.3|-0.3|-0.5|-0.3|-0.5| 0.3

        # Create color row 
        self.color_row  = self.create_matrix_label_color("R", x=2 + self.bracket_space * 1 - 5, y=self.adjust_attraction_matrix_label5.y - self.space_between_labels*2)
        self.color_row2 = self.create_matrix_label_color("O", x=2 + self.bracket_space * 2 - 5, y=self.color_row.y)
        self.color_row3 = self.create_matrix_label_color("Y", x=2 + self.bracket_space * 3 - 5, y=self.color_row.y)
        self.color_row4 = self.create_matrix_label_color("G", x=2 + self.bracket_space * 4 - 5, y=self.color_row.y)
        self.color_row5 = self.create_matrix_label_color("B", x=2 + self.bracket_space * 5 - 5, y=self.color_row.y)
        self.color_row6 = self.create_matrix_label_color("P", x=2 + self.bracket_space * 6 - 5, y=self.color_row.y)

        # Create other rows
        self.row1_color = self.create_matrix_label_color("R", x=2, y=self.color_row.y - self.space_between_labels)
        self.row2_color = self.create_matrix_label_color("O", x=2, y=self.row1_color.y - self.space_between_labels)
        self.row3_color = self.create_matrix_label_color("Y", x=2, y=self.row2_color.y - self.space_between_labels)
        self.row4_color = self.create_matrix_label_color("G", x=2, y=self.row3_color.y - self.space_between_labels)
        self.row5_color = self.create_matrix_label_color("B", x=2, y=self.row4_color.y - self.space_between_labels)
        self.row6_color = self.create_matrix_label_color("P", x=2, y=self.row5_color.y - self.space_between_labels)
        
        # Create brackets 
        for i in range(7):
            if i == 0:
                for j in range(7):
                    self.create_matrix_label_bracket(x=2 + self.first_bracket_space, y=self.color_row.y - self.space_between_labels * j)
            else:
                for j in range(7):
                    self.create_matrix_label_bracket(x=2 + self.first_bracket_space + self.bracket_space * i, y=self.color_row.y - self.space_between_labels * j)

        # Create matrix elements
        self.element_labels = []
        for i in range(6):
            element_row = []
            for j in range(6):
                element_row.append(self.create_matrix_label_element(i, j, x=2 + self.first_bracket_space + self.bracket_space * j + 15, y=self.row1_color.y - self.space_between_labels * i))
                if i == self.selected_attraction_matrix_element[0] and j == self.selected_attraction_matrix_element[1]:
                    element_row[j].color = (255, 0, 0, 255)
            self.element_labels.append(element_row)



        # Create dt label
        self.dt_label = pyglet.text.Label("Time dt: " + str(round(self.particle_canvas.engine.dt, 3)), 
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.row6_color.y - (self.space_between_labels*3))
        # Create label how to adjust dt
        self.adjust_dt_label = pyglet.text.Label("E/D to increase/decrease",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.dt_label.y - self.space_between_labels)
        
        # Create rMax label
        self.rMax_label = pyglet.text.Label("rMax: " + str(self.particle_canvas.engine.rMax), 
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_dt_label.y - (self.space_between_labels*2))
        # Create label how to adjust rMax
        self.adjust_rMax_label = pyglet.text.Label("R/F to increase/decrease",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.rMax_label.y - self.space_between_labels)
        
        # Create forceFactor label
        self.forceFactor_label = pyglet.text.Label("ForceFactor: " + str(self.particle_canvas.engine.forceFactor),
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_rMax_label.y - (self.space_between_labels*2))
                        
        # Create label how to adjust forceFactor
        self.adjust_forceFactor_label = pyglet.text.Label("T/G to increase/decrease",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.forceFactor_label.y - self.space_between_labels)
        
        # Create frictionHalfLife label
        self.frictionHalfLife_label = pyglet.text.Label("FrictionHalfLife: " + str(self.particle_canvas.engine.frictionHalfLife),
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_forceFactor_label.y - (self.space_between_labels*2))
        # Create label how to adjust frictionHalfLife
        self.adjust_frictionHalfLife_label = pyglet.text.Label("Y/H to increase/decrease",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.frictionHalfLife_label.y - self.space_between_labels)
        
        # Create frictionFactor label
        self.frictionFactor_label = pyglet.text.Label("FrictionFactor: " + str(round(self.particle_canvas.engine.frictionFactor, 3)),
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_frictionHalfLife_label.y - (self.space_between_labels*2))
        # Create label how to adjust frictionFactor
        self.adjust_frictionFactor_label = pyglet.text.Label("Changes automatically ",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.frictionFactor_label.y - self.space_between_labels)
        # Create 2nd label how to adjust frictionFactor
        self.adjust_frictionFactor_label2 = pyglet.text.Label("based on frictionHalfLife",
                        font_size=self.font_size,
                        batch=self.ui_batch,
                        x=2, y=self.adjust_frictionFactor_label.y - self.space_between_labels)

        
        @self.window.event
        def on_key_press(symbol, modifiers):
            
            # change particle count on key press
            if symbol == key.Q:
                if self.particle_canvas.total_particles < 100000 and self.particle_canvas.total_particles >= 1000:
                    self.particle_canvas.total_particles += 1000
                elif self.particle_canvas.total_particles < 1000 and self.particle_canvas.total_particles >= 100:
                    self.particle_canvas.total_particles += 100
                elif self.particle_canvas.total_particles < 100 and self.particle_canvas.total_particles >= 10:
                    self.particle_canvas.total_particles += 10
                elif self.particle_canvas.total_particles < 10 and self.particle_canvas.total_particles >= 1:
                    self.particle_canvas.total_particles += 1
                self.particle_canvas.updateParticleNumber()
                # Clear old batch and create new vertex list and add it to batch
                self.batch = pyglet.graphics.Batch()
                self.vertex_list = self.createNewVertexList()
            elif symbol == key.A:
                if self.particle_canvas.total_particles > 1000:
                    self.particle_canvas.total_particles -= 1000
                elif self.particle_canvas.total_particles > 100:
                    self.particle_canvas.total_particles -= 100
                elif self.particle_canvas.total_particles > 10:
                    self.particle_canvas.total_particles -= 10
                elif self.particle_canvas.total_particles > 1:
                    self.particle_canvas.total_particles -= 1
                self.particle_canvas.updateParticleNumber()
                # Clear old batch and create new vertex list and add it to batch
                self.batch = pyglet.graphics.Batch()
                self.vertex_list = self.createNewVertexList()
            
            # change number of colors on key press
            elif symbol == key.W:
                if self.particle_canvas.number_of_colors < len(self.particle_canvas.particle_colors):
                    self.particle_canvas.number_of_colors += 1
                    self.particle_canvas.updateParticleColors()
                    # Clear old batch and create new vertex list and add it to batch
                    self.batch = pyglet.graphics.Batch()
                    self.vertex_list = self.createNewVertexList()
            elif symbol == key.S:
                if self.particle_canvas.number_of_colors > 1:
                    self.particle_canvas.number_of_colors -= 1
                    self.particle_canvas.updateParticleColors()
                    # Clear old batch and create new vertex list and add it to batch
                    self.batch = pyglet.graphics.Batch()
                    self.vertex_list = self.createNewVertexList()

            # change dt on key press
            elif symbol == key.E:
                self.particle_canvas.engine.dt += 0.001
            elif symbol == key.D:
                self.particle_canvas.engine.dt -= 0.001

            # change rMax on key press
            elif symbol == key.R:
                self.particle_canvas.engine.rMax += 5
            elif symbol == key.F:
                if self.particle_canvas.engine.rMax > 5:
                    self.particle_canvas.engine.rMax -= 5

            # change forceFactor on key press
            elif symbol == key.T:
                self.particle_canvas.engine.forceFactor += 0.1
            elif symbol == key.G:
                self.particle_canvas.engine.forceFactor -= 0.1

            # change frictionHalfLife on key press
            elif symbol == key.Y:
                self.particle_canvas.engine.frictionHalfLife += 0.01
                self.particle_canvas.engine.frictionHalfLife = round(self.particle_canvas.engine.frictionHalfLife, 2)
            elif symbol == key.H:
                self.particle_canvas.engine.frictionHalfLife -= 0.01
                self.particle_canvas.engine.frictionHalfLife = round(self.particle_canvas.engine.frictionHalfLife, 2)

        
            # change attraction matrix on key press
            elif symbol == key._1:
                self.particle_canvas.updateMatrix(1)
                self.attraction_matrix_label.text = "Attraction matrix: snakes"
                self.particle_canvas.engine.frictionHalfLife = 0.01
                self.particle_canvas.engine.calculateFrictionFactor()
                self.particle_canvas.forceFactor = 0.1
                self.particle_canvas.engine.rMax = 50
                self.particle_canvas.engine.dt = 0.002

            elif symbol == key._2:
                self.particle_canvas.updateMatrix(2)
                self.attraction_matrix_label.text = "Attraction matrix: random fun"
            elif symbol == key._3:
                self.particle_canvas.updateMatrix(3)
                self.attraction_matrix_label.text = "Attraction matrix: chains 1"
            elif symbol == key._4:
                self.particle_canvas.updateMatrix(4)
                self.attraction_matrix_label.text = "Attraction matrix: chains 2"
            elif symbol == key._5:
                self.particle_canvas.updateMatrix(5)
                self.attraction_matrix_label.text = "Attraction matrix: chains 3"
            elif symbol == key._6:
                self.particle_canvas.updateMatrix(6)
                self.attraction_matrix_label.text = "Attraction matrix:rand symmetry"
            elif symbol == key._0:
                self.particle_canvas.updateMatrix(0)
                self.attraction_matrix_label.text = "Attraction matrix: random"


            # change selected element in attraction matrix
            elif symbol == key.UP:
                if self.selected_attraction_matrix_element[0] > 0:
                    self.selected_attraction_matrix_element[0] -= 1
            elif symbol == key.DOWN:
                if self.selected_attraction_matrix_element[0] < 5:
                    self.selected_attraction_matrix_element[0] += 1
            elif symbol == key.LEFT:
                if self.selected_attraction_matrix_element[1] > 0:
                    self.selected_attraction_matrix_element[1] -= 1
            elif symbol == key.RIGHT:
                if self.selected_attraction_matrix_element[1] < 5:
                    self.selected_attraction_matrix_element[1] += 1

            # change value of selected element in attraction matrix. move up by 0.1 if equals is pressed. move down by 0.1 if minus is pressed
            elif symbol == key.EQUAL:
                if self.particle_canvas.attraction_matrix[self.selected_attraction_matrix_element[0]][self.selected_attraction_matrix_element[1]] < 1:
                    self.particle_canvas.attraction_matrix[self.selected_attraction_matrix_element[0]][self.selected_attraction_matrix_element[1]] += 0.1
                    self.particle_canvas.attraction_matrix[self.selected_attraction_matrix_element[0]][self.selected_attraction_matrix_element[1]] = round(self.particle_canvas.attraction_matrix[self.selected_attraction_matrix_element[0]][self.selected_attraction_matrix_element[1]], 1)
            elif symbol == key.MINUS:
                if self.particle_canvas.attraction_matrix[self.selected_attraction_matrix_element[0]][self.selected_attraction_matrix_element[1]] > -1:
                    self.particle_canvas.attraction_matrix[self.selected_attraction_matrix_element[0]][self.selected_attraction_matrix_element[1]] -= 0.1
                    self.particle_canvas.attraction_matrix[self.selected_attraction_matrix_element[0]][self.selected_attraction_matrix_element[1]] = round(self.particle_canvas.attraction_matrix[self.selected_attraction_matrix_element[0]][self.selected_attraction_matrix_element[1]], 1)




        self.debug = debug
    
    def update(self):
        """ Update window """
        if(self.debug):
            begin = time.time_ns()  / (10 ** 9)
        
        self.window.clear()
        
        # Particles
        self.updateObjectPositions()
        self.batch.draw()

        if(self.debug):
            particle_time = time.time_ns()  / (10 ** 9)
            print("2. Draw particles:\t\t\t\t" + str(particle_time - begin) + " seconds")

        # UI
        self.updateLabelText()
        self.ui_batch.draw()

        if(self.debug):
            print("3. Draw UI:\t\t\t\t\t" + str(time.time_ns()  / (10 ** 9) - particle_time) + " seconds")

    def create_matrix_label_color(self, color, x, y):
            return pyglet.text.Label(color,
                        font_size=self.font_size-1,
                        batch=self.ui_batch,
                        x=x, y=y)


    def create_matrix_label_bracket(self, x, y):
        return pyglet.text.Label("|",
                    font_size=self.font_size-1,
                    batch=self.ui_batch,
                    x=x, y=y)


    def create_matrix_label_element(self, matrix_row_number, matrix_column_number, x, y):
        element = str(self.particle_canvas.attraction_matrix[matrix_row_number][matrix_column_number])
        return pyglet.text.Label(element,
                    font_size=self.font_size-1,
                    batch=self.ui_batch,
                    x=x, y=y,
                    anchor_x='center')


    def updateLabelText(self):
        self.particle_count_label.text = "Particles: " + str(len(self.particle_canvas.particles))
        self.number_of_colors_label.text = "Number of colors: " + str(self.particle_canvas.number_of_colors)
        self.dt_label.text = "Time dt: " + str(round(self.particle_canvas.engine.dt, 3))
        self.rMax_label.text = "rMax: " + str(self.particle_canvas.engine.rMax)
        self.forceFactor_label.text = "ForceFactor: " + str(round(self.particle_canvas.engine.forceFactor, 3))
        self.frictionHalfLife_label.text = "FrictionHalfLife: " + str(round(self.particle_canvas.engine.frictionHalfLife, 3))
        self.particle_canvas.engine.calculateFrictionFactor()
        self.frictionFactor_label.text = "FrictionFactor: " + str(round(self.particle_canvas.engine.frictionFactor, 3))
        for i in range(6):
            for j in range(6):
                if i == self.selected_attraction_matrix_element[0] and j == self.selected_attraction_matrix_element[1]:
                    self.element_labels[i][j].color = (255, 0, 0, 255)
                else:
                    self.element_labels[i][j].color = (255, 255, 255, 255)
                self.element_labels[i][j].text = str(self.particle_canvas.attraction_matrix[i][j])
        

    def createNewVertexList(self):
        vertices, colors = self.updateVertexList()
        return self.batch.add(len(self.particle_canvas.particles) * 4, pyglet.gl.GL_QUADS, None,
                                                       ('v2f', vertices),
                                                       ('c3B', colors),) 

    def updateVertexList(self, color=True):
        """ Create vertex list for particles. 
        Option to also create color list """	
        vertices = []
        colors = []
        for prtcl in self.particle_canvas.particles:
            vertices.extend([prtcl.posX                                     , prtcl.posY                                    ,
                             prtcl.posX                                     , prtcl.posY +self.particle_canvas.particle_size,
                             prtcl.posX +self.particle_canvas.particle_size , prtcl.posY +self.particle_canvas.particle_size,
                             prtcl.posX +self.particle_canvas.particle_size , prtcl.posY                                    ])
            if(color):
                colors.extend(color_to_RGB.transform(prtcl.color) * 4)
        
        if(color):
            return vertices, colors
        else:
            return vertices

    def updateFPS(self, fps):
        """ Update FPS label """	
        self.fps_label.text = "FPS: " + str(fps)

    def updateObjectPositions(self):	
        """ Update vertex list for particles """
        self.vertex_list.vertices = self.updateVertexList(color=False)