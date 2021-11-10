import selenium
from selenium import webdriver

# Succès steam TBOI

driver = webdriver.Chrome("C:/Users/elmay/Desktop/chromedriver.exe")
#On récupère les statistiques de jeu générales / Succès généraux <=> % de tous les joueurs ayant débloqué chaque succès
driver.get("https://steamcommunity.com/stats/250900/achievements/")
list_achievements_general = driver.find_elements_by_class_name("achieveTxtHolder")

achievement_accomplished_percentage = dict()

for element in list_achievements_general:
	percentage = round(float(element.find_element_by_class_name('achievePercent').text.replace('%',''))/100,3)
	achievement_name = element.find_element_by_class_name('achieveTxt').text.split('\n')[0]
	achievement_accomplished_percentage[achievement_name] = percentage
# 	print(achievement_name, percentage)
print("Première étape okay")

#On récupère les dates de déblocages personnelles des succès
driver.get("https://steamcommunity.com/profiles/76561198105020499/stats/250900/achievements/")
list_achievements_perso = driver.find_elements_by_class_name("achieveTxtHolder")
achievement_accomplished_personal_unlock = dict()

for element in list_achievements_perso:
	try:
		unlock_date = element.find_element_by_class_name('achieveUnlockTime').text.encode('utf-8')
		unlock_date = unlock_date.replace('Débloqué le '.encode('utf-8'),''.encode('utf-8')).replace('à '.encode('utf-8'),''.encode('utf-8')).decode('utf-8') #.replace('é'.encode('utf-8'),'e'.encode('utf-8'))
		unlock_date = ' '.join([unlock_date.split(' ')[0], unlock_date.split(' ')[1], '2021']) if 'h' in unlock_date.split(' ')[2] else ' '.join(unlock_date.split(' ')[:3])
		unlock_date = unlock_date.replace('janv.','janvier').replace('avr.','avril').replace('juil.', 'juillet').replace('sept.','septembre').replace('aout','août').replace('oct','octobre').replace('nov.','novembre')
		achievement_name = element.find_element_by_class_name('ellipsis').text
		achievement_accomplished_personal_unlock[achievement_name] = unlock_date
		# print(achievement_name, unlock_date)
	except:
		break
print("Deuxième étape okay")

driver.close()

# On mixe le tout et on sort une matrice n*3 où n est le nombre de succès et 3 paramètres : 
# - nom du succès
# - pourcentage de personne l'ayant débloqué
# - date de déblocage du joueur

final_list = []

file = open("data.csv","w")
file.write('Success name,Unlocked by (%),Unlocked by me on\n')

for succes in achievement_accomplished_percentage:
	try:
		final_list.append([succes, achievement_accomplished_percentage[succes], achievement_accomplished_personal_unlock[succes]])
		# print([succes, achievement_accomplished_percentage[succes], achievement_accomplished_personal_unlock[succes]])
	except:
		final_list.append([succes, achievement_accomplished_percentage[succes], ''])
		# print([succes, achievement_accomplished_percentage[succes], ''])

for i in range(len(final_list)):
	for j in range(len(final_list[i])):
		file.write(str(final_list[i][j]))
		file.write(',')
	file.write('\n')
file.close()

print("Troisième étape okay")

