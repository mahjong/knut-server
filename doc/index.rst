Serwer Knut - Dokumentacja
====================================

Jest to dokumentacja techniczna przeznaczona dla programistów, którzy chcą zrozumieć jak działa serwer Knuta - repozytorium testów i odpowiedzi. Składa się ona z opisu klas, atrybutów i metod.

Program został napisany w języku `Python <http://python.org>`_, przy użyciu frameworka `Django <http://www.djangoproject.com/>`_. 


Zawartość:

* :ref:`views`
* :ref:`www`
* :ref:`models`
	
	* :ref:`models-user`
	* :ref:`models-category`
	* :ref:`models-test`
	* :ref:`models-result`
	* :ref:`models-testuser`

.. toctree::
   :maxdepth: 2
 
.. _views:   
   
Opis URL/API, ścieżek zasobów i sposobu komunikacji z serwerem
==============================================================   
   
Komunikacja z serwerem odbywa sie przy pomocy protokołu HTTP, w szczególności metod GET i POST.

Metody edytujące testy weryfikują uprawnienia użytkownika za pomocą loginu i hasła, które muszą być przesłane w żądaniu.

Lista ścieżek zasobów:

	* :ref:`/test_upload - zapisuje test na serwerze <test_upload>`
	* :ref:`/test_list - listuje testy użytkownika <test_list>`
	* :ref:`/test_list_public - listuje testy publiczne wszystkich użytkowników. <test_list_public>`
	* :ref:`/test_delete/test_id - usuwa test o podanym id <test_delete>`
	* :ref:`/questions_download - Metoda zwraca plik z pytaniami do testu <questions_download>`
	* :ref:`/answers_download - Metoda zwraca plik z odpowiedziami do testu <answers_download>`
	* :ref:`/user_answers_download - Pobiera odpowiedzi ucznia w formacie xml <user_answers_download>`
	* :ref:`/results_upload - zapisuje wyniki ucznia na serwerze <results_upload>`
	* :ref:`/results_list - listuje wyniki testu wszystkich uczniów dla podanego testu <results_list>`
	
