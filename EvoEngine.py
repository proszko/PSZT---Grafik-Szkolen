#!/usr/bin/python3
# -*- coding: utf-8 -*-
from random import *
from math import *
import collections
import operator
import time


def dataAssignment(simpleDataList, listedDataList):
	global ilosc_pokolen, liczebnosc, mutate_chance, t_dnia, n_dni, n_sal, typy_szkolen, n_uczestnikow
	global pojemnosc_sal, pojemnosc_szkolen, t_szkolen, max_szkolen, preferencje_ucz
	
	ilosc_pokolen = simpleDataList[0]
	liczebnosc = simpleDataList[1]
	mutate_chance = simpleDataList[2]
	t_dnia = simpleDataList[3]
	n_dni = simpleDataList[4]
	n_sal = simpleDataList[5]
	typy_szkolen = simpleDataList[6]
	n_uczestnikow = simpleDataList[7]
	
	pojemnosc_sal = listedDataList[0]
	pojemnosc_szkolen = listedDataList[1]
	t_szkolen = listedDataList[2]
	max_szkolen = listedDataList[3]
	preferencje_ucz = listedDataList[4]
	
	

def random_genotyp(bity_sali,bity_preferencji):
    genotyp_preferencji=[]
    genotyp_sali=[]
    for i in range(bity_sali):
        test=random()
        if test>0.5:
            genotyp_preferencji.append(True)
        else:
            genotyp_preferencji.append(False)
    for j in range(bity_preferencji):
        test=random()
        if test>0.5:
            genotyp_sali.append(True)
        else:
            genotyp_sali.append(False)      
            
    return [genotyp_preferencji,genotyp_sali]
  
def inverse(gen):
    if gen==False:
        gen=True
    elif gen==True:
        gen=False
    return gen

def xor(bit1,bit2):
    if (bit1==bit2):
        result=False
    else:
        result=True
    return result
    
def gray2int(word):
   
    length=len(word)
    nkbit=word[0]
    result=nkbit*pow(2,length-1)
    
    for i in range(1,length,1):
        nkbit=xor(nkbit,word[i])
        result+=nkbit*pow(2,length-i-1)
    
    return int(result)        


# Negacja losowych genow 
def mutate(genotyp,bity_sali,bity_preferencji,mutate_chance):
                              
    for i in range(bity_sali):
        test=random()
        if test<mutate_chance:
            genotyp[0][i]=inverse(genotyp[0][i])
            
    for j in range(bity_preferencji):
        test=random()
        if test<mutate_chance:
            genotyp[1][j]=inverse(genotyp[1][j])
            
            
    
    return genotyp
    

def krzyzowanie(genotyp1,genotyp2,bity_sali,bity_preferencji):
    potomek1=[[],[]]
    potomek2=[[],[]]
    
    
    test=randint(1,bity_sali)     
    
    # Losujemy jeden punkt podzialu
    for i in range(test):
        
        potomek1[0].append(genotyp1[0][i])
        potomek2[0].append(genotyp2[0][i])
    
    
    for j in range(test,bity_sali):
        
        potomek1[0].append(genotyp2[0][j])
        potomek2[0].append(genotyp1[0][j])
        
    
    # Losujemy drugi punkt podzialu    
    test2=randint(1,bity_preferencji)    

    for i in range(test2):
        
        potomek1[1].append(genotyp1[1][i])
        potomek2[1].append(genotyp2[1][i])
    
    for i in range(test2,bity_preferencji):
        
        potomek1[1].append(genotyp2[1][i])
        potomek2[1].append(genotyp1[1][i])        
    

    return potomek1,potomek2
    
   
   
   
   # Funkcja mapujaca wartosci chromosowow typow szkolen na wlasciwe szkolenia
   # z uwagi na to ze liczba szkolen jest rozna z reguly od maksymalnych kombinacji
   # kodowanych przez te bity, niektore (najpopularniejsze) szkolenia beda kodowane
   # wieksza ilosc razy
   
