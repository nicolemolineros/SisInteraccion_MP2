from openal import oalOpen, Listener, Source, WaveFile, oalQuit
from time import sleep
import random
import time

class Player:
    def __init__(self, name, health=15, attack=2):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.inventory = []

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

def play_sound(filename, lado=0):
    """Reproduce un archivo de sonido.
        lado = 1 -> derecha
        lado = 0 -> centro
        lado = -1 -> izquierda
    """	
    source = oalOpen("audio.wav")
    if source is None:
        print("Failed to load audio file.")
        oalQuit()
        exit(1)
    source.set_position([0, 0, 0])
    source.play()
    listener = Listener()
    listener.set_position([0, 0, 0])
    try:
        source.set_position([lado, 0, 0])
        sleep(1)
    finally:
        source.stop()
        

def witch_sound():
    play_sound("sound_effects/witchdeath.wav")

def goblin_sound():
    play_sound("sound_effects/goblinattack.wav") 

def dragon_sound():
    play_sound("sound_effects/dragon_sound.wav") 

def monster_sound():
    play_sound("sound_effects/monster.wav") 

def victory_sound():
    play_sound("sound_effects/victory.wav") 

def defeat_sound():
    play_sound("sound_effects/defeat.wav") 

def restore_sound():
    play_sound("sound_effects/recover.wav") 

def attack_sound(): 
    play_sound("sound_effects/attack.wav") 

def failed_attack_sound(): 
    play_sound("sound_effects/failattack.wav")

def dragon_attack_sound(): 
    play_sound("sound_effects/dragonattack.wav")

def witch_attack_sound(): 
    play_sound("sound_effects/witchattack.wav")

def goblin_attack_sound():
    play_sound("sound_effects/goblindeath.wav") 

def potion_sound():
    play_sound("sound_effects/potion.wav") 

def help_sound():
    play_sound("sound_effects/help.wav", 1,0,0) 

def bells_sound():
    play_sound("sound_effects/bells.wav") 

def laugh_sound():
    play_sound("sound_effects/laugh.wav", 0,0,-1)

def print_status(player, enemy):
    print(f"\nTu vida: {player.health}")
    print(f"Vida de {enemy.name}: {enemy.health}")

