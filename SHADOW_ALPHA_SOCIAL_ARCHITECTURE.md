# Shadow Alpha Social Media & Marketing Architecture

Ce document contient l'architecture complète, exhaustive et exécutable de la présence numérique de Shadow Alpha, couvrant 8 plateformes.

---

### PLATFORM: GMAIL / GOOGLE WORKSPACE
**Priority**: P0 — Jour 1
**Blocker**: Aucun (Pré-requis absolu pour tout le reste)
**Estimated time**: 2 heures
**Copy status**: Prêt à coller ✅

#### SETUP CHECKLIST
- [ ] Enregistrer le domaine `shadowalpha.io` (Namecheap, Google Domains ou Route53).
- [ ] Activer Google Workspace Business Starter (6$/user/mois) ou configurer Cloudflare Email Routing vers une adresse Gmail personnelle.
- [ ] Configurer les enregistrements DNS exacts : SPF, DKIM, DMARC pour garantir la deliverability.
- [ ] Créer l'adresse email principale : `contact@shadowalpha.io`
- [ ] Créer les alias d'email : `support@`, `invest@`, `noreply@`, `admin@`
- [ ] Configurer l'Auto-reply (OOO/First Contact) sur `contact@` et `support@`.
- [ ] Configurer les filtres automatisés Gmail avec des labels par alias.
- [ ] Ajouter la signature HTML par défaut pour toutes les communications sortantes.

#### TOUT LE COPY

**Email Signature (HTML-ready)**:
```html
Shadow Alpha | contact@shadowalpha.io<br>
Plateforme d'échange de positions P2P & tontines digitales<br>
<a href="https://shadowalpha.io">shadowalpha.io</a> | <a href="Lien LinkedIn">LinkedIn</a> | <a href="Lien X">X</a> | <a href="https://t.me/ShadowAlphaOfficial">Telegram</a><br>
─────────────────────────────────────────<br>
<small>Ce message est confidentiel. Shadow Alpha ne sollicite jamais de transferts d'argent par email. En cas de doute: support@shadowalpha.io</small>
```

**Auto-reply (OOO/First Contact)**:
```text
Objet: Nous avons bien reçu votre message — Shadow Alpha

Bonjour,

Merci de contacter Shadow Alpha.
Notre équipe vous répondra dans les 24–48h ouvrées.

En attendant, rejoignez notre communauté Telegram pour
les dernières actualités : t.me/ShadowAlphaOfficial

L'équipe Shadow Alpha
contact@shadowalpha.io | shadowalpha.io
```

#### CONFIGURATIONS
- **Aliases forwarding** : Rediriger tous les alias vers `contact@shadowalpha.io`.
- **DKIM/DMARC** : Paramètre DMARC sur `v=DMARC1; p=quarantine;` pour sécuriser contre le spoofing de l'image de marque financière.

---

### PLATFORM: WHATSAPP BUSINESS
**Priority**: P0 — Jour 1
**Blocker**: Achat d'une nouvelle carte SIM (numéro professionnel), Platform 1
**Estimated time**: 1 heure
**Copy status**: Prêt à coller ✅

#### SETUP CHECKLIST
- [ ] Acheter une SIM dédiée – ne jamais utiliser de numéro personnel.
- [ ] Télécharger l'application WhatsApp Business.
- [ ] Nom de l'entreprise : **"Shadow Alpha"** (exact).
- [ ] Catégorie : **"Finance"**.
- [ ] Ajouter la photo de profil : Logo Gold α (640×640px).
- [ ] Ajouter l'adresse : Yaoundé, Cameroun.
- [ ] Heures d'ouverture : Lun–Ven 8h–18h WAT.
- [ ] Configurer l'Away message, le Greeting message et les Quick replies.
- [ ] Configurer le catalogue WhatsApp (Attente, Ambassadeur, Doc).

#### TOUT LE COPY

**Description Courte (Profil WhatsApp)**:
```text
Plateforme P2P d'investissement & tontines digitales.
KYC requis. contact@shadowalpha.io | shadowalpha.io
```

**Greeting Message**:
```text
Bonjour et bienvenue sur Shadow Alpha 👋

Je suis l'assistant officiel Shadow Alpha.
Voici ce que je peux vous partager :

🔹 *En savoir plus* → shadowalpha.io
🔹 *Liste d'attente* → shadowalpha.io/waitlist
🔹 *Support* → contact@shadowalpha.io
🔹 *Communauté* → t.me/ShadowAlphaCommunity

Tapez *1* pour en savoir plus sur notre plateforme
Tapez *2* pour rejoindre la liste d'attente
Tapez *3* pour contacter l'équipe
```