def typ_szkolenia_map(preferencje_szk,typy_szkolen):
    
    max_komb_typu_szkolen=int(pow(2,ceil(log(typy_szkolen,2)))) 
    unused_komb=max_komb_typu_szkolen-typy_szkolen

    komb_typ_szkolenia=[]
    genotyp2typ_szkolenia_map=[]

    popyt_szk={}
    pref_sum=0


    for i in range(typy_szkolen):
        popyt_szk[i]=len(preferencje_szk[i])
        pref_sum+=len(preferencje_szk[i])
        komb_typ_szkolenia.append([])
    
    # Sortowanie szkolen wedlug preferencji
    dict=collections.OrderedDict(sorted(popyt_szk.items(), key=lambda t: t[1],reverse=True))

    # Przyporzadkowanie liczby wystapien kombinacji bitowych do danych szkolen
    for ite in dict.items():
        slots=float(ite[1])/(pref_sum)*max_komb_typu_szkolen
        slots=floor(slots)
        slots=max(slots,1)
        slots=min(slots,unused_komb+1)
        unused_komb+=1-slots
    
        komb_typ_szkolenia[ite[0]]=int(slots)
    
    # Tworzenie ostatecznej mapy przyporzadkowan
    i=0
    while unused_komb>0:
        komb_typ_szkolenia[i]=komb_typ_szkolenia[i]+1
        unused_komb-=1
        i+=1
        

    for i in range(typy_szkolen):
        for j in range(komb_typ_szkolenia[i]):
            genotyp2typ_szkolenia_map.append(i)
    
    return genotyp2typ_szkolenia_map
    

    # Przeksztalcanie danej sekwencji bitowej na odpowiednia ceche fenotypu
def decode(chromosom,typ_map):
    no_kombinacji=gray2int(chromosom)
    no_fenotypu=typ_map[no_kombinacji]
    return no_fenotypu

    # Analogiczne dzialanie jak przy tworzeniu map uzytkownikow, tylko tutaj
    # preferowane sa krotsze dlugosci przerw
def przerwa_map(t_dnia):
    max_komb_przerwy=int(pow(2,ceil(log(t_dnia+1,2)))) 
    unused_komb=max_komb_przerwy-t_dnia
    
    komb_przerwa=[]
    for i in range(t_dnia+1):
        if unused_komb>0:
            komb_przerwa.append(int(1+ceil(float(unused_komb/2))))
            unused_komb+=1-komb_przerwa[i]
        else:
            komb_przerwa.append(1)
    
    genotyp2przerwa_map=[]
    
    for i in range(t_dnia+1):
        for j in range(komb_przerwa[i]):
            genotyp2przerwa_map.append(i)
    
    return genotyp2przerwa_map
    
    
    # Przeksztalcanie pierwszej czesci genotypu na fenotyp