def combat(player : Player, enemy):
    print(f"\n¡Te encuentras con un {enemy.name}!")
    
    while player.health > 0 and enemy.health > 0:
        print_status(player, enemy)
        print("\nOpciones:")
        print("1. Atacar")
        print("2. Curar")
        
        choice = input("Elige una opción: ")
        
        if choice == '1':
            if random.random() < 0.8:  # 80% de probabilidad de éxito
                damage = player.attack
                enemy.health -= damage
                print(f"¡Atacas al {enemy.name} y le haces {damage} de daño!")
                attack_sound()
            else:
                print("Fallas el ataque.")
                failed_attack_sound()
        elif choice == '2':
            heal = random.randint(0, player.max_health//6)
            player.health = min(player.health + heal, player.max_health)
            print(f"Te curas {heal} puntos de vida.")
            restore_sound()
        else:
            print("Opción no válida. Pierdes tu turno.")
        
        if enemy.health <= 0:
            print(f"¡Has derrotado al {enemy.name}!")
            if enemy.name == "Monstruo Terrible":
                monster_sound()
            elif enemy.name == "Goblin":
                goblin_sound()
            elif enemy.name == "Bruja":
                witch_sound()
            elif enemy.name == "Dragón Feroz":
                dragon_sound()
            victory_sound()
            return "victory"
        
        # Turno del enemigo
        enemy_damage = random.randint(1, enemy.attack)
        player.health -= enemy_damage
        print(f"El {enemy.name} te ataca y te hace {enemy_damage} de daño.")
        if enemy.name == "Dragón Feroz":
            dragon_attack_sound()
        elif enemy.name == "Bruja":
            witch_attack_sound()
        elif enemy.name == "Goblin":
            goblin_attack_sound()
    
    if player.health <= 0:
        print("Has sido derrotado...")
        defeat_sound()
        return "defeat"

def inicio(player : Player):
    print("\n--- ACTO I: EL INICIO ---")
    print("Te adentras en la oscura mansión en busca de la princesa.")
    print("Un terrible monstruo aparece ante ti.")
    
    enemigo_fuerte = Enemy("Monstruo Terrible", 15, 3)
    resultado = combat(player, enemigo_fuerte)
    
    if resultado == "defeat":
        print("El monstruo te ha derrotado, pero no todo está perdido...")
        print("Despiertas en una celda, herido pero vivo.")
        restore_sound()
        player.health = player.max_health // 2  # Recuperas la mitad de tu salud
        return True
    else:
        print("Has logrado escapar por poco. Necesitas hacerte más fuerte.")
        return True

def nudo_1(player : Player):
    print("\n--- ACTO II: EL NUDO PARTE 1 ---")
    print("Te adentras más en la mansión, determinado a rescatar a la princesa.")
    
    enemigo_debil = Enemy("Goblin", 6, 1)
    resultado = combat(player, enemigo_debil)
    
    if resultado == "victory":
        print("Has derrotado al goblin. En su bolsa encuentras una llave.")
        print("La llave abre un cofre cercano. ¡Dentro hay una espada mágica!")
        player.attack = random.randint(3, 5)
        print(f"Tu ataque ha aumentado a {player.attack}.")
        restore_sound()
        return True
    else:
        print("Has sido derrotado por el goblin. Tu aventura termina aquí.")
        defeat_sound()
        return False

def nudo_2(player : Player):
    print("\n--- ACTO II: EL NUDO PARTE 2 ---")
    print("Despues de matar al goblin, encuentras una habitacion. Entras y hay una bruja")
    laugh_sound()

    enemigo_debil = Enemy("Bruja", 10, 1)
    resultado = combat(player, enemigo_debil)
    
    if resultado == "victory":
        print("Has derrotado a la bruja. En su estante encuentras una pocion.")
        witch_sound()
        print("Te tomas la pocion y recuperas todos tus puntos de vida.")
        potion_sound()
        player.health = player.max_health
        print(f"Tu vida ha aumentado a {player.health}.")
        restore_sound()
        return True
    else:
        print("Has sido derrotado por la bruja. Tu aventura termina aquí.")
        defeat_sound()
        return False

def desenlace_1(player : Player):
    print("\n--- ACTO III: EL DESENLACE PARTE 1---")
    print("Llegas a la cámara final. Un enorme dragón custodia a la princesa.")
    
    dragon = Enemy("Dragón Feroz", 27, 3)
    resultado = combat(player, dragon)
    
    if resultado == "victory":
        print("¡Has derrotado al dragón y rescatado a la princesa!")
        print("Felicidades, has completado tu misión.")
        victory_sound()
        return True
    else:
        print("El dragón era demasiado poderoso. Tu aventura termina aquí.")
        defeat_sound()
        return False
    
def desenlace_2():
    print("\n--- ACTO III: EL DESENLACE PARTE 2---")
    print("Escuchas a la princesa gritar a tu derecha. Corres hacia ella")
    help_sound()

    print("La princesa te pide que la liberes de sus cadenas")
    print("Con tu espada, cortas las cadenas de la princesa")
    print("La princesa te da las gracias y te da un beso en la mejilla")

    print("La princesa te dice que te llevara a su reino y te dara una recompensa")

    print("La princesa te lleva a su reino y te da una recompensa")
    print("La recompensa es casarte con ella y ser el rey de su reino")
    bells_sound()
    
    return True

def main_game_loop():
    nombre = input("Ingresa el nombre de tu héroe: ")
    player = Player(nombre, health=15, attack=2)
    print(f"Bienvenido, {player.name}. Tu misión es rescatar a la princesa de que se encuentra encerrada hace quince años en una mansión abandonada llena de monstruos y criaturas.")
    if inicio(player):
        if nudo_1(player):
            if nudo_2(player):
                if desenlace_1(player):
                    desenlace_2()
                    print("¡Has completado el juego! Eres un verdadero héroe.")
                    victory_sound()

    print(f"Gracias por jugar {player.name}.")
    oalQuit()
if __name__ == "__main__":
    main_game_loop()