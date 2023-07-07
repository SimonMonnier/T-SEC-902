# T-SEC-902

## Aperçu

T-SEC-902-NAN_1 est une application client-serveur basée sur Python. Cette application vous permet d'envoyer et de recevoir des données via une connexion réseau. La paire de scripts fournie est un exemple de serveur client. Le serveur attend des connexions et envoie des commandes à exécuter sur le client. Le client se connecte au serveur et attend les commandes à exécuter. Ce type de configuration est souvent utilisé pour les tests de pénétration ou l'administration à distance.

## Commencer

Avant de commencer, assurez-vous que Python est installé sur votre machine. Vous pouvez télécharger Python à partir de ce lien : https://www.python.org/downloads/.

### Dépendances

Installer les dépendances requises depuis la racine du projet :

```
pip install -r required_dependencies.txt
```

### Configuration initiale

Configuration de l'adresse IP du serveur : Vous devez définir l'adresse IP du serveur dans les scripts du serveur et du client. Pour cela, cherchez la ligne adresse_hote = '192.168.1.57' et remplacez '192.168.1.57' par l'adresse IP de la machine sur laquelle le serveur est en cours d'exécution.

Lancement du serveur : Pour démarrer le serveur, ouvrez un terminal, naviguez jusqu'au répertoire où se trouve le script du serveur et exécutez la commande python server.py. Le serveur commencera alors à écouter les connexions entrantes.

Configuration du client : Pour que le client puisse se connecter au serveur, il doit être exécuté sur la machine cible. Pour cela, vous devez d'abord convertir le script client en un exécutable. Vous pouvez le faire en utilisant des outils tels que PyInstaller. Une fois l'exécutable créé, il doit être envoyé et exécuté sur la machine cible.


## Lancer le Serveur

Pour démarrer le serveur, naviguez jusqu'au répertoire `SERVER` dans votre terminal et exécutez la commande suivante :

```
python server.py
```

## Création d'un Fichier Exécutable

Pour créer un fichier exécutable avec `shell.pyw`, naviguez jusqu'au répertoire `SHELL` dans votre terminal et exécutez la commande suivante : 

```
pyinstaller --onefile shell.pyw
```
Cela va créer un fichier exécutable unique à partir de votre script Python à l'aide du package `pyinstaller`. 


## Commandes

Une fois que le client est connecté au serveur, vous pouvez utiliser les commandes suivantes :

##### cd <chemin>               : Change le répertoire courant sur la machine cliente.
##### start_logger              : Démarre un enregistreur de frappe sur la machine cliente.
##### stop_logger               : Arrête l'enregistreur de frappe et envoie le fichier de journal au serveur.
##### start_webcam              : Démarre la webcam de la machine cliente et envoie les images au serveur.
##### stop_webcam               : Arrête la webcam de la machine cliente.
##### take_photo                : Prend une photo avec la webcam de la machine cliente et la sauvegarde sur le serveur.
##### record_audio <duree>      : Enregistre un audio depuis le microphone du client pendant une durée spécifiée en seconde et l'envoie au

 serveur.
##### create_persistence        : Crée une persistance du script au redémarrage de la machine cliente.
##### start_rdp <adresse>       : Démarre une session RDP à l'adresse spécifiée.
##### stop_connection           : Arrête la connexion entre le serveur et le client.
##### gpt <question>            : Fait appel à GPT-4 pour rechercher des commandes shell et PowerShell ou répondre à toute autre question.
##### copy_file <fichier>       : Copie le fichier spécifié du client vers le serveur.
##### kill                      : Sature le processeur du client rendant le PC inutilisable.
##### infecte                   : Duplique l'exécutable actuel dans tous les autres exécutables du répertoire courant et les place dans le répertoire de démarrage.
##### help                      : Affiche la liste d'aide.
##### back                      : Retour aumenu principal.

Toutes ces commandes doivent être saisies dans la console du serveur. Notez que vous pouvez également exécuter des commandes shell et PowerShell directement depuis le serveur. Elles seront exécutées sur la machine cliente.

Si vous avez besoin d'aide pour une commande, vous pouvez taper `help` dans le terminal pour afficher le menu d'aide :

```
help
```

### Utilisation de la commande GPT

La commande `gpt` utilise le modèle de langage GPT-4 d'OpenAI pour répondre à vos questions ou pour générer des commandes shell et PowerShell. Pour utiliser cette fonctionnalité, vous devez d'abord créer un compte sur OpenAI et obtenir une clé API. Voici comment faire :

1. Allez sur https://beta.openai.com/signup/ et créez un compte.

2. Une fois votre compte créé et validé, connectez-vous et naviguez jusqu'à la section "API Keys" de votre tableau de bord.

3. Cliquez sur "Create new key". Vous pouvez donner un nom à cette clé pour vous souvenir de son utilisation. Assurez-vous de garder cette clé API secrète car elle vous donne accès à l'API OpenAI.

4. Une fois la clé API générée, copiez-la.

5. Revenez à votre script serveur Python et cherchez la ligne où `openai.api_key` est définie. Collez votre clé API en remplaçant la valeur existante.

```python
openai.api_key = 'YOUR_API_KEY'
```

Remplacez `'YOUR_API_KEY'` par la clé API que vous avez copiée. Assurez-vous de conserver les guillemets autour de la clé API.

Une fois la clé API en place, vous pouvez utiliser la commande `gpt` pour poser des questions ou générer des commandes shell ou PowerShell. Par exemple :

```
gpt What is the weather like today?
gpt How do I create a new directory in Linux?
```

Veuillez noter que l'utilisation de l'API OpenAI peut entraîner des coûts en fonction de votre utilisation. Consultez la documentation d'OpenAI pour plus d'informations sur la tarification.

## Persistance

Le script crée une persistance sur la machine sur laquelle est exécuté le script client (uniquement pour un client sous windows 11), ce qui signifie qu'il continuera à s'exécuter même après un redémarrage. Si vous voulez supprimer cette persistance, vous devez supprimer le script du dossier de démarrage de Windows. Voici comment le faire :

1. Appuyez sur la touche Windows + R pour ouvrir la boîte de dialogue Exécuter.
2. Tapez "shell:startup" et appuyez sur Entrée.
3. Cela ouvrira le dossier de démarrage de Windows. Recherchez le script que vous souhaitez supprimer et supprimez-le.

Veuillez noter que ce programme doit être utilisé de manière responsable et éthique. Ne l'utilisez pas sans le consentement approprié, et n'essayez jamais d'accéder illégalement à un système informatique.