def create_plan_szkolen(genotyp):
	global max_szkolen
	instancje_szkolen=[]
	for i in range(typy_szkolen):
		instancje_szkolen.append([])
		
	uzyte_szkolenia=[]
	for i in range(typy_szkolen):
		uzyte_szkolenia.append(0)

	grafik=[]
	current_bit=0
	remaining_szkolenia=max_szkolen.copy()
	wolne_szkolenia=True                      #Jesli jakiekolwiek szkolenie jest dostepne do wlozenia to jest True
	
	for i in range(n_sal):
		grafik.append([])
		
		for j in range(n_dni):
			grafik[i].append([])
			
			no_szkolenia=0                     #chronologiczny numer szkolenia w danej sali w danym dniu
			current_hour=0
			current_bit= i * n_dni * bity_dnia *(bity_szkolenia+bity_przerwy) + j * bity_dnia *(bity_szkolenia+bity_przerwy)
			
			while current_hour<t_dnia:
				
				chromosom_przerwy=genotyp[0][current_bit:current_bit+bity_przerwy]
				dlugosc_przerwy=decode(chromosom_przerwy,przerwy_map)   
				
				if(dlugosc_przerwy+current_hour<=t_dnia):
					current_bit+=bity_przerwy
					current_hour+=dlugosc_przerwy
				else:
					break                #koniec dnia

				chromosom_szkolenia=genotyp[0][current_bit:current_bit+bity_szkolenia]
				typ_szkolenia=decode(chromosom_szkolenia,szkolenia_map)
				wyj_szkolenie=typ_szkolenia
				
				while (remaining_szkolenia[typ_szkolenia]==0 and wolne_szkolenia==True):    # Jesli nie mamy takiego szkolenia juz w zapasie to bierzemy nastepne
					typ_szkolenia+=1 #remaining_szkolenia[typ_szkolenia]>0 and wolne_szkolenia==True
					typ_szkolenia= typ_szkolenia%typy_szkolen      # to nam zalatwia automatyczne przechodzenie z ostatniego szkolenia do zerowego
					if typ_szkolenia==wyj_szkolenie:               # Zrobilismy caly obrot a tu ciagle nie ma wolnych szkolen
						wolne_szkolenia=False
						
						
				dlugosc_szkolenia=t_szkolen[typ_szkolenia]
				
				if (dlugosc_szkolenia+current_hour<=t_dnia and wolne_szkolenia==True):        # Jesli miesci sie w dniu
					current_bit+=bity_szkolenia

					grafik[i][j].append({})
					grafik[i][j][no_szkolenia]["Start"]=current_hour
					current_hour+=dlugosc_szkolenia
					grafik[i][j][no_szkolenia]["Koniec"]=current_hour
					grafik[i][j][no_szkolenia]["Szkolenie"]=typ_szkolenia
					grafik[i][j][no_szkolenia]["Uczestnicy"]=[]
					#grafik[i][j][no_szkolenia]["Id_szkolenia"]=no_szkolenia
					instancje_szkolen[typ_szkolenia].append({})
					instancje_szkolen[typ_szkolenia][uzyte_szkolenia[typ_szkolenia]]["Sala"]=i
					instancje_szkolen[typ_szkolenia][uzyte_szkolenia[typ_szkolenia]]["Dzien"]=j
					instancje_szkolen[typ_szkolenia][uzyte_szkolenia[typ_szkolenia]]["Godzina"]=current_hour-dlugosc_szkolenia
					instancje_szkolen[typ_szkolenia][uzyte_szkolenia[typ_szkolenia]]["No_szkolenia"]=no_szkolenia
					uzyte_szkolenia[typ_szkolenia]+=1
					no_szkolenia+=1;
					remaining_szkolenia[typ_szkolenia]-=1
					
				else:                                             # Jesli nie miesci sie to konczymy tworzenie grafika danego dnia
					break

	# Sortujemy tablice instancje szkolen ktora bedzie uzyteczna przy konwersji drugiej czesci genotypu na fenotyp
	for i in range(typy_szkolen):
		instancje_szkolen[i]=sorted(instancje_szkolen[i], key=lambda x:(x["Dzien"],x["Godzina"],x["Sala"]))

	return grafik,instancje_szkolen,uzyte_szkolenia
    
    # Przeksztalcanie drugiej czesci genotypu na fenotyp