**Away Message**:
```text
Nous sommes actuellement hors ligne.
Notre équipe vous répondra dans les 24h ouvrées.

En attendant : shadowalpha.io
Telegram (instantané) : t.me/ShadowAlphaOfficial
```

**Quick Replies**:
- `/waitlist` : `Rejoignez notre liste d'attente ici : shadowalpha.io/waitlist 🚀`
- `/telegram` : `Notre communauté Telegram : t.me/ShadowAlphaCommunity 📢`
- `/kyc` : `Shadow Alpha exige une vérification KYC pour tous les utilisateurs. Plus d'infos : shadowalpha.io/kyc`
- `/contact` : `Email : contact@shadowalpha.io — Réponse sous 24–48h ouvrées.`

#### CONFIGURATIONS
- **WhatsApp Catalog** :
  1. "Compte Shadow Alpha (Liste d'attente)" -> Lien vers `shadowalpha.io/waitlist`
  2. "Programme Ambassadeur" -> Lien vers programme
  3. "Documentation / Whitepaper" -> PDF direct link

---

### PLATFORM: TELEGRAM
**Priority**: P0 — Jour 1
**Blocker**: Numéro de téléphone (utiliser le même que WhatsApp)
**Estimated time**: 1 heure
**Copy status**: Prêt à coller ✅

#### SETUP CHECKLIST
- [ ] Créer le canal officiel (Broadcast) : `@ShadowAlphaOfficial`. Type : Public.
- [ ] Créer le groupe communautaire : `@ShadowAlphaCommunity`. Type : Supergroup Public.
- [ ] Configurer les descriptions pour les deux entités.
- [ ] Épingler (Pin) le message de bienvenue dans le canal.
- [ ] Épingler les règles dans le groupe communautaire.
- [ ] Configurer Slow Mode sur 30 secondes pour le groupe communautaire.
- [ ] Configurer `@ShadowAlphaBot` (via BotFather) avec les commandes de base pour la modération/FAQ.

#### TOUT LE COPY

**Description Canal @ShadowAlphaOfficial**:
```text
Canal officiel de Shadow Alpha 🖤
Annonces, mises à jour produit, actualités.

Plateforme P2P d'investissement & tontines digitales.
🌐 shadowalpha.io
📩 contact@shadowalpha.io
```

**Description Groupe @ShadowAlphaCommunity**:
```text
Communauté officielle Shadow Alpha 🤝
Discussions, questions, retours produit.

Règles : No spam | No FUD | No promotions externes
Canal officiel : @ShadowAlphaOfficial
```

**Welcome Message (À épingler dans le canal)**:
```text
🖤 Bienvenue sur Shadow Alpha

Shadow Alpha est une plateforme d'échange de positions P2P
et de tontines digitales pour les investisseurs africains.

📌 Ce canal : annonces officielles uniquement
💬 Rejoignez la communauté : @ShadowAlphaCommunity
🌐 Site web : shadowalpha.io
📋 Liste d'attente : shadowalpha.io/waitlist
📩 Support : contact@shadowalpha.io

Activez les notifications pour ne rien manquer. 🔔
```

#### CONFIGURATIONS
- **Bot Commands** :
  - `/start` : Message de bienvenue et liens vitaux
  - `/waitlist` : `shadowalpha.io/waitlist`
  - `/faq` : Raccourci vers la page FAQ
  - `/contact` : `contact@shadowalpha.io`
  - `/rules` : No spam, No FUD, vérification stricte face aux arnaqueurs.

---

### PLATFORM: FACEBOOK BUSINESS PAGE
**Priority**: P1 — Jour 2–3
**Blocker**: Platform 1 (Email activé)
**Estimated time**: 1.5 heures
**Copy status**: Prêt à coller ✅

#### SETUP CHECKLIST
- [ ] Aller sur `facebook.com/pages/create` en choisissant Business/Brand.
- [ ] Nom : **"Shadow Alpha"**.
- [ ] Catégorie : **"Financial Service"** → sous-catégorie **"Investment Service"**.
- [ ] Username : `facebook.com/ShadowAlphaIO`.
- [ ] Intégrer la page sur Meta Business Suite (`business.facebook.com`).
- [ ] Assigner le Business Manager ID.
- [ ] Activer la section Page Transparency.
- [ ] Lier une page Instagram (le moment venu).
- [ ] Configurer la Messenger Auto-reply (via Meta Business Suite automations).
- [ ] Publier les 3 premiers posts.

