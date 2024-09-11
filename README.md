
# AgriChain 360 API

AgriChain 360 est une API Django permettant de gérer les utilisateurs, les données des capteurs, les alertes et les notifications pour un système de gestion agricole. Cette API peut être intégrée dans des applications web ou mobiles pour surveiller les conditions des capteurs, envoyer des alertes et gérer les utilisateurs.

## Prérequis

Avant d'installer et d'utiliser l'API, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.x
- Django 4.x
- Django REST Framework
- pip (gestionnaire de packages Python)
- [Flutter](https://flutter.dev/docs/get-started/install) (pour les développeurs mobiles)

## Installation

### 1. Cloner le dépôt

Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/votre-repository/agri-chain-360.git
cd agri-chain-360
```

### 2. Créer un environnement virtuel (venv)

Un environnement virtuel est un espace isolé pour installer des dépendances spécifiques à votre projet sans affecter les autres projets Python sur votre machine.

Pour créer et activer un environnement virtuel :

```bash
# Créez un environnement virtuel dans le dossier actuel
python -m venv venv

# Activez l'environnement virtuel (Linux/macOS)
source venv/bin/activate

# Sur Windows
venv\Scripts\activate
```

Une fois activé, l'environnement virtuel isolera toutes les installations de dépendances. Vous pouvez voir que l'environnement est actif si le préfixe `(venv)` apparaît dans votre terminal.

### 3. Installer les dépendances

Installez les packages nécessaires à partir du fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations de base de données

Créez les tables dans la base de données avec la commande suivante :

```bash
python manage.py migrate
```

### 5. Créer un superutilisateur

Un superutilisateur est un compte administrateur qui peut accéder à l'interface d'administration Django.

```bash
python manage.py createsuperuser
```

Suivez les instructions pour entrer un nom d'utilisateur, une adresse email et un mot de passe.

### 6. Lancer le serveur de développement

Démarrez le serveur Django pour utiliser l'API localement :

```bash
python manage.py runserver
```

L'API est maintenant disponible à l'adresse suivante : `http://127.0.0.1:8000/api/`.

---

## Modèles disponibles

L'API gère les entités suivantes :

1. **User (Utilisateur)** : Gère les informations des utilisateurs.
2. **SensorData (Données des capteurs)** : Gère les données provenant de capteurs comme la température ou l'humidité.
3. **Alert (Alerte)** : Gère les alertes comme les conditions météorologiques ou d'irrigation.
4. **Notification** : Gère les notifications envoyées aux utilisateurs.

Chaque entité a des attributs spécifiques (voir les détails dans le code).

---

## Utilisation de l'API

### Exemples de requêtes

#### Récupérer tous les utilisateurs

```bash
GET /api/users/
```

#### Créer un nouvel utilisateur

```bash
POST /api/users/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john_doe@example.com",
  "password": "password123"
}
```

---

## Intégration dans une application mobile (Flutter)

Pour intégrer cette API dans une application mobile Flutter, vous pouvez utiliser le package `http` pour effectuer des requêtes HTTP. Voici un exemple détaillé de la manière de faire.

### 1. Ajouter le package HTTP à Flutter

Dans votre fichier `pubspec.yaml`, ajoutez la dépendance suivante :

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.3
```

Ensuite, installez les dépendances :

```bash
flutter pub get
```

### 2. Exemple de requête GET dans Flutter

Voici un exemple d'application Flutter qui récupère les données des utilisateurs depuis l'API.

```dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: UserList(),
    );
  }
}

class UserList extends StatefulWidget {
  @override
  _UserListState createState() => _UserListState();
}

class _UserListState extends State<UserList> {
  List users = [];

  @override
  void initState() {
    super.initState();
    fetchUsers();
  }

  fetchUsers() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:8000/api/users/'));

    if (response.statusCode == 200) {
      setState(() {
        users = json.decode(response.body);
      });
    } else {
      throw Exception('Failed to load users');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Users'),
      ),
      body: ListView.builder(
        itemCount: users.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(users[index]['username']),
            subtitle: Text(users[index]['email']),
          );
        },
      ),
    );
  }
}
```

### 3. Expliquer le fonctionnement

Dans cet exemple :
- Le package `http` est utilisé pour effectuer une requête GET à l'API (`http://127.0.0.1:8000/api/users/`).
- Les données JSON récupérées sont décodées et stockées dans une liste.
- Une `ListView` est utilisée pour afficher les utilisateurs dans l'interface Flutter.

### Important : Tester avec un émulateur

Lorsque vous utilisez un émulateur, assurez-vous que l'API est accessible. Si vous utilisez `localhost`, remplacez-le par l'IP locale de votre machine (`http://10.0.2.2:8000/` pour les émulateurs Android).

---

## Sécurisation de l'API avec JWT (JSON Web Tokens)

Pour sécuriser l'API, nous utilisons le package `djangorestframework-simplejwt` qui permet d'ajouter une authentification basée sur les tokens JWT.

### 1. Installer JWT

Ajoutez `djangorestframework-simplejwt` aux dépendances :

```bash
pip install djangorestframework-simplejwt
```

### 2. Configurer JWT dans `settings.py`

Ajoutez la configuration suivante dans le fichier `settings.py` pour activer JWT :

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

### 3. Ajouter les routes JWT

Dans votre fichier `urls.py`, ajoutez les routes pour gérer l'obtention et la vérification des tokens :

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### 4. Utilisation du token dans Flutter

Lors de l'authentification de l'utilisateur, récupérez le token JWT et utilisez-le pour chaque requête sécurisée.

```dart
fetchData() async {
  String token = 'votre_token_jwt';  // Récupéré lors de l'authentification
  final response = await http.get(
    Uri.parse('http://127.0.0.1:8000/api/sensordata/'),
    headers: {
      'Authorization': 'Bearer $token',
    },
  );

  if (response.statusCode == 200) {
    // Traitez les données reçues
  } else {
    throw Exception('Failed to load data');
  }
}
```

### Sécurisation des points de terminaison API

Pour sécuriser un point de terminaison, ajoutez la permission `IsAuthenticated` dans la vue.

```python
from rest_framework.permissions import IsAuthenticated

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    permission_classes = [IsAuthenticated]  # Utilisation de la permission
```

---

## Conclusion

L'API AgriChain 360 est prête à être utilisée et sécurisée avec des tokens JWT. Elle peut être intégrée facilement dans des applications web ou mobiles (comme Flutter). Pour toute question ou amélioration, veuillez soumettre une issue sur ce dépôt.
```

### Explications :

1. **Partie Flutter** : J'ai ajouté un exemple simple qui montre comment récupérer des données d'utilisateurs via une requête HTTP dans une application Flutter en utilisant le package `http`. L'exemple inclut une explication étape par étape sur la configuration du fichier `pubspec.yaml`, l'envoi de requêtes HTTP, et la gestion des réponses JSON.
  
2. **Venv**