def create_plan_uczestnikow(grafik,instancje_szkolen,uzyte_szkolenia,genotyp):
    current_bit=0
    grafik_uczestnikow=[]
    
    for i in range(n_uczestnikow):
      
        grafik_uczestnikow.append([])
        for j in range(n_dni):
            grafik_uczestnikow[i].append([])

    
    for preferencja in preferencje:
        no_uczestnika=preferencja[0]
        no_szkolenia=preferencja[1]
        n_bitow_szkolenia=kombinacje_szkolen[no_szkolenia]
        
        chromosom=genotyp[1][current_bit:current_bit+n_bitow_szkolenia]
        try:
            pozycja=gray2int(chromosom)%uzyte_szkolenia[no_szkolenia]                  #pozycja - chronologiczny numer instancji szkolenia na ktory uzytkownik jest zapisywany
        except ZeroDivisionError:                                              # brak takich szkolen
            current_bit+=kombinacje_szkolen[no_szkolenia]
            continue
        except IndexError:                                                       # jesli mamy tylko jedna maksymalna instancje szkolenia
            pozycja=0  
        pozycja_pierwotna=pozycja
        
        try:                                                                
            numer_sali=instancje_szkolen[no_szkolenia][pozycja]["Sala"]
        except IndexError:                                #jesli nie ma wgl takiego szkolenia w planie
            current_bit+=kombinacje_szkolen[no_szkolenia]
            continue
            
        numer_dnia=instancje_szkolen[no_szkolenia][pozycja]["Dzien"]
        godzina_rozpoczecia=instancje_szkolen[no_szkolenia][pozycja]["Godzina"]
        godzina_zakonczenia=godzina_rozpoczecia+t_szkolen[no_szkolenia]
        
        id_szkolenia=instancje_szkolen[no_szkolenia][pozycja]["No_szkolenia"]    # id_szkolenia - chronologiczny numer szkolenia odbywajacy sie danego dnia w danej sali
        wszystkie_sprawdzone=False
        pasujacy_termin=True
        
        for szkolenia in grafik_uczestnikow[no_uczestnika][numer_dnia]:
            for godzina in range (t_szkolen[no_szkolenia]):
                if godzina+godzina_rozpoczecia>=szkolenia["Godzina rozpoczecia"] and godzina_rozpoczecia<szkolenia["Godzina zakonczenia"]:   #nowe szkolenie zaczyna sie w czasie trwania innego
                    pasujacy_termin=False
        
        while (len(grafik[numer_sali][numer_dnia][id_szkolenia]["Uczestnicy"])==pojemnosc_sal[numer_sali] or len(grafik[numer_sali][numer_dnia][id_szkolenia]["Uczestnicy"])==pojemnosc_szkolen[id_szkolenia] or pasujacy_termin==False) and wszystkie_sprawdzone==False:    #jesli na dane szkolenie sala jest juz pelna, zapisanych jest tyle osob rowne pojemnosci sali lub szkolenie jest pelne lub uzytkownikowi nie pasuje dany termin szukamy innego(ktorego jeszcze nie znalezlismy)
            pozycja=(pozycja+1)%uzyte_szkolenia[no_szkolenia]                     #Bierzemy nastepne w kolejnosci
            numer_sali=instancje_szkolen[no_szkolenia][pozycja]["Sala"]
            numer_dnia=instancje_szkolen[no_szkolenia][pozycja]["Dzien"]
            id_szkolenia=instancje_szkolen[no_szkolenia][pozycja]["No_szkolenia"]
            
            for szkolenia in grafik_uczestnikow[no_uczestnika][numer_dnia]:
                for godzina in range (t_szkolen[no_szkolenia]):
                    if godzina+godzina_rozpoczecia>=szkolenia["Godzina rozpoczecia"] and godzina_rozpoczecia<szkolenia["Godzina zakonczenia"]:   #nowe szkolenie koliduje w czasie trwania innego
                        pasujacy_termin=False
            
            if pozycja==pozycja_pierwotna:
                wszystkie_sprawdzone=True
                
                
        if wszystkie_sprawdzone==False:             # Innymi slowy istnieje wolny termin dla uzytkownika
            grafik[numer_sali][numer_dnia][id_szkolenia]["Uczestnicy"].append(no_uczestnika)     #wpisujemy uczestnika do grafika ogolnego
            grafik_uczestnikow[no_uczestnika][numer_dnia].append({"Godzina rozpoczecia":godzina_rozpoczecia,"Godzina zakonczenia":godzina_zakonczenia,"Szkolenie":no_szkolenia,"Sala":numer_sali})
            

                
        current_bit+=kombinacje_szkolen[no_szkolenia] 

    for i in range(n_uczestnikow):
        for j in range(n_dni):
            
            grafik_uczestnikow[i][j]=sorted(grafik_uczestnikow[i][j], key=lambda x:(x["Godzina rozpoczecia"]))            
    return grafik,grafik_uczestnikow
    