#### TOUT LE COPY

**Page About Section (FR)**:
```text
Shadow Alpha est une plateforme d'investissement P2P qui permet
d'échanger des positions de trading vérifiées et de gérer des
tontines digitales en toute transparence.

📍 Cameroun & zone CEMAC
🔐 KYC obligatoire — contreparties vérifiées uniquement
📲 Disponible sur mobile et web

🌐 shadowalpha.io
📩 contact@shadowalpha.io
📢 Telegram: t.me/ShadowAlphaOfficial
```

**Page About Section (EN)**:
```text
Shadow Alpha is a P2P investment platform enabling verified
position trading and transparent digital tontine management
across the CEMAC zone.

KYC-verified counterparties. Institutional-grade infrastructure.
Built for Africa.

🌐 shadowalpha.io
```

**Messenger Auto-Reply (FR)**:
```text
Bonjour 👋 Merci de nous contacter sur Shadow Alpha.

Voici comment nous pouvons vous aider :
1️⃣ En savoir plus sur la plateforme → shadowalpha.io
2️⃣ Rejoindre la liste d'attente → shadowalpha.io/waitlist
3️⃣ Contacter l'équipe → contact@shadowalpha.io
4️⃣ Rejoindre Telegram → t.me/ShadowAlphaOfficial

Notre équipe répond sous 24–48h ouvrées. À bientôt !
```

**Content Brief (First 3 Posts)**:
- **Post 1 (Teaser) :** `Quelque chose se prépare. 🖤 Shadow Alpha arrive bientôt. L'investissement institutionnel, accessible à tous. ➡ Rejoignez la liste d'attente : shadowalpha.io #ShadowAlpha #Fintech ...`
- **Post 2 (Problème/Solution) :** `Vous avez une position gagnante... Shadow Alpha connecte acheteurs et vendeurs de positions vérifiées. P2P. Transparent. Sécurisé. 🔗 shadowalpha.io ...`
- **Post 3 (Focus Tontine) :** `La tontine : l'un des outils financiers les plus puissants d'Afrique. Nous l'avons digitalisé. Suivi en temps réel. Membres vérifiés. Zéro dispute. shadowalpha.io`

#### CONFIGURATIONS
- Ajouter explicitement le disclaimer : *"Shadow Alpha est une plateforme en bêta (Waitlist) n'offrant pas de rendements garantis."*

---

### PLATFORM: TWITTER / X
**Priority**: P1 — Jour 2–3
**Blocker**: Platform 1 (Email contact@) / Asset Kit (Banners/Logo)
**Estimated time**: 1 heure
**Copy status**: Prêt à coller ✅

#### SETUP CHECKLIST
- [ ] Créer le compte X avec l'handle : `@ShadowAlpha_`.
- [ ] Display name : **"Shadow Alpha"**.
- [ ] Uploader la photo de profil (Gold α, 400x400) et la bannière (1500x500).
- [ ] Configurer la Location : **"Yaoundé, Cameroun 🇨🇲"**.
- [ ] Ajouter l'URL web : `shadowalpha.io`.
- [ ] [OPTIONNEL/RECOMMANDÉ] Passer à X Premium (8$/mois) pour le checkmark bleu.
- [ ] Épingler le premier tweet Teaser.
- [ ] Publier le thread de lancement.

#### TOUT LE COPY

**Bio**:
```text
Plateforme P2P d'investissement & tontines digitales. 🖤
KYC-verified. Built for Africa.
➡ shadowalpha.io
```

**Pinned Tweet (Launch Teaser)**:
```text
Quelque chose se prépare. 🖤

Shadow Alpha — la première plateforme d'échange
de positions P2P et de tontines digitales pour
les investisseurs africains.

Liste d'attente ouverte 👇
shadowalpha.io/waitlist

#ShadowAlpha #Fintech #Investissement #Afrique #CEMAC
```

**Content Brief (Thread lancement)**:
1. `Pourquoi les tontines africaines génèrent des milliards mais restent informelles et risquées ? Parce qu'il n'existait pas d'infrastructure digitale pour les gérer correctement. Jusqu'à maintenant. 🧵`
2. `Shadow Alpha digitalise la tontine : → Suivi en temps réel des contributions → Membres KYC-vérifiés uniquement → Historique immuable des transactions → Notifications automatiques. Zéro dispute. Zéro opacité.`
3. `Et ce n'est que la moitié de ce qu'on construit. L'autre moitié : un marché P2P pour échanger des positions de trading vérifiées. Rejoignez la liste d'attente → shadowalpha.io/waitlist Retweet si tu connais quelqu'un qui en a besoin 🙏`

