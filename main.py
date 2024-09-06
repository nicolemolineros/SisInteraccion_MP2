from openal import oalOpen, oalQuit
from time import sleep
import random
import os
from colorama import init, Fore, Style

init(autoreset=True) # Colorama initialization 

class Player:
    def __init__(self, name, health=17, attack=2): 
        #By default, the player has 17 points of life and 2 points to attack
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

def play_sound(filename, side=0):
    # if side is 0, audio is centered, 
    # if side is -1, audio is to the left,
    # if side is 1, audio is to the right
    source = oalOpen(filename)
    if source is None:
        print("Failed to load audio file.")
        oalQuit()
        exit(1)
    source.play()
    try:
        source.set_position([side, 0, 0])
        sleep(1)
    finally:
        source.stop()

def print_colored(text, color=Fore.WHITE, bold=False):
    # Specific text color
    if bold:
        print(f"{color}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    else:
        print(f"{color}{text}{Style.RESET_ALL}")
    

def print_separator(char='*', length=50):
    print(char * length)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def witch_sound():
    play_sound("sound_effects/witchdeath.wav")

def goblin_sound():
    play_sound("sound_effects/goblinattack.wav") 

def dragon_sound():
    play_sound("sound_effects/dragon_sound.wav",1) 

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
    play_sound("sound_effects/potion.wav",-1) 

def help_sound():
    play_sound("sound_effects/help.wav", 1) 

def bells_sound():
    play_sound("sound_effects/bells.wav") 

def laugh_sound():
    play_sound("sound_effects/laugh.wav", -1)

def print_status(player, enemy):
    print_colored(f"\nTu vida: {player.health}", Fore.GREEN)
    print_colored(f"Vida de {enemy.name}: {enemy.health}", Fore.RED)

def combat(player : Player, enemy):
    print_colored(f"\n¡Te encuentras con un {enemy.name}!", Fore.YELLOW, bold=True)
    
    while player.health > 0 and enemy.health > 0:
        print_status(player, enemy)
        print_colored("\nOpciones:", Fore.CYAN)
        print_colored("1. Atacar", Fore.CYAN)
        print_colored("2. Curar", Fore.CYAN)
        
        choice = input("Elige una opción: ")
        
        if choice == '1':
            if random.random() < 0.8:  # 80% of hitting the enemy
                damage = player.attack
                enemy.health -= damage
                print_colored(f"¡Atacas al {enemy.name} y le haces {damage} de daño!", Fore.GREEN)
                attack_sound()
            else:
                print_colored("Fallas el ataque.", Fore.RED)
                failed_attack_sound()
        elif choice == '2':
            heal = random.randint(0, player.max_health//6) # Recovers between 0 and 1/6 of his total health
            player.health = min(player.health + heal, player.max_health) # Cannot heal beyond his total health
            print_colored(f"Te curas {heal} puntos de vida.", Fore.GREEN)
            restore_sound()
        else:
            print_colored("Opción no válida. Pierdes tu turno.", Fore.RED)
        
        if enemy.health <= 0:
            print_colored(f"¡Has derrotado al {enemy.name}!", Fore.GREEN, bold=True)
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
        
        # Enemy's turn
        enemy_damage = random.randint(1, enemy.attack) # Damages between 1 and enemy's attack
        player.health -= enemy_damage 
        print_colored(f"El {enemy.name} te ataca y te hace {enemy_damage} de daño.", Fore.RED)
        if enemy.name == "Dragón Feroz":
            dragon_attack_sound()
        elif enemy.name == "Bruja":
            witch_attack_sound()
        elif enemy.name == "Goblin":
            goblin_attack_sound()
    
    if player.health <= 0:
        print_colored("Has sido derrotado perdedor...", Fore.RED, bold=True)
        defeat_sound()
        return "defeat"

def inicio(player : Player):
    clear_console()
    print_separator('=')
    print_colored("\n--- ACTO I: EL INICIO ---", Fore.YELLOW, bold=True)
    print_colored("Te adentras en la oscura mansión en busca de la princesa.", Fore.WHITE)
    print_colored(f"Tienes un poco de miedo pero no te llamas {player.name} para quedarte solo viendo Netflix.", Fore.WHITE)
    print_colored("Caminas sin esperar lo que se viene.", Fore.WHITE)
    print_colored("Cuando de repente, un terrible monstruo aparece ante ti.", Fore.WHITE)
    input("...")
    monster_sound()

    enemigo_fuerte = Enemy("Monstruo Terrible", 15, 3)
    resultado = combat(player, enemigo_fuerte)
    
    if resultado == "defeat":
        print_colored("El monstruo te ha derrotado, pero no todo está perdido (por ahora)...", Fore.RED)
        defeat_sound()
        input("...")
        print_colored("Despiertas en una celda, herido pero vivo.", Fore.WHITE)
        print_colored("Te preguntas como haras para no sentirte como un perrito encerrado guaof guaof guaof.", Fore.WHITE)
        restore_sound()
        input("...")
        player.health = player.max_health // 2  # Half health restored
        return True
    else:
        print_colored("Matas al monstruo pero su espiritu te clava una espada", Fore.RED)
        print_colored("Lo siento, nunca seras rey.", Fore.RED)
        input("...")
        return True

def nudo_1(player : Player):
    clear_console()
    print_separator('=')
    print_colored("\n--- ACTO II: EL NUDO PARTE 1 ---", Fore.YELLOW, bold=True)
    print_colored("Te adentras más en la mansión, determinado a rescatar a la princesa.", Fore.WHITE)
    input("...")
    goblin_attack_sound()
    enemigo_debil = Enemy("Goblin", 6, 1)
    resultado = combat(player, enemigo_debil)
    
    if resultado == "victory":
        print_colored("Has derrotado al goblin y en su bolsa encuentras una llave.", Fore.GREEN)
        print_colored("Piensas que ojala sea la llave a la habitacion de la princesa...", Fore.GREEN)
        victory_sound()
        input("...")
        print_colored("Pero... en realidad, la llave abre un cofre cercano. ¡Dentro hay una espada mágica!", Fore.WHITE)
        player.attack = random.randint(4, 6)
        print_colored(f"Tu ataque ha aumentado a {player.attack}.", Fore.GREEN)
        input("...")
        restore_sound()
        return True
    else:
        print_colored("Has sido derrotado por el goblin. Tu aventura termina aquí.", Fore.RED)
        print_colored("Que triste que una criatura tan pequeña te haya derrotado. Dale mas duro a la proxima!", Fore.RED)
        input("...")
        defeat_sound()
        return False

def nudo_2(player : Player):
    clear_console()
    print_separator('=')
    print_colored("\n--- ACTO II: EL NUDO PARTE 2 ---", Fore.YELLOW, bold=True)
    print_colored("Despues de matar al goblin, encuentras una habitacion a la izquierda.", Fore.WHITE)
    print_colored("Ya estas cansado y de repente aparece una bruja horrible.", Fore.WHITE)
    print_colored("Piensas que es el ultimo esfuerzo y vas con toda aniquilarla", Fore.WHITE)
    print_colored("Ten cuidado, es una bruja muy malvada que no quiere verte feliz con la princesa, porque la princesa al cantar le da vida a la bruja y eterna juventud.", Fore.WHITE)
    input("...")
    laugh_sound()

    enemigo_debil = Enemy("Bruja", 10, 1)
    resultado = combat(player, enemigo_debil)
    
    if resultado == "victory":
        print_colored("Has derrotado a la bruja.", Fore.GREEN)
        print_colored("Por suerte, en su estanteria, encuentras una pocion que te da fortaleza y te pone papucho para ver a la princesa.", Fore.GREEN)
        print_colored("La pocion sabe algo feo y dudas que funcione.", Fore.GREEN)
        witch_sound()
        print_colored("Pero aun asi te tomas la pocion y recuperas todos tus puntos de vida.", Fore.WHITE)
        print_colored("Estas determinado en encontrar a la princesa y ojala no encontrar mas monstruos porque no quieres despeinarte", Fore.GREEN)
        potion_sound()
        player.health = player.max_health
        print_colored(f"Tu vida ha aumentado a {player.health}.", Fore.GREEN)
        restore_sound()
        input("...")
        return True
    else:
        print_colored("Has sido derrotado por la bruja. Tu aventura termina aquí.", Fore.RED)
        print_colored("Sad, loser. Nunca encontraras a la princesa", Fore.RED)
        defeat_sound()
        input("...")
        return False

def desenlace_1(player : Player):
    clear_console()
    print_separator('=')
    print_colored("\n--- ACTO III: EL DESENLACE PARTE 1---", Fore.YELLOW, bold=True)
    print_colored("Llegas a la cámara final. Un enorme dragón custodia a la princesa.", Fore.WHITE)
    dragon_attack_sound()
    input("...")
    dragon = Enemy("Dragón Feroz", 21, 3)
    resultado = combat(player, dragon)
    
    if resultado == "victory":
        print_colored("¡Has derrotado al dragón y rescatado a la princesa para ser felices forever and ever!", Fore.GREEN, bold=True)
        print_colored("Felicidades, has completado tu misión.", Fore.GREEN)
        print_colored("Tristemente, el dragon nunca conocera a burro y no tendran burros voladores", Fore.GREEN, bold=True)
        victory_sound()
        input("...")
        return True
    else:
        print_colored("El dragón era demasiado poderoso. Tu aventura termina aquí.", Fore.RED)
        defeat_sound()
        input("...")
        return False
    
def desenlace_2():
    clear_console()
    print_separator('=')
    print_colored("\n--- ACTO III: EL DESENLACE PARTE 2---", Fore.YELLOW, bold=True)
    print_colored("Escuchas a la princesa gritar a tu derecha. Corres hacia ella", Fore.WHITE)
    help_sound()
    input("...")

    print_colored("La princesa te pide que la liberes de sus cadenas", Fore.WHITE)
    print_colored("Con tu espada, cortas las cadenas de la princesa", Fore.WHITE)
    print_colored("La princesa te da las gracias y te da un beso en la mejilla", Fore.WHITE)
    input("...")
    print_colored("La princesa te dice que te llevara a su reino y te dara una recompensa", Fore.WHITE)
    input("...")
    print_colored("La princesa te lleva a su reino y te da una recompensa", Fore.WHITE)
    print_colored("La recompensa es casarte con ella y ser el rey de su reino", Fore.GREEN)
    print_colored("Aunque piensas que a los 35 eres muy joven para casarte, aceptas", Fore.GREEN)
    bells_sound()
    input("...")
    
    return True

def princess_rescue():
    clear_console()
    nombre = input("Ingresa el nombre de tu héroe: ")
    player = Player(nombre, health=15, attack=2)
    print_colored(f"Bienvenido, {player.name}. Tu misión es rescatar a la princesa que se encuentra encerrada hace quince años en una mansión abandonada llena de monstruos y criaturas.", Fore.CYAN)
    print_colored(f"{player.name}. esta en tus manos, rescatarla antes que el ogro feo de Shrek ", Fore.CYAN)
    if inicio(player):
        if nudo_1(player):
            if nudo_2(player):
                if desenlace_1(player):
                    desenlace_2()
                    print_colored("¡Has completado el juego! Eres un verdadero héroe, le has ganado a Shrek", Fore.GREEN, bold=True)
                    victory_sound()

    print_colored(f"Gracias por jugar {player.name}.", Fore.CYAN)
    oalQuit()

if __name__ == "__main__":
    princess_rescue()