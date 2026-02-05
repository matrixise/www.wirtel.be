---
modified: 2026-01-04T17:57:51+01:00
tags:
- tool
author: Stephane Wirtel
date: 2012-02-21
lang: fr
title: MailCatcher, L'outil pour le développeur
slug: mailcatcher-l-outil-pour-le-developpeur

---

# MailCatcher

J'avais envie de vous présenter [MailCatcher](http://mailcatcher.me) qui
est un petit outil très utile que tout développeur doit au moins
connaitre.

L'idée de [MailCatcher](http://mailcatcher.me), est de proposer un
server SMTP tournant sur le port 1025 et permettant ainsi de récupérer
tous les emails qui auront été émis par votre application.

Cet outil est très important si vous désirez vérifier tous les emails
sortant de votre système sans devoir modifier une configuration ou
commencer à bidouiller des emails.

## Installation

MailCatcher est un gem Ruby, il est donc installable sur les systèmes
possédant Ruby

    gem install mailcatcher

Afin de l'exécuter, veuillez simplement lancer l'application via la
commande suivante

    mailcatcher

Attention, cette commande lancera MailCatcher en mode daemon par défaut,
si vous désirez l'utiliser sans passer par un mode daemon, ajouter le
paramètre -f sur la ligne de commande.

    mailcatcher -f

## Utilisation

J'utilise l'outil swaks que vous pouvez installer via le package manager
de votre distribution. Dans mon cas, il s'agit de fedora, mais vous
pouvez l'avoir dans Debian ou Ubuntu.

    yum install swaks

    apt-get install swaks

Une fois installé, vous pouvez utiliser l'outil comme indiqué dans
l'exemple ci-dessous

    swaks --from stephane@wirtel.be --to stephane@wirtel.be --server localhost --port 1025

## Vérification

![MailCatcher](http://i.imgur.com/kg2QC.png)

Comme vous pouvez le constater, mon mail est bien arrivé dans
MailCatcher, et il m'est donc possible de le regarder à mon aise.

## Cas d'utilisation

### Utilisation avec Devise et Rails

Devise donne la possibilité d'envoyer des emails lors de l'inscription
d'un utilisateur. Avec cet outil, il vous est donc possible de regarder
le contenu sans devoir passer votre temps à inspecter les logs de Rails.

## Références

- [swaks](http://www.jetmore.org/john/code/swaks/)
- [MailCatcher](http://mailcatcher.me)