def funkcja_przystosowania (t_dnia,grafik,grafik_uczestnikow):
    w1=10000                                       # modyfikator zapisanach uczestnikow
    w2=20*n_sal                                        # modyfikator ilosci dni o ktorej udalo sie skrocic cykl szkoleniowy
    w3=-10                                         # modyfikator sumy dni przez ktore musiala byc uzykowana kazda sala (dzien ostatni-dzien pierwszy+1)
    w4=-2                                          # liczba przeprowadzonych szkolen                    
    w5=-0.2                                          # modyfikator sumy dlugosci trwania okienek uczestnikow
    w6=-1                                           # modyfikator sumy dlugosci trwania szkolen uczestnikow (w dniach
    w7=-30                                            # modyfikator liczby uczestnikow niezapisanych na zadne szkolenie
    
    z1=0
    z2=0
    z3=0
    z4=0
    z5=0
    z6=0
    z7=0
    poczatek_uzytku_glob=n_dni                                  
    koniec_uzytku_glob=1
    
    for i in range(n_sal):
        poczatek_uzytku=None
        koniec_uzytku=None
        
        for j in range (n_dni):
         
            if grafik[i][j]:                                        #Jesli lista nie jest pusta
                if poczatek_uzytku==None:
                    poczatek_uzytku=j
                koniec_uzytku=j
            for szkolenia in grafik[i][j]:
                z1+=len(szkolenia["Uczestnicy"])
                z4+=1
                
        if poczatek_uzytku!=None:                                #Byly jakies szkolenia tego dnia
            poczatek_uzytku_glob=min(poczatek_uzytku,poczatek_uzytku_glob)   
            koniec_uzytku_glob=max(koniec_uzytku,koniec_uzytku_glob)
            z3+=koniec_uzytku-poczatek_uzytku+1  
            
                                       
    z2=n_dni-(koniec_uzytku_glob-poczatek_uzytku_glob+1)
    

    for i in range(n_uczestnikow):
        last_day=-1                                          #Dzien ostatniego szkolenia
        first_day=-1                                         #Dzien pierwszego szkolenia
        
        for j in range(n_dni):
            recent_hour=-1                                    #Godzina zakonczenia ostatniego szkolenia
            
            for szkolenia in grafik_uczestnikow[i][j]:
                if recent_hour!=-1:                            #Jesli to nie jest pierwsze szkolenie danego dnia
                    z5+=szkolenia["Godzina rozpoczecia"]-recent_hour
                recent_hour=szkolenia["Godzina zakonczenia"] 
                
                if first_day==-1:
                    first_day=j
                last_day=j
                
        if first_day!=-1:
            z6+=last_day-first_day+1 
        else:                                    #uztkownik niezapisany na zadne szkolenie
            z7+=1

    return w1*z1+w2*z2+w3*z3+w4*z4+w5*z5+w6*z6+w7*z7


#Zbiorcze przeksztalcenie genotypu na fenotyp
def genotyp2fenotyp(genotyp):
    
    grafik,instancje_szkolen,uzyte_szkolenia=create_plan_szkolen(genotyp)
    
    grafik,grafik_uczestnikow=create_plan_uczestnikow(grafik,instancje_szkolen,uzyte_szkolenia,genotyp)
    
    return grafik,grafik_uczestnikow
    

# Tworzenie wyjsciowej populacji

