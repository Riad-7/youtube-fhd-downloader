# YouTube FHD Downloader

Application de bureau en Python avec Tkinter pour télécharger une vidéo YouTube en MP4. Elle sélectionne la meilleure qualité disponible jusqu’à 1080p. Si la vidéo ne propose pas de 1080p, l’application sélectionne automatiquement une résolution inférieure.

## Fonctionnalités

- Téléchargement d’une vidéo à partir de son lien YouTube
- Choix du dossier de destination
- Suivi de la progression des flux vidéo et audio
- Assemblage de la vidéo et de l’audio avec FFmpeg

## Installation sur Windows

Installez Python 3 avec Tkinter, puis ouvrez PowerShell dans le dossier qui contient `youtube_fhd.py`.

```powershell
py -m pip install -U "yt-dlp[default]"
winget install --id Gyan.FFmpeg -e
winget install --id DenoLand.Deno -e
```

FFmpeg et FFprobe servent au traitement du fichier vidéo. Deno permet à yt-dlp de traiter les défis JavaScript de YouTube. Après l’installation, fermez PowerShell et ouvrez une nouvelle fenêtre pour que Windows retrouve ces commandes.

## Utilisation

Depuis le dossier du script, lancez l’application.

```powershell
py .\youtube_fhd.py
```

1. Collez le lien d’une vidéo YouTube.
2. Cliquez sur **Parcourir…** pour choisir le dossier de destination.
3. Cliquez sur **Télécharger**. Le fichier MP4 sera enregistré dans le dossier choisi.

Une connexion Internet est nécessaire pour télécharger la vidéo. Le fichier MP4 peut ensuite être lu hors ligne.

## Dépannage

- **Le raccourci du Bureau ne lance pas l’application.** Exécutez la commande de lancement dans PowerShell pour afficher l’erreur.
- **L’application indique que FFmpeg est manquant.** Vérifiez que `ffmpeg -version` et `ffprobe -version` fonctionnent dans une nouvelle fenêtre PowerShell.
- **Le téléchargement échoue.** Vérifiez le lien et la connexion, puis mettez à jour yt-dlp avec la commande d’installation ci-dessus.

Utilisez l’application pour les vidéos que vous possédez ou que vous êtes autorisé à télécharger.