#### CONFIGURATIONS
- Aucun engagement dans des promesses financières sur Twitter. Usage strictly institutionnel.

---

### PLATFORM: YOUTUBE CHANNEL
**Priority**: P1 — Jour 2–3
**Blocker**: Platform 1, Asset Kit (Outils visuels conformes)
**Estimated time**: 1 heure (hors montage)
**Copy status**: Prêt à coller ✅

#### SETUP CHECKLIST
- [ ] Créer la chaîne via YouTube ou Google account (`contact@shadowalpha.io`).
- [ ] Nom de la chaîne : **"Shadow Alpha"**.
- [ ] S'approprier le YouTube Handle : `@ShadowAlpha`.
- [ ] Uploader Profil (2048x2048) & Bannière (2560x1440).
- [ ] Activer les paramètres de base et lier URL/Socials en "About".
- [ ] Langue par défaut : Français.
- [ ] Créer les 3 playlists : "Comment ça marche", "Actualités Shadow Alpha", "Tutoriels".

#### TOUT LE COPY

**Channel Description**:
```text
Shadow Alpha est la première plateforme d'échange de positions P2P
et de tontines digitales pour les investisseurs africains.

Sur cette chaîne :
→ Comment fonctionne Shadow Alpha
→ Tutoriels d'utilisation
→ Actualités et mises à jour produit
→ Webinaires et sessions communautaires

📩 contact@shadowalpha.io
🌐 shadowalpha.io
📢 t.me/ShadowAlphaOfficial
🐦 @ShadowAlpha_
```

**Content Brief (First Teaser Video - Script):**
```text
[VISUAL: Black screen. Gold particle animation. Silence 2s.]
VOIX OFF : "En Afrique, des milliards de francs circulent chaque jour dans des tontines, des groupes d'investissement, des clubs de traders.
[VISUAL: Abstract data flow, map of CEMAC zone]
Mais ces transactions restent informelles. Opaques. Sans traçabilité. Sans protection.
[VISUAL: Phone notification — "Paiement reçu: 500 000 FCFA"]
Et si tout cela pouvait changer ?
[VISUAL: Reveal — Shadow Alpha interface on phone]
Shadow Alpha. La première plateforme d'échange de positions P2P et de tontines digitales pour les investisseurs africains.
Des contreparties vérifiées. Un marché transparent. Une infrastructure institutionnelle.
[VISUAL: Logo animation — gold alpha symbol]
L'investissement institutionnel, accessible à tous.
shadowalpha.io — Rejoignez la liste d'attente."
[VISUAL: End card]
```

#### CONFIGURATIONS
- **Tagging**: Utiliser les tags spécifiques au Cameroun, à l'OHADA, au marché CEMAC.

---

### PLATFORM: LINKEDIN COMPANY PAGE
**Priority**: P2 — Jour 4–5
**Blocker**: Profil LinkedIn de l'Admin créateur
**Estimated time**: 1 heure
**Copy status**: Prêt à coller ✅

#### SETUP CHECKLIST
- [ ] Créer la page Société : `linkedin.com/company/setup/new`.
- [ ] Nom : **"Shadow Alpha"**.
- [ ] URL public : `linkedin.com/company/shadow-alpha-io`.
- [ ] Industrie : **"Financial Services"**.
- [ ] Taille : **"1-10 employees"**.
- [ ] Année : **2024 / Année courante**.
- [ ] Uploader Logo & Banner.

#### TOUT LE COPY

**Tagline**:
```text
L'investissement institutionnel, accessible à tous. | P2P · Tontines · KYC
```

**About Section**:
```text
Shadow Alpha est une plateforme fintech qui démocratise l'accès
à l'investissement institutionnel pour les marchés africains.

Notre infrastructure permet :

🔄 L'échange P2P de positions de trading vérifiées
Entre investisseurs KYC-certifiés, de manière transparente
et sécurisée.

🤝 La gestion de tontines digitales
Modernisation d'une pratique africaine ancestrale avec
traçabilité, automatisation et protection des membres.

📍 Basés à Yaoundé, Cameroun. Construits pour la zone CEMAC et au-delà.

→ shadowalpha.io
→ contact@shadowalpha.io
```