def generateRandomPopulation(ilosc_pokolen,liczebnosc):
    
    rodzice_0=[]
    potomstwo=[]
    przystosowanie_rodzicow_0=[]
    przystosowanie_potomstwa=[]
    for i in range(liczebnosc):                                      
        rodzice_0.append(random_genotyp(bity_sali,bity_preferencji))
        potomstwo.append(None)
        grafik_0,grafik_ucz_0=genotyp2fenotyp(rodzice_0[i])
        
        przystosowanie_rodzicow_0.append(funkcja_przystosowania (t_dnia,grafik_0,grafik_ucz_0) )
        przystosowanie_potomstwa.append(None)
        
        
    return rodzice_0,potomstwo,przystosowanie_rodzicow_0,przystosowanie_potomstwa


def doAlgorithm(ilosc_pokolen,liczebnosc,mutate_chance,rodzice_startowi,potomstwo,przystosowanie_rodzicow_0,przystosowanie_potomstwa):  
 
    rodzina=[]
    rodzice=rodzice_startowi
    przystosowanie_rodzicow=przystosowanie_rodzicow_0
    
    szkolenia_map=typ_szkolenia_map(preferencje_szk,typy_szkolen)
    przerwy_map=przerwa_map(t_dnia)
    
    mutate_chance=0.1

    for no_pokolenia in range(ilosc_pokolen):
        
        
        for no_potomka in range(0,liczebnosc,2):
            
            # Losowanie dwoch rodzicow
            no_rodzica1=randint(0,liczebnosc-1)
            no_rodzica2=randint(0,liczebnosc-1)
            while no_rodzica1==no_rodzica2:                             # Rodzice musza byc rozni, jesli nie sa to losujemy jeszcze raz 
                no_rodzica1=randint(0,liczebnosc-1)
                no_rodzica2=randint(0,liczebnosc-1) 
                
            rodzic1=rodzice[no_rodzica1]
            rodzic2=rodzice[no_rodzica2]
            # Generujemy potomkow
            potomek1,potomek2=krzyzowanie(rodzic1,rodzic2,bity_sali,bity_preferencji)
            potomstwo[no_potomka]=mutate(potomek1,bity_sali,bity_preferencji,mutate_chance)
            potomstwo[no_potomka+1]=mutate(potomek2,bity_sali,bity_preferencji,mutate_chance)
            
            # Generujemy fenotypy potomkow
            grafik1,grafik_ucz1=genotyp2fenotyp(potomek1)
            przystosowanie_potomstwa[no_potomka]=funkcja_przystosowania (t_dnia,grafik1,grafik_ucz1)  
            
            grafik2,grafik_ucz2=genotyp2fenotyp(potomek2)            
            przystosowanie_potomstwa[no_potomka+1]=funkcja_przystosowania (t_dnia,grafik2,grafik_ucz2)
            
            # Generujemy przystosowania
            rodzina=rodzice+potomstwo
            przystosowania=przystosowanie_rodzicow+przystosowanie_potomstwa
            
            
            # Bierzemy osobnikow o najlepszym przystosowaniu
        for i in range(liczebnosc):
               
                
            max_index, max_value = max(enumerate(przystosowania), key=operator.itemgetter(1))
            przystosowania[i]=0
            rodzice[i]=rodzina[max_index]
            przystosowanie_rodzicow[i]=max_value
            
            
        #print(max(przystosowanie_rodzicow))
    
    optymalny_grafik,optymalny_grafik_uczestnikow=genotyp2fenotyp(rodzice[0])    
    
    
    return optymalny_grafik,optymalny_grafik_uczestnikow,max(przystosowanie_rodzicow)
    
    

# ############################## Przeksztalcanie danych do bardziej zjadliwej formy 

def convertData():

# Preferencje szkolen - dla kazdego szkolenia: uzytkownicy ktory chca sie na nie zapisac
    preferencje_szk=[]
    for i in range(typy_szkolen):
        preferencje_szk.append([])
 
    kombinacje_szkolen=[]                   #ile bitow potrzebujemy do zakodowania wszystkich instancji szkolenia, zalezne od max_szkolen 
    for i in range(typy_szkolen):
        kombinacje_szkolen.append(int(ceil(log(max_szkolen[i],2))))