Opis ścieżek zasobów:

	.. _test_upload:

	* **/test_upload** - zapisuje test na serwerze. Metoda sprawdza czy użytkownik o podanym loginie i haśle istnieje w bazie danych a następnie zapisuje nowy test do bazy danych i przenosi odpowiednie pliki z pytaniami i odpowiedziami do katalogu "test_files/nr_testu/"
		
		Oczekuje na metodę POST zawierającą:
		
		* Login użytkownika - nauczyciela
		* Hasło użytkownika - nauczyciela
		* Tytuł testu
		* Instrukcje do testu
		* Hasło zabezpieczające test przed pobraniem - jęśli test prywatny
		* Kategorię testu
		* Wersję testu
		
	.. _test_list:	
		
	* **/test_list** - listuje testy użytkownika. Metoda zwraca dokument xml z listą testów użytkownika, w szczególności nie pokazuje testów innych użytkowników.

		Oczekuje na metodę POST zawierającą:
		
		* Login użytkownika - nauczyciela
		* Hasło użytkownika - nauczyciela
	   
	.. _test_list_public:   
	   
	* **/test_list_public** - listuje testy publiczne wszystkich użytkowników. Metoda zwraca dokument xml z listą wszystkich testów publicznych.

		Metoda nie oczekuje na argumenty.
		
	.. _test_delete: 
		
	* **/test_delete/<test_id>** - usuwa test o podanym id. Metoda sprawdza czy użytkownik o podanym loginie i haśle istnieje w bazie danych i jest autorem danego testu. Następnie usuwa test z bazy danych i pliki z dysku.
		
		Oczekuje na metodę POST zawierającą:
		
		* Login użytkownika - nauczyciela
		* Hasło użytkownika - nauczyciela
   
	.. _questions_download:    
   
	* **/questions_download** - Metoda zwraca plik z pytaniami do testu. Jeśli test jest prywatny sprawdza dodatkowo czy użytkownik (uczeń) podał poprawne hasło testu, lub czy użytkownik (nauczyciel) jest właścicielem testu. Jeśli żądanie wysłane przez ucznia zakończyło się odesłaniem testu, zapisuje tą informacje w bazie danych. Uczeń wysyła więc id testu, swój login i hasło do testu. Jeśli nauczyciel pobiera pytania do edycji to wysyła id testu, swój login i swoje hasło.
		
		Oczekuje na metodę POST zawierającą:
		
		* Id testu
		* Login użytkownika - ucznia lub nauczyciela
		* Hasło użytkownika - ucznia lub nauczyciela
		
	.. _answers_download: 
		
	* **/answers_download** - Metoda zwraca plik z odpowiedziami do testu. Logika jak w questions_download.
		
		Oczekuje na metodę POST zawierającą:
		
		* Id testu
		* Login użytkownika - ucznia lub nauczyciela
		* Hasło użytkownika - ucznia lub nauczyciela

	.. _user_answers_download:

	* **/user_answers_download** - Pobiera odpowiedzi ucznia w formacie xml. Metoda sprawdza czy użytkownik o podanym loginie i haśle istnieje w bazie danych.
		
		Oczekuje na metodę POST zawierającą:
		
		* Login użytkownika - nauczyciela
		* Hasło użytkownika - nauczyciela
		* Id testu
		* Id użytkownika - ucznia
		* Id odpowiedzi
	
	.. _results_upload:
	
	* **/results_upload** - zapisuje wyniki ucznia na serwerze. Metoda zapisuje login ucznia, id testu i wynik ucznia w bazie danych oraz plik xml z odpowiedziami na dysku w katalogu "results_files/<id_wyników>/".
		
		Oczekuje na metodę POST zawierającą:
		
		* Login użytkownika - ucznia
		* Id testu
		* Punkty uzyskane na teście
		* Punkty uzyskane na teście procentowo
		
	.. _results_list:
		
	* **/results_list** - listuje wyniki testu wszystkich uczniów dla podanego testu. Metoda sprawdza czy użytkownik (nauczyciel) o podanym loginie i haśle istnieje w bazie danych. 
		
		Oczekuje na metodę POST zawierającą:
		
		* Login użytkownika - nauczyciela
		* Hasło użytkownika - nauczyciela
		* Id testu

.. _www:

Opis strony internetowej dostępnej z przeglądarki
=========================================

Strona internetowa programu z opisem działania i możliwością pobrania wszystkich kodu. Użytkownik ma też możliwość przeglądanie testów.
	
	Dostępne podstrony:
	
	* **/** - strona główna programu z podstawowymi informacjami i linkami do programów do pobrania.
	
	* **/categories** - strona listująca kategorie testów
	
	* **/categories/<category-id>** - strona listująca wszystkie testy w wybranej kategorii

.. _models:   
   
Opis klas bazy danych
=====================   
   
.. automodule:: knut_server.tests.models

	.. _models-user:
	
	Klasa opisująca tabelę użytkownika - nauczyciela
	================================================
	
	.. autoclass:: knut_server.tests.models.User
		:members:

	.. _models-category:
	
	Klasa opisująca tabelę kategorii testów
	=======================================
	
	.. autoclass:: knut_server.tests.models.Category
		:members:
		
	.. _models-test:
	
	Klasa opisująca tabelę testów
	=============================
	
	.. autoclass:: knut_server.tests.models.Test
		:members:
		
	.. _models-result:
	
	Klasa opisująca tabelę wyników testu
	====================================
	
	.. autoclass:: knut_server.tests.models.Result
		:members:

	.. _models-testuser:
	
	Klasa opisująca tabelę użytkownika rozwiązującego testy - ucznia
	================================================================
	
	.. autoclass:: knut_server.tests.models.TestUser
		:members:

Indeksy i tabele
==================

* :ref:`genindex`

