import random
import time
import sys

class TextAdventure:
    def __init__(self):
        self.player_name = ""
        self.difficulty = ""
        self.health = 100
        self.inventory = []
        self.escaped = False
        self.killer_location = "далеко"
        
    def type_text(self, text, delay=0.03):
        """Функция для постепенного вывода текста"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def clear_screen(self):
        """Очистка экрана"""
        print("\n" * 50)
    
    def show_status(self):
        """Показать статус игрока"""
        print(f"\n--- Статус ---")
        print(f"Здоровье: {self.health}%")
        print(f"Инвентарь: {', '.join(self.inventory) if self.inventory else 'пусто'}")
        print(f"Маньяк: {self.killer_location}")
        print("---------------\n")
    
    def choose_difficulty(self):
        """Выбор уровня сложности"""
        self.clear_screen()
        self.type_text("Выберите уровень сложности:")
        self.type_text("1. ЛЕГКИЙ - больше подсказок, маньяк медленнее")
        self.type_text("2. СРЕДНИЙ - баланс между сложностью и шансами")
        self.type_text("3. СЛОЖНЫЙ - мало подсказок, маньяк быстрый и умный")
        
        while True:
            choice = input("\nВаш выбор (1-3): ").strip()
            if choice == "1":
                self.difficulty = "легкий"
                return
            elif choice == "2":
                self.difficulty = "средний"
                return
            elif choice == "3":
                self.difficulty = "сложный"
                return
            else:
                self.type_text("Пожалуйста, выберите 1, 2 или 3")
    
    def killer_moves(self):
        """Движение маньяка в зависимости от сложности"""
        move_chance = {"легкий": 0.3, "средний": 0.5, "сложный": 0.7}[self.difficulty]
        
        if random.random() < move_chance:
            locations = ["далеко", "близко", "очень близко"]
            current_index = locations.index(self.killer_location)
            if current_index < len(locations) - 1:
                self.killer_location = locations[current_index + 1]
                self.type_text("\n...Вы слышите странные звуки... Маньяк приближается!")
    
    def check_killer_attack(self):
        """Проверка атаки маньяка"""
        attack_chance = {"легкий": 0.1, "средний": 0.2, "сложный": 0.3}[self.difficulty]
        
        if self.killer_location == "очень близко" and random.random() < attack_chance:
            damage = random.randint(20, 40)
            self.health -= damage
            self.type_text(f"\n⚡ МАНЬЯК НАПАЛ НА ВАС! Вы потеряли {damage}% здоровья!")
            return True
        return False
    
    def introduction(self):
        """Введение в игру"""
        self.clear_screen()
        self.type_text("=== ПОБЕГ ОТ МАНЬЯКА ===")
        self.type_text("\nВы просыпаетесь в темном, незнакомом подвале...")
        self.type_text("Голова раскалывается, воспоминания отрывочны...")
        self.type_text("Последнее, что помните - странный человек предложил помощь...")
        time.sleep(2)
        
        self.player_name = input("\nКак вас зовут? ").strip()
        if not self.player_name:
            self.player_name = "Незнакомец"
        
        self.choose_difficulty()
        
        self.type_text(f"\nИтак, {self.player_name}, готовьтесь к борьбе за выживание...")
        self.type_text(f"Уровень сложности: {self.difficulty.upper()}")
        self.type_text("Нажмите Enter чтобы продолжить...")
        input()
    
    def basement_scene(self):
        """Сцена в подвале"""
        self.clear_screen()
        self.type_text("=== ПОДВАЛ ===")
        self.type_text("\nВы в холодном, сыром подвале. В воздухе пахнет плесенью и чем-то еще...")
        self.type_text("Слабый свет проникает через маленькое окно под потолком.")
        self.type_text("Вы замечаете несколько предметов вокруг...")
        
        while True:
            self.show_status()
            self.type_text("\nЧто будете делать?")
            self.type_text("1. Осмотреть ящики в углу")
            self.type_text("2. Попробовать открыть дверь")
            self.type_text("3. Взглянуть на окно")
            self.type_text("4. Прислушаться к звукам")
            
            choice = input("\nВаш выбор (1-4): ").strip()
            
            if choice == "1":
                if "ключ" not in self.inventory:
                    self.type_text("\nВ ящиках вы находите старый ржавый ключ!")
                    self.inventory.append("ключ")
                else:
                    self.type_text("\nЯщики пусты.")
            elif choice == "2":
                if "ключ" in self.inventory:
                    self.type_text("\nКлюч подошел! Дверь открыта!")
                    return "corridor"
                else:
                    self.type_text("\nДверь заперта. Нужен ключ.")
            elif choice == "3":
                self.type_text("\nОкно слишком маленькое, чтобы пролезть. Но через него виден лунный свет.")
            elif choice == "4":
                sounds = ["...тишина...", "...скрип...", "...шаги...", "...шепот..."]
                self.type_text(f"\nВы прислушиваетесь: {random.choice(sounds)}")
            else:
                self.type_text("\nНеверный выбор!")
            
            self.killer_moves()
            if self.check_killer_attack():
                if self.health <= 0:
                    return "game_over"
    
    def corridor_scene(self):
        """Сцена в коридоре"""
        self.clear_screen()
        self.type_text("=== КОРИДОР ===")
        self.type_text("\nВы выходите в длинный темный коридор.")
        self.type_text("Стены покрыты странными символами. В конце коридора виднеется лестница.")
        self.type_text("Справа - приоткрытая дверь, слева - шкаф.")
        
        while True:
            self.show_status()
            self.type_text("\nКуда пойдете?")
            self.type_text("1. Подняться по лестнице")
            self.type_text("2. Заглянуть в комнату справа")
            self.type_text("3. Проверить шкаф")
            self.type_text("4. Вернуться в подвал")
            
            choice = input("\nВаш выбор (1-4): ").strip()
            
            if choice == "1":
                if "нож" in self.inventory:
                    self.type_text("\nВы осторожно поднимаетесь по лестнице...")
                    return "living_room"
                else:
                    self.type_text("\nСлишком опасно идти без оружия! Нужно найти что-то для защиты.")
            elif choice == "2":
                if "фонарик" not in self.inventory:
                    self.type_text("\nВ комнате вы находите фонарик! Теперь будет светлее.")
                    self.inventory.append("фонарик")
                else:
                    self.type_text("\nКомната пуста. Только старая мебель и пыль.")
            elif choice == "3":
                if "нож" not in self.inventory:
                    self.type_text("\nВ шкафу вы находите кухонный нож! Хорошее оружие.")
                    self.inventory.append("нож")
                else:
                    self.type_text("\nШкаф пуст.")
            elif choice == "4":
                self.type_text("\nВы возвращаетесь в подвал...")
                return "basement"
            else:
                self.type_text("\nНеверный выбор!")
            
            self.killer_moves()
            if self.check_killer_attack():
                if self.health <= 0:
                    return "game_over"
    
    def living_room_scene(self):
        """Финальная сцена"""
        self.clear_screen()
        self.type_text("=== ГОСТИНАЯ ===")
        self.type_text("\nВы в большой гостиной. Видите входную дверь на свободу!")
        self.type_text("Но внезапно из темноты появляется он... МАНЬЯК!")
        self.type_text("У него в руках бензопила... Она заводится с ужасным ревом!")
        
        escape_chance = {"легкий": 0.8, "средний": 0.6, "сложный": 0.4}[self.difficulty]
        
        while True:
            self.show_status()
            self.type_text("\nФИНАЛЬНАЯ СХВАТКА! Что будете делать?")
            self.type_text("1. Попробовать убежать к двери")
            self.type_text("2. Использовать нож для защиты")
            self.type_text("3. Бросить фонарик в маньяка")
            self.type_text("4. Попробовать договориться")
            
            choice = input("\nВаш выбор (1-4): ").strip()
            
            if choice == "1":
                if random.random() < escape_chance:
                    self.type_text("\nВы бежите к двери! Рука тянется к ручке...")
                    self.type_text("ДВЕРЬ ОТКРЫТА! ВЫ НА СВОБОДЕ!")
                    return "victory"
                else:
                    self.type_text("\nМаньяк перекрыл вам путь! Нужно найти другой способ!")
                    self.health -= 15
            elif choice == "2":
                if "нож" in self.inventory:
                    self.type_text("\nВы раните маньяка ножом! Он отступает с криком!")
                    self.type_text("Это ваш шанс! Вы выбегаете за дверь!")
                    return "victory"
                else:
                    self.type_text("\nУ вас нет ножа! Маньяк смеется над вашей попыткой.")
                    self.health -= 20
            elif choice == "3":
                if "фонарик" in self.inventory:
                    self.type_text("\nВы бросаете фонарик! Он попадает маньяку в голову!")
                    self.type_text("Пока он в замешательстве, вы выскальзываете за дверь!")
                    self.inventory.remove("фонарик")
                    return "victory"
                else:
                    self.type_text("\nНечего бросать! Маньяк приближается...")
                    self.health -= 25
            elif choice == "4":
                self.type_text("\n'Пожалуйста, отпустите меня!' - умоляете вы.")
                self.type_text("'ХА-ХА-ХА! Никогда!' - отвечает маньяк.")
                self.health -= 10
            else:
                self.type_text("\nНет времени на раздумья!")
            
            if self.health <= 0:
                return "game_over"
            
            self.killer_moves()
            if self.check_killer_attack():
                if self.health <= 0:
                    return "game_over"
    
    def game_over(self):
        """Сцена проигрыша"""
        self.clear_screen()
        self.type_text("=== КОНЕЦ ИГРЫ ===")
        self.type_text("\nТемнота поглощает вас...")
        self.type_text("Последнее, что вы слышите - зловещий смех маньяка...")
        self.type_text(f"\n{self.player_name}, вам не удалось выжить.")
        self.type_text("Может, в следующий раз повезет больше...")
    
    def victory(self):
        """Сцена победы"""
        self.clear_screen()
        self.type_text("=== ПОБЕДА! ===")
        self.type_text("\nВы выбегаете на холодный ночной воздух! ВЫ СВОБОДНЫ!")
        self.type_text("За спиной слышен яростный рев бензопилы, но вы уже в безопасности.")
        self.type_text(f"\nПоздравляем, {self.player_name}! Вы пережили этот кошмар!")
        self.type_text(f"Уровень сложности: {self.difficulty}")
        self.type_text(f"Оставшееся здоровье: {self.health}%")
        self.escaped = True
    
    def play(self):
        """Основной игровой цикл"""
        self.introduction()
        
        current_scene = "basement"
        
        while True:
            if current_scene == "basement":
                current_scene = self.basement_scene()
            elif current_scene == "corridor":
                current_scene = self.corridor_scene()
            elif current_scene == "living_room":
                current_scene = self.living_room_scene()
            elif current_scene == "game_over":
                self.game_over()
                break
            elif current_scene == "victory":
                self.victory()
                break
            
            if self.health <= 0:
                self.game_over()
                break
        
        self.type_text("\nСпасибо за игру!")
        time.sleep(2)

# Запуск игры
if __name__ == "__main__":
    game = TextAdventure()
    game.play()