# Preferencje: wszystkie pary uzytkownik, szkolenie na ktore chce sie zapisac
    preferencje=[]

    for no_uczestnika in range(n_uczestnikow):
        for preferencja in preferencje_ucz[no_uczestnika]:
            preferencje_szk[preferencja].append(no_uczestnika)
       
    bity_preferencji=0
    for i in range(typy_szkolen):
        bity_preferencji+=len(preferencje_szk[i])*kombinacje_szkolen[i]
    

    for i in range(typy_szkolen):
        for j in range(n_uczestnikow):
            try:
                preferencje.append([j,preferencje_ucz[j][i]])
            except IndexError:
                continue
        
# Liczenie dlugosci slow bitowych
    bity_szkolenia=int(ceil(log(typy_szkolen,2)))
    bity_przerwy=int(ceil(log(t_dnia+1,2)))
    bity_dnia=int(floor (t_dnia/min(t_szkolen)))

    bity_sali= int(n_sal * n_dni * bity_dnia *(bity_szkolenia+bity_przerwy))  
    
    return preferencje_szk,preferencje,kombinacje_szkolen,bity_preferencji,bity_sali,bity_szkolenia,bity_przerwy,bity_dnia



def testParameters():
    
 
    przystosowanie_rodzicow_0=[]   
    av_used_time=0
    av_results=0

    
    m=60
    n=60
    
    for p in [0.001,0.005,0.01,0.05,0.1]:
        av_results=0
        
        for it in range(20):                    # ilosc probek
            rodzice_0,potomstwo,przystosowanie_rodzicow_0,przystosowanie_potomstwa=generateRandomPopulation(m,n)
            a,b,przystosowanie=doAlgorithm(m,n,p,rodzice_0,potomstwo,przystosowanie_rodzicow_0,przystosowanie_potomstwa)
            end=time.time()
            av_results+=0.05*przystosowanie
                
        print("\nSzansa mutacji:",p,"\nwynik koncowy:",round(av_results,2))        
    return

    

def runTheCode():
	global preferencje_szk,preferencje,kombinacje_szkolen,bity_preferencji,bity_sali,bity_szkolenia,bity_przerwy,bity_dnia
	global szkolenia_map, przerwy_map
	global rodzice_0,potomstwo,przystosowanie_rodzicow_0,przystosowanie_potomstwa
	global optymalny_grafik,optymalny_grafik_uczestnikow,przystosowanie_koncowe
	global max_szkolen
	
	
	# ##################################  REWARD: PLAN SZKOLEN  
	preferencje_szk,preferencje,kombinacje_szkolen,bity_preferencji,bity_sali,bity_szkolenia,bity_przerwy,bity_dnia=convertData()

	szkolenia_map=typ_szkolenia_map(preferencje_szk,typy_szkolen)
	przerwy_map=przerwa_map(t_dnia)
	# ####################################### GROUNDWORK ########################################
	forNerds = [bity_sali, bity_preferencji, len(preferencje)]

	best_przystosowanie=0
	for k in range(5):
		rodzice_0,potomstwo,przystosowanie_rodzicow_0,przystosowanie_potomstwa = generateRandomPopulation(ilosc_pokolen,liczebnosc)
		optymalny_grafik,optymalny_grafik_uczestnikow,przystosowanie_koncowe=doAlgorithm(ilosc_pokolen,liczebnosc,mutate_chance,rodzice_0,potomstwo,przystosowanie_rodzicow_0,przystosowanie_potomstwa)
		print(przystosowanie_koncowe)
		if przystosowanie_koncowe>best_przystosowanie:
			best_przystosowanie=przystosowanie_koncowe
			best_grafik=optymalny_grafik
			best_grafik_ucz=optymalny_grafik_uczestnikow

	forNerds.append(best_przystosowanie)
	return best_grafik, best_grafik_ucz, forNerds
