class Animal:
    def fazer_som(self):
        pass ### prosseguir com a info

class Cachorro(Animal):
    def fazer_som(self):
        return "Au Au"
    
class Gato(Animal):
    def fazer_som(self):
        return "Meau"
    
# usando o polimorfismo 
def fazer_animal_falar(animal: Animal):
    print(animal.fazer_som())

safadao = Cachorro()
panicat = Gato()

fazer_animal_falar(safadao)