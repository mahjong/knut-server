#encoding: utf8
from django.db import models
import datetime

class Category(models.Model):
    """Klasa kategori testów
    
        Opis pól:
    
        **name**
      
            Nazwa kategorii (100znaków)
    """
    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    name = models.CharField(max_length=100, verbose_name="Nazwa")

    def __unicode__(self):
        return u"%s" % self.name

class User(models.Model):
    """Klasa użytkownika wysyłającego testy - nauczyciela
    
    Opis pól:
    
        **login**
      
            Login, identyfikator nauczyciela (30 znaków)
    
        **password**
            
            Hasło (30 znaków)
            
        **full_name**
        
            Imię i nazwisko (100 znaków)
    """
        
    class Meta:
        verbose_name = "Użytkownika"
        verbose_name_plural = "Użytkownicy"

    login = models.CharField(max_length=30, verbose_name="Nazwa użytkownika")
    password = models.CharField(max_length=30, verbose_name="Hasło")
    full_name = models.CharField(max_length=100, verbose_name="Imię i nazwisko")
    
    def __unicode__(self):
        return self.full_name

class Test(models.Model):
    """ Klasa testu, dane opisujące test zapisywane są w bazie danych, natomiast pliki z pytaniami i odpowiedziami na dysku.
    
        Opis pól:
            
            **user**
            
                Klucz obcy do użytkownika, który wysłał testy
            
            **category**
            
                Klucz obcy do kategorii testu
                
            **title**
            
                Tytuł testu (30 znaków)
            
            **instructions**
            
                Instrukcje do testu (256 znaków)
                
            **password**
            
                Hasło testu (30 znaków)
                
            **version**
            
                Wersja testu (liczba całkowita)
                
            **id_unq**
            
                Unikalne id testu (10 znaków)
    """
    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testy"
        
    user = models.ForeignKey(User, verbose_name="Użytkownik")
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name="Kategoria")
    title = models.CharField(max_length=30, verbose_name="Tytuł")
    instructions = models.CharField(max_length=256, verbose_name="Instrukcje")
    password = models.CharField(max_length=30, null=True, blank=True, verbose_name="Hasło")
    version = models.IntegerField(verbose_name="Wersja")
    id_unq = models.CharField(max_length=10, verbose_name="Unikalne id")

    def __unicode__(self):
        return u"A: %s, T: %s, I: %s" %(self.user, self.title, self.instructions)

class Result(models.Model):
    """ Klasa wyników testu. Wynik punktowy zapisywany jest bazie danych. Lista odpowiedzi udzielonych przez ucznia zapisywana jest na dysku w formacie xml.
    
        Opis pól:
            
            **user_id_unq**
            
                Unikalne id użytkownika (30 znaków)
            
            **test_id_unq**
            
                Unikalne id testu (10 znaków)
                
            **points**
            
                Wynik z testu wyrażony w punktach (liczba zmiennoprzecinkowa)
            
            **points_percentage**
            
                Wynik z testu wyrażony w procentach (liczba zmiennoprzecinkowa)
                
            **ts_created**
            
                Stempel czasowy
    """
    class Meta:
        verbose_name = "Wynik"
        verbose_name_plural = "Wyniki"
    user_id_unq = models.CharField(max_length=30, verbose_name="Id użytkownika")
    test_id_unq = models.CharField(max_length=10, verbose_name="Unikalne id testu")
    points = models.FloatField(verbose_name="Punkty")
    points_percentage = models.FloatField(verbose_name="Wynik procentowo")
    ts_created = models.DateTimeField(default=datetime.datetime.now, verbose_name="Data utworzenia")
    
    def __unicode__(self):
        return unicode("Uczeń:".decode('utf8')) + " %s, Test: %s, Wynik (punkty): %s, Wynik (procentowy): %s" % (self.user_id_unq, self.test_id_unq, self.points, self.points_percentage)
    
class TestUser(models.Model):
    """ Klasa opisująca obiekt rozwiązywanego testu. Zapisuje datę rozpoczęcia i odesłania wyników testu.
    
        Opis pól:
            
            **user_id_unq**
            
                Unikalne id użytkownika (30 znaków)
            
            **test_id_unq**
            
                Unikalne id testu (10 znaków)
                               
            **ts_created**
            
                Stempel czasowy
                
            **ts_returned**
            
                Stempel czasowy
    """
    class Meta:
        verbose_name = "Użytkownicy rozwiązujący testy"
        verbose_name_plural = "Użytkownicy rozwiązujący testy"
    user_id_unq = models.CharField(max_length=30, verbose_name="Id użytkownika")
    test_id_unq = models.CharField(max_length=10, verbose_name="Unikalne id")
    ts_created = models.DateTimeField(default=datetime.datetime.now, verbose_name="Data wysłania pytań")
    ts_returned = models.DateTimeField(null=True, blank=True, verbose_name="Data odesłania testu")

    def __unicode__(self):
        return unicode(self.user_id_unq) + u" -> " + unicode(self.test_id_unq)
    
    def test_returned(self):
        self.ts_returned = datetime.datetime.now()
        self.save()
    
    