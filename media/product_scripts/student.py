class Student:
    def __init__(self, vorname, nachname, matrikelnummer, geburtsdatum, noten):
        self.vorname = vorname
        self.nachname = nachname
        self.matrikelnummer = matrikelnummer
        self.geburtsdatum= geburtsdatum
        self.noten = noten

    def __str__(self):
        return self.vorname + " " + self.nachname

    def __repr__(self):
        return "Matrikelnummer: " + str(self.matrikelnummer) + "\n" + "Geburtsdatum: " + self.geburtsdatum + "\n" + "Alle Noten" + str(self.noten)

    def note_eintragen(self, kurs, note):
        self.noten[kurs] = note

    def noten_berichten(self):
        return self.noten


    def noten_schummeln(self):
        count = 0
        for key in self.noten:
            if self.noten[key] != 1.0:
                self.noten[key] = 1.0
                count+=1

        print(f"{count} Noten wurden verändert")

student1 = Student("max", "muster", 80998, "11.09.99", {})
student1.note_eintragen("Mathe",1.2)
student1.note_eintragen("Mathe2",1.0)
student1.note_eintragen("Deutsch",1.7)
student1.note_eintragen("Medien",1.5)

print(student1.__str__())
print(student1.__repr__())

student1.noten_schummeln()

print(student1.noten_berichten())










