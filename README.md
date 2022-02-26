# Project: PersonaChatBot

## Description

API for creating a bot with a set of personalities and chat with it! This is a simple, bare-bones, working prototype. Model taken from https://huggingface.co/af1tang/personaGPT

## API Documentation

### Create a chatbot

**Endpoint:** POST /api/chatbot/create
**Content Type:** application/json
**Body:**

```
{
	"id": "dX7IEgjCI0k5yJZm",
	"name": "Anatroc"
}
```

**Response:**

```
{
	"id": "dX7IEgjCI0k5yJZm",
	"name": "Anatroc"
}
```

### Get a chatbot

**Endpoint:** GET /api/chatbot/:id
**Response:**

```
{
	"id": "dX7IEgjCI0k5yJZm",
	"name": "Anatroc"
}
```

### Add a personality trait

**Endpoint:** POST /api/personality/add
**Content Type:** application/json
**Body:**

```
{
	"id": "dX7IEgjCI0k5yJZm",
	"personality": "I like surfing and birdwatching"
}
```

**Response:** No Response

### Get a chatbot's personality traits

**Endpoint:** GET /api/personality/:id
**Response:**

```
{
	"id": "dX7IEgjCI0k5yJZm",
	"personalities": [
    "My name is Anatroc",
    "I like surfing and birdwatching"
  ]
}
```

### Get the dialogue with a chatbot

**Endpoint:** GET /api/dialogue/:id
**Response:**

```
{
	"id": "dX7IEgjCI0k5yJZm",
	"dialogue": [
    "Hello there!",
    "hi there! whats your favorite activity?"
  ]
}
```

### Converse with a chatbot

**Endpoint:** POST /api/converse
**Content Type:** application/json
**Body:**

```
{
	"id": "dX7IEgjCI0k5yJZm",
	"message": "I like reading."
}
```

**Response:**

```
i'm a surfing enthusiast.
```

## Development

0. Install Python and pip
1. Activate the venv: `venv\Scripts\activate.bat` OR `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize database if needed: `python setup.py`
4. Run the app: `flask run`