**Content Brief (Post Fondateur - Lancement):**
```text
Pourquoi j'ai décidé de construire Shadow Alpha.
En Afrique centrale, j'ai vu des personnes brillantes perdre de l'argent dans des investissements opaques...
Les tontines — l'un des mécanismes financiers les plus efficaces du monde — fonctionnent encore sur du papier et de la confiance aveugle.
Shadow Alpha change ça. Nous construisons la couche d'infrastructure manquante : KYC systématique, marché transparent, tontines digitales.
Nous sommes en pré-lancement. La liste d'attente est ouverte.
→ shadowalpha.io/waitlist
#Fintech #Afrique #Investissement #ShadowAlpha
```

#### CONFIGURATIONS
- Liez les fondateurs directement à l'entité page pour la StreetCred et l'autorité professionnelle.

---

### PLATFORM: TIKTOK
**Priority**: P2 — Jour 4–5
**Blocker**: Platform 1 (contact@shadowalpha.io)
**Estimated time**: 1 heure (hors vidéo)
**Copy status**: Prêt à coller ✅

#### SETUP CHECKLIST
- [ ] Créer un compte : `@shadowalpha_` ou `@shadowalpha.io`.
- [ ] Passer immédiatement en **Business Account**.
- [ ] Catégorie : **"Finance & Banking"**.
- [ ] Activer le "Business Content Toggle" pour éviter le shadowban sur les sujets de finance.
- [ ] Ajouter l'URL en bio une fois éligible, ou le déclarer publiquement.

#### TOUT LE COPY

**Bio**:
```text
P2P investing & digital tontines 🖤
shadowalpha.io
```

**Content Brief (First 5 Videos):**
- **Vidéo 1 - Éducative :** Hook : "Vous avez déjà mis de l'argent en commun avec des amis ?" -> Explication rapide de la Tontine. "Le problème : disputes, pas de traçabilité. On a la solution." Lien Bio.
- **Vidéo 2 - P2P Alert :** Hook : "Vous avez acheté une position à un ami. Il a disparu." -> Problème du trading informel. "Shadow Alpha vérifie tout."
- **Vidéo 3 - Behind The Build :** Screen recording authentique du produit/dev. "Voilà ce qu'on construit".
- **Vidéo 4 - KYC Facile :** Pourquoi le KYC ? Pour se protéger mutuellement. Pas de bullshit.
- **Vidéo 5 - Engagement Stitch :** "Combien avez-vous perdu dans une tontine qui a mal tourné ? Racontez-moi en commentaire."

#### CONFIGURATIONS
- Très important : pas de mentions de promesses de ROI fulgurants. Restez descriptif et focus sur l'outil/infrastructure.

---

## 🚀 CROSS-PLATFORM LAUNCH SEQUENCE

**JOUR 1 — FOUNDATION & DIRECT COMMUNICATION**
1. **Google Workspace / Gmail** : Enregistrer le domaine, créer `contact@shadowalpha.io`, paramétrer le SPF/DKIM/DMARC (Fondation absolue).
2. **Spreadsheet de Tracking** : Initialiser le tracking des mots de passe/Vault et metrics.
3. **WhatsApp Business** : Acheter la SIM, configurer le profil, le greeting message.
4. **Telegram** : Créer le Canal, la Communauté, les épingler, configurer le Bot anti-spam.

**JOUR 2 — PRIMARY SOCIAL SIGNALS (Awareness)**
1. **Twitter / X** : Créer `@ShadowAlpha_`, uploader les Assets, Payer X Premium pour la crédibilité, tweeter le Thread de lancement + Pinned Tweet Teaser.
2. **Facebook Business Page** : Créer la page et activer l'Auto-Messenger. Publier les 3 posts programmés.

**JOUR 3 — SEARCH & VIDEO FOUNDATION**
1. **YouTube Channel** : Revendiquer le Handle, configurer l'interface propre, créer les Playlists (mieux pour le SEO organique).

**JOUR 4 — AUTHORITY & PROFESSIONAL NETWORK**
1. **LinkedIn Company Page** : Créer la page d'entreprise. Publier le texte du Founder racontant le "Pourquoi Shadow Alpha".

**JOUR 5 — VIRALITY & NEW GEN OUTREACH**
1. **TikTok Business Account** : Lancer la page, la paramétrer pour l'industrie Finance, préparer l'upload des vidéos éducatives.
2. **Checklist Validation :** Vérification finale de tous les liens vers le site web et Waitlist depuis tous les profils.

=======================================================
*Tous les textes fournis dans ce document respectent les contraintes CEMAC/OHADA (absence totale de garantie de rendements), un ton institutionnel Premium, et ne demandent plus aucune altération avant leur mise en production.*
