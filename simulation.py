import pygame 
import math
from pygame import mixer

pygame.init()

WIDTH, HEIGHT = 800, 800

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation planetes") ##titre de la fenêtre


BLANC = (255, 255, 255)
JAUNE = (255, 255, 0)
BLEU = (100, 149, 237)
ROUGE = (188, 39, 50)
DARK_GREY = (80, 78, 81)




font = pygame.font.Font(None, 36)

class Planete:

    UA = 149.6e6 * 1000 ##Unité astronomique convertion en mètres
    G = 6.67428e-11 ##gravité
    ECHELLE = 250 / UA  ## 1UA = 100 pixels
    TEMPS = 3600*24 # echelle de temps 1 jour

    def __init__(self, x, y, radius, color, masse):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.masse = masse

        self.orbite = [] ##suivre tous les points parcourus par la planete
        self.soleil = False   ##ne pas tracer orbite du soleil
        self.distance_du_soleil = 0

        self.x_vitesse = 0
        self.y_vitesse = 0

    def draw(self, window): 
        x = self.x * self.ECHELLE + WIDTH / 2
        y = self.y * self.ECHELLE + HEIGHT / 2
       

        ##dessin des orbites
       ## création d'une liste de points qui seront toutes les coordonnées XY mis à l'échelle
        if len(self.orbite) > 2:
            updated_points = []
            for point in self.orbite:
                x, y = point 
                x = x* self.ECHELLE + WIDTH / 2 
                y = y * self.ECHELLE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(window, self.color, False, updated_points, 2) ##dessine des lignes entre tous les points

        pygame.draw.circle(window, self.color, (x,y), self.radius )


    def attraction(self, other):

        ##calcul de la distance entre les 2 objets
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        
        if other.soleil:  ##si l'objet est le soleil on sock la variable 
            self.distance_du_soleil = distance


        ##calcul de la force d'attraction
        force = self.G * self.masse * other.masse / distance ** 2   ##calcul de la force F = G* M*m/r², il faut décomposer cette force en x et y grâce à la trigonométrie
        teta = math.atan2(distance_y, distance_x) ## calcul de l'angle, il faut utiliser atan2 et pas atan parcequ'on prend le y sur le x et donner l'angle associé
        force_x = math.cos(teta) * force
        force_y = math.sin(teta) * force
        return force_x, force_y

    ##calcul de la force d'attraction entre les planetes et leurs vitesse
    def update_position(self, planetes):
        total_fx = total_fy = 0


        ##pour chaque planete on calcule la force x et force y exercée
        for planete in planetes:
            if self == planete:  ##si la planete est égale à elle meme continuer car on ne veut pas calculer la force avec elle même
                continue
            fx, fy = self.attraction(planete)
            total_fx += fx
            total_fy += fy

        ##calcul de la vitesse F = m / a  (masse divisée par l'accélération)
        self.x_vitesse += total_fx / self.masse * self.TEMPS      ## j'augmente ma vitesse par mon accélération multiplié par le temps (ici un jour)
        self.y_vitesse += total_fy / self.masse * self.TEMPS

        self.x += self.x_vitesse  * self.TEMPS
        self.y += self.y_vitesse * self.TEMPS   
        self.orbite.append((self.x, self.y))


def main():

    pygame.mixer.init()  # initialiser le lecteur
    
    pygame.mixer.music.load('/home/batou/Music/The_Sound_of_water.mp3')
    pygame.mixer.music.play(-1)  ##boucler la musique à l'infinie


    
    jours_compteur = 0
    last_second = pygame.time.get_ticks()


    run = True
    clock = pygame.time.Clock()

    soleil = Planete(0, 0, 30, JAUNE, 1.98892 * 10**30)
    soleil.soleil = True #pas besoin de dessiner d'orbite car c'est le soleil

    terre = Planete(-1*Planete.UA, 0, 16 ,BLEU, 5.9742 * 10**24)
    terre.y_vitesse = 29.783 * 1000 

    mars = Planete(-1.524 * Planete.UA, 0, 12, ROUGE, 6.39 * 10**23)
    mars.y_vitesse = 24.077 * 1000 

    mercure = Planete(0.387 * Planete.UA, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercure.y_vitesse = -47.4*1000

    venus = Planete(0.723 * Planete.UA, 0, 14, BLANC, 4.8685 * 10**24)
    venus.y_vitesse = -35.02 * 1000 

    planetes = [soleil, terre, mars, mercure, venus]

    while run:
        clock.tick(60) ##actualise 60 images par secondes
        WINDOW.fill((0,0,0)) ##ATTENTION  ! il faut absolument mettre un nouveau fond car il faut refresh en mettant un nouveau fond dessus à chaque fois sinon les planetes se dessinent les unes sur les autres

        for event in pygame.event.get():
            if event.type == pygame.QUIT:    ##si on clique sur fermer
                run = False


        for planete in planetes:
            planete.update_position(planetes)
            planete.draw(WINDOW)

        current_time = pygame.time.get_ticks()
        if current_time - last_second >= 10:  # 1000 milliseconds = 1 second
            # Increment day counter
            jours_compteur += 1
            last_second = current_time  # Update last_second
        day_text = font.render(f"Jours: {jours_compteur}", True, BLANC)
        WINDOW.blit(day_text, (10, 10))

        pygame.display.update() ##mettre à jour l'affichage

    pygame.quit()

 


main()