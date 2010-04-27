#encoding: utf8
from django.db import models
import datetime

class Category(models.Model):
    """ Model kategori: """
    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    name = models.CharField(max_length=100, verbose_name="Nazwa")

    def __unicode__(self):
        return u"%s" % self.name

class User(models.Model):
    class Meta:
        verbose_name = "Użytkownika"
        verbose_name_plural = "Użytkownicy"
    """ Model użytkownika wysyłającego testy:
    1.login(login),
    2.hasło(password)
    3.imię i nazwisko """
    login = models.CharField(max_length=30, verbose_name="Nazwa użytkownika")
    password = models.CharField(max_length=30, verbose_name="Hasło")
    full_name = models.CharField(max_length=100, verbose_name="Imię i nazwisko")

    def __unicode__(self):
        return self.full_name

class Test(models.Model):
    """ Model testu:
    1.klucz obcy do użytkownika który wysłał testy
    2.lokalizacje pliku z testem
    3.opis testu """
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
